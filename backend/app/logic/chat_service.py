import os
import json
from typing import AsyncGenerator, List

from openai import OpenAI
from fastapi import HTTPException

from app.logs.logger import get_logger
from app.models.data_structures import ChatRequest, DocumentChunk
from app.db.db_handler import DatabaseHandler
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from langchain_openai import OpenAIEmbeddings



logger = get_logger(__name__)


class ChatService:
    def __init__(self, llm_client: OpenAI, db_handler: DatabaseHandler, embeddings: OpenAIEmbeddings, llm_model: str):
        self.llm_client = llm_client
        self.db_handler = db_handler
        self.embeddings = embeddings
        self.llm_model = llm_model
        self.max_context_messages = 10  

    async def stream_chat(self, chat_request: ChatRequest) -> AsyncGenerator[str, None]:
        try:
            context = await self._fetch_relevant_context(chat_request.message)
            system_prompt = self._build_system_prompt(context)
            messages = self._build_messages(system_prompt, chat_request)
            
            stream = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                stream=True,
                temperature=0,
            )
            
            complete_response = ""
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    content = delta.content
                    complete_response += content
                    yield f'0:{json.dumps(content)}\n'
            
            await self.db_handler.log_chat(
                user_message=chat_request.message,
                assistant_message=complete_response,
                session_id=chat_request.session_id,
                timestamp=chat_request.timestamp
            )
        
        except Exception as e:
            logger.error(f"Error in stream_chat: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Se produjo un error al procesar su solicitud."
            )
            
    async def _fetch_relevant_context(self, user_message: str) -> str:
        """
       Obtenga el contexto relevante para la consulta del usuario mediante búsqueda semántica.
        Devuelve contenido concatenado de los fragmentos más relevantes.
        """
        try:
            logger.info(f"Obtener contexto relevante para la consulta: {user_message}")
            query_embedding: List[float] = self.embeddings.embed_query(user_message)
            chunks: List[DocumentChunk] = await self.db_handler.search_similar_chunks(
                query_embedding,
                limit=4
            )
            
            if not chunks:
                logger.info("No se encontró ningún contexto relevante para la consulta")
                return ""
            
            context = ""
            for chunk in chunks:    
                logger.info(f"Chunk: {chunk.content}")
                context += f"{chunk.content}\n\n"
            logger.info(f"Found {len(chunks)} fragmentos relevantes para el contexto")
            
            return context
            
        except Exception as e:
            logger.error(f"Error fetching context: {str(e)}")
            return ""
        
        
    
    def _build_system_prompt(self, context: str) -> str:
        base_prompt: str = f"""
            "Eres un asistente de IA profesional, diseñado para brindar interacción atractiva., "
            "Interacciones personalizadas basadas en mis experiencias y escritos. Sus respuestas deberían:\n"
            "1. Sea preciso y confíe únicamente en información verificada del contexto dado o conversaciones anteriores cuando sea relevante..\n"
            "2. Sea conciso, directo y claro y evite la verbosidad innecesaria.\n"
            "3. Mantener la continuidad haciendo referencia a intercambios anteriores cuando corresponda.\n"
            "4. Muestra personalidad sin dejar de ser profesional y cortés.\n"
            "5. Indique claramente cuándo no está seguro en lugar de adivinar.\n"
            "6. Negarse a compartir información confidencial o generar contenido dañino.\n"
            "7. Al crear un mensaje de respuesta, utilice siempre el formato Markdown adecuado.\n"
            "8. Al enumerar artículos, utilice siempre el formato de Markdown adecuado.\n"
        """

        if context:
            base_prompt += (
                f"\nUtilice el siguiente contexto para fundamentar sus respuestas:\n{context}\n"
                "Si bien puede hacer referencia a este contexto, mantenga un flujo de conversación natural. "
                "Si no estás seguro de algo, reconócelo explícitamente. "
            )
        else:
            base_prompt += (
                "\nNo hay contexto adicional del documento disponible. Si la conversación actual o los mensajes anteriores "
                "No proporcione contexto suficiente para responder una pregunta, no alucine ni fabrique información. "
                "En su lugar, indique claramente que le falta contexto suficiente para proporcionar una respuesta precisa."
            )
        logger.debug(f"System prompt length: {len(base_prompt)} characters")
        return base_prompt
    
    def _build_messages(self, system_prompt: str, chat_request: ChatRequest) -> List[ChatCompletionMessageParam]:
        messages = [{"role": "system", "content": system_prompt}]
        recent_messages = chat_request.messages[-self.max_context_messages:] if chat_request.messages else []
        messages.extend({"role": msg.role, "content": msg.content} for msg in recent_messages)
        messages.append({"role": "user", "content": chat_request.message})
        return messages


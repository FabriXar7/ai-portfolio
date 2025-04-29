from typing import List
from sqlmodel import Session, SQLModel, create_engine
from contextlib import contextmanager
from datetime import datetime
from app.db.db_config import PostgresConfig
from app.models.data_structures import ChatLog, DocumentChunk
from app.logs.logger import get_logger
from sqlalchemy import text
import numpy as np

logger = get_logger(__name__)

class DatabaseHandler:
    def __init__(self, db_config: PostgresConfig):
        self.config = db_config
        self.engine = create_engine(
            self.config.get_connection_url(),
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
            echo=False,
            pool_pre_ping=True,
        )
        self.__setup_vector_extension()
        self.__setup_database()

    def __setup_vector_extension(self):
        """Crea la extensión del vector si no existe"""
        try:
            with self.get_session() as session:
                session.exec(text('CREATE EXTENSION IF NOT EXISTS vector'))
                session.commit()
        except Exception as e:
            logger.error(f"No se pudo crear la extensión del vector: {str(e)}")
            raise RuntimeError(f"No se pudo crear la extensión del vector: {str(e)}")

    def __setup_database(self):
        try:
            SQLModel.metadata.create_all(self.engine)
        except Exception as e:
            logger.error(f"No se pudo inicializar la base de datos: {str(e)}")
            raise RuntimeError(f"No se pudo inicializar la base de datos: {str(e)}")

    @contextmanager
    def get_session(self):
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    async def log_chat(self, user_message: str, assistant_message: str, session_id: str, timestamp: datetime) -> None:
        """
        Registra las interacciones del chat en la base de datos con ID de sesión
        """
        chat_log = ChatLog(
            session_id=session_id,
            user_message=user_message,
            assistant_message=assistant_message,
            timestamp=timestamp
        )
        
        try:
            with self.get_session() as session:
                session.add(chat_log)
        except Exception as e:
            logger.error(f"No se pudo registrar el chat en la base de datos: {str(e)}")
            raise RuntimeError(f"No se pudo registrar el chat en la base de datos: {str(e)}")


    async def store_document_chunk(self, content: str, embedding: List[float], metadata: dict):
        """Almacenar un fragmento de documento utilizando el objeto ORM DocumentChunk."""
        chunk = DocumentChunk(
            content=content,
            embedding=embedding,
            doc_metadata=metadata
        )
        
        with self.get_session() as session:
            session.add(chunk)
    
    async def search_similar_chunks(self, query_embedding: List[float], limit: int) -> List[DocumentChunk]:
        """Encuentre los fragmentos de documentos más similares utilizando la similitud del coseno sin filtrar por umbral."""
        query = text("""
            SELECT 
                content, 
                doc_metadata,
                1 - (embedding <#> CAST(:embedding AS vector)) as similarity
            FROM documentchunk
            ORDER BY similarity DESC
            LIMIT :limit;
        """)

        try:
            with self.get_session() as session:
                results = session.exec(
                    query,
                    params={
                        'embedding': np.array(query_embedding).tolist(),
                        'limit': limit
                    }
                )
                return results.all()
                
        except Exception as e:
            logger.exception("Error en search_similar_chunks")
            return []

    async def document_exists(self, file_path: str) -> bool:
        """Comprobar si existen fragmentos de documentos para una ruta de archivo determinada."""
        query = text("""
            SELECT EXISTS (
                SELECT 1 FROM documentchunk 
                WHERE doc_metadata->>'source' = :file_path
                LIMIT 1
            );
        """)
        
        try:
            with self.get_session() as session:
                result = session.exec(query, params={'file_path': file_path}).first()
                return result[0] if result else False
        except Exception as e:
            logger.error(f"No se pudo verificar la existencia del documento: {str(e)}")
            return False

    async def get_document_hash(self, file_path: str) -> str:
        """Obtener el hash del contenido almacenado para un documento."""
        query = text("""
            SELECT doc_metadata->>'content_hash'
            FROM documentchunk 
            WHERE doc_metadata->>'source' = :file_path
            LIMIT 1;
        """)
        
        try:
            with self.get_session() as session:
                result = session.exec(query, params={'file_path': file_path}).first()
                return result[0] if result else None
        except Exception as e:
            logger.error(f"No se pudo obtener el hash del documento: {str(e)}")
            return None

    async def delete_document_chunks(self, file_path: str) -> bool:
        """Eliminar todos los fragmentos de un documento determinado."""
        query = text("""
            DELETE FROM documentchunk 
            WHERE doc_metadata->>'source' = :file_path;
        """)
        
        try:
            with self.get_session() as session:
                session.exec(query, params={'file_path': file_path})
                session.commit()
                return True
        except Exception as e:
            logger.error(f"No se pudieron eliminar fragmentos de documentos: {str(e)}")
            return False

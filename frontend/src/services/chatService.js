const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export class ChatService {
  static async handleStreamingResponse(response, callbacks) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullMessage = '';

    try {
      while (true) {
        if (callbacks.shouldStop?.()) {
          await reader.cancel();
          callbacks.onComplete(fullMessage);
          break;
        }

        const { done, value } = await reader.read();
        
        if (done) {
          callbacks.onComplete(fullMessage);
          break;
        }

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.trim() === '') continue;

          const match = line.match(/^0:(.+)$/);
          if (match) {
            try {
              const content = JSON.parse(match[1]);
              fullMessage += content;
              callbacks.onChunk(fullMessage);
              await new Promise(resolve => setTimeout(resolve, 30));
            } catch (e) {
              console.error('Error al analizar la respuesta de streaming:', e);
            }
          }
        }
      }
    } catch (e) {
      console.error('Error al leer el stream:', e);
      throw new Error('Error procesando la respuesta del stream');
    }
  }

  static async handleError(response) {
    const errorData = await response.json();
    if (response.status === 429) {
      return {
        isRateLimit: true,
        message: errorData.friendly_message || "Has alcanzado el límite de velocidad. Espera antes de enviar más mensajes.",
        retryAfter: errorData.retry_after
      };
    }
    throw new Error(errorData.detail || 'Fallo el envio del mensaje');
  }

  static async sendMessage(chatRequest) {
    const response = await fetch(`${BACKEND_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...chatRequest,
        messages: chatRequest.messages.map(({ role, content }) => ({ role, content }))
      }),
    });

    if (!response.ok) {
      return this.handleError(response);
    }

    return response;
  }
} 

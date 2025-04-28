# Sistema de configuración

Este documento explica el sistema de configuración utilizado en el proyecto AI Portfolio. Este sistema permite personalizar el contenido del portafolio sin modificar el código.

## Descripción general

El proyecto utiliza un único archivo `config.json` en el directorio `public` para almacenar todos los valores de configuración. Este archivo es esencial para el correcto funcionamiento de la aplicación. El frontend requiere que este archivo esté presente y mostrará un mensaje de error si no se encuentra.

## Estructura del archivo de configuración

El archivo `config.json` tiene la siguiente estructura:

```json
{
  "personal": {
    "name": "Your Name",
    "email": "your.email@example.com",
  },
  "social": {
    "github": {
      "url": "https://github.com/yourusername"
    },
    "linkedin": {
      "url": "https://linkedin.com/in/yourusername"
    },
    "email": {
      "url": "mailto:your.email@example.com"
    }
  },
  "content": {
    "intro": {
      "cards": [
        {
          "title": "Característica 1",
          "description": "Descripción de la característica 1",
          "icon": "Brain"
        },
        {
          "title": "Característica 2",
          "description": "Descripción de la característica 2",
          "icon": "BookOpen"
        },
        {
          "title": "Característica 3",
          "description": "Descripción de la característica 3",
          "icon": "MessageSquareText"
        }
      ],
      "paragraphs": [
        "Párrafo principal sobre ti.",
        "Párrafo secundario con información adicional."
      ]
    }
  },
  "chat": {
    "inputPlaceholder": "Pregúntame cualquier cosa sobre Su Nombre...",
    "initialMessage": "¡Hola! Soy la asistente de inteligencia artificial de (tu nombre). Tengo acceso a los datos de trabajos y curriculum vitae. ¡No dudes en preguntar y explorar su trayectoria profesional o crecimiento personal!"
  }
}
```

## Cómo personalizar

1. Edite el archivo `config.json` en el directorio `public`.
2. Actualice los valores para que coincidan con su información.
3. Reinicie el servidor de desarrollo o reconstruya la aplicación.

## Implementación técnica


El frontend utiliza un cargador de configuración que obtiene el archivo `config.json` y proporciona acceso a los valores de configuración mediante ganchos de React y funciones de utilidad. La configuración se carga al iniciar la aplicación y se almacena en caché para su posterior acceso.

Si no se puede cargar el archivo de configuración, la aplicación mostrará un mensaje de error al usuario indicando que se requiere el archivo `config.json`.


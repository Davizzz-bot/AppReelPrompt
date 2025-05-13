# AppReelPrompt: Generador de Video Corto IA (MVP)

Este proyecto es un MVP (Producto Mínimo Viable) de una aplicación web simple para generar videos cortos a partir de un prompt de texto utilizando inteligencia artificial. En su estado actual, la "IA" es una simulación que selecciona imágenes y música predefinidas basándose en palabras clave simples del prompt, y utiliza FFmpeg para ensamblar un video de diapositivas.

## Estado Actual (MVP)

*   **Funcionalidad:** La aplicación toma una idea de texto (prompt) del usuario.
*   **Generación de Video:** Selecciona un número limitado de imágenes y una pista de música de un conjunto predefinido de archivos locales, intentando hacer coincidir palabras clave básicas del prompt con etiquetas asociadas a las imágenes.
*   **Tecnología:**
    *   **Backend:** Python con Flask.
    *   **Frontend:** HTML, CSS (TailwindCSS via CDN) y JavaScript.
    *   **Generación de Video:** Utiliza la herramienta de línea de comandos FFmpeg para crear un video de diapositivas con música a partir de los archivos seleccionados.
*   **Estructura:** La aplicación sigue una estructura simple de Flask con templates para el frontend y archivos estáticos para los medios.
*   **Limitaciones Actuales:**
    *   La "IA" es muy básica (selección por palabras clave).
    *   Depende completamente de un conjunto limitado de imágenes y música locales predefinidas.
    *   La generación de video es síncrona y puede tardar, bloqueando el servidor (no ideal para producción).
    *   Requiere FFmpeg instalado en el sistema donde corre el backend.
    *   Los videos generados se guardan localmente (no persistente en muchos entornos de despliegue).
    *   Interfaz de usuario muy simple.

## Estructura del Proyecto

```
/
├── app.py                 # Backend de Flask con la lógica de generación.
├── templates/
│   └── index.html         # Frontend (HTML, CSS, JS).
├── static/
│   ├── media/             # Directorio para imágenes y música.
│   │   ├── images/        # Aquí deben colocarse las imágenes base.
│   │   └── music/         # Aquí deben colocarse los archivos de música base.
│   └── videos/            # Directorio temporal para videos generados (ignorado por git).
├── requirements.txt       # Dependencias de Python.
└── .gitignore             # Archivos y directorios a ignorar por Git.
```

## Configuración y Ejecución Local

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/Davizzz-bot/AppReelPrompt.git
    cd AppReelPrompt
    ```
2.  **Instalar Python:** Asegúrate de tener Python 3.x instalado.
3.  **Instalar FFmpeg:** Descarga e instala FFmpeg para tu sistema operativo y asegúrate de que esté en el PATH. [Guía de instalación de FFmpeg](https://ffmpeg.org/download.html)
4.  **Crear y Activar un Entorno Virtual (Recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    # venv\Scripts\activate
    # En macOS/Linux:
    # source venv/bin/activate
    ```
5.  **Instalar Dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```
6.  **Añadir Archivos de Media:**
    *   Crea las carpetas `static/media/images/` y `static/media/music/`.
    *   Coloca tus archivos `.jpg`, `.png`, etc. en `static/media/images/`.
    *   Coloca tus archivos `.mp3`, `.wav`, etc. en `static/media/music/`.
    *   **Importante:** Actualiza las listas `PREDEFINED_IMAGES` y `PREDEFINED_MUSIC` en `app.py` con las rutas y palabras clave relevantes para tus archivos.
7.  **Ejecutar la Aplicación Flask:**
    ```bash
    export FLASK_APP=app.py # En Windows usa set FLASK_APP=app.py
    flask run
    ```
    La aplicación se ejecutará localmente, probablemente en `http://127.0.0.1:5000/`.

## Posibles Mejoras y Estado Futuro

Este MVP sienta las bases para una aplicación de generación de video mucho más potente. Aquí hay ideas para futuras iteraciones:

*   **Integración con Modelos de IA Reales:** Reemplazar la selección de media predefinida con llamadas a APIs de generación de contenido (ej. DALL-E para imágenes, modelos de texto a voz para narración, modelos de texto a video).
*   **Gestión de Medios Avanzada:** Permitir a los usuarios subir sus propias imágenes y música, categorizarlas y usarlas en sus prompts.
*   **Mayor Control de Generación:** Añadir opciones en el frontend para controlar la duración del video, transiciones entre imágenes, añadir texto superpuesto, seleccionar estilos de música, etc.
*   **Procesamiento Asíncrono:** Implementar una cola de tareas (como Celery con Redis o RabbitMQ) para manejar la generación de video de forma asíncrona, evitando que las solicitudes largas bloqueen el servidor web principal y proporcionando retroalimentación de progreso al usuario.
*   **Almacenamiento en la Nube:** Configurar el almacenamiento de los videos generados en un servicio como AWS S3, Google Cloud Storage o similar para persistencia y escalabilidad.
*   **Mejoras de UI/UX:** Rediseñar el frontend para una experiencia más fluida, añadir indicadores de carga más claros, previsualizaciones, historial de videos generados.
*   **Autenticación de Usuarios:** Implementar un sistema de registro e inicio de sesión para que los usuarios puedan guardar sus prompts, videos y configuraciones.
*   **Optimización de FFmpeg:** Explorar parámetros de FFmpeg para optimizar la calidad, tamaño del archivo y velocidad de generación.
*   **Despliegue Sencillo:** Añadir configuraciones o scripts para facilitar el despliegue en plataformas cloud (Docker, Heroku, Render, etc.).

¡Siéntete libre de contribuir a este proyecto con nuevas ideas y código!

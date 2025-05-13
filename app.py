import os
import subprocess
import uuid
import random
import json # Importado para manejar el prompt
from flask import Flask, request, jsonify, render_template, url_for

app = Flask(__name__)

# --- Configuración ---
# Directorios (asegúrate de que existan)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
IMAGE_DIR = os.path.join(MEDIA_DIR, 'images')
MUSIC_DIR = os.path.join(MEDIA_DIR, 'music')
GENERATED_VIDEOS_DIR = os.path.join(STATIC_DIR, 'videos')

# Crear directorios si no existen
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)
os.makedirs(GENERATED_VIDEOS_DIR, exist_ok=True)

# Medios predefinidos (Imágenes y Música)
# DEBES CREAR ESTOS ARCHIVOS Y CARPETAS EN TU PROYECTO
# static/media/images/dog.jpg, cat.jpg, etc.
# static/media/music/ambient.mp3, upbeat.mp3, etc.
PREDEFINED_IMAGES = [
    {"path": os.path.join(IMAGE_DIR, "dog.jpg"), "keywords": ["perro", "animal", "mascota", "canino", "feliz"]},
    {"path": os.path.join(IMAGE_DIR, "cat.jpg"), "keywords": ["gato", "animal", "mascota", "felino"]},
    {"path": os.path.join(IMAGE_DIR, "beach.jpg"), "keywords": ["playa", "verano", "viaje", "mar", "arena", "vacaciones"]},
    {"path": os.path.join(IMAGE_DIR, "city.jpg"), "keywords": ["ciudad", "urbano", "edificios", "noche", "luces"]},
    {"path": os.path.join(IMAGE_DIR, "nature.jpg"), "keywords": ["naturaleza", "bosque", "montaña", "paisaje", "verde"]},
    {"path": os.path.join(IMAGE_DIR, "food.jpg"), "keywords": ["comida", "restaurante", "delicioso", "cena", "almuerzo"]},
    {"path": os.path.join(IMAGE_DIR, "party.jpg"), "keywords": ["fiesta", "celebracion", "amigos", "musica", "baile"]},
    {"path": os.path.join(IMAGE_DIR, "technology.jpg"), "keywords": ["tecnologia", "codigo", "computadora", "innovacion"]},
    {"path": os.path.join(IMAGE_DIR, "travel.jpg"), "keywords": ["viaje", "aventura", "mundo", "explorar"]},
    {"path": os.path.join(IMAGE_DIR, "sports.jpg"), "keywords": ["deportes", "futbol", "juego", "accion"]},
]

PREDEFINED_MUSIC = [
    {"path": os.path.join(MUSIC_DIR, "ambient.mp3"), "name": "Ambient"},
    {"path": os.path.join(MUSIC_DIR, "upbeat.mp3"), "name": "Upbeat"},
    {"path": os.path.join(MUSIC_DIR, "cinematic.mp3"), "name": "Cinematic"},
    {"path": os.path.join(MUSIC_DIR, "electronic.mp3"), "name": "Electronic"},
    {"path": os.path.join(MUSIC_DIR, "folk.mp3"), "name": "Folk"},
]

# Parámetros de video
NUM_IMAGES_TO_SELECT = 3
IMAGE_DURATION_SECONDS = 3 # Duración de cada imagen en el video
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 24

# --- Helper Functions ---

def select_media_from_prompt(prompt_text):
    """
    Selecciona imágenes basadas en palabras clave simples del prompt.
    Si no hay coincidencias, selecciona imágenes aleatorias.
    """
    selected_images = []
    prompt_lower = prompt_text.lower()
    
    # Buscar coincidencias de palabras clave
    for media_item in PREDEFINED_IMAGES:
        if any(keyword in prompt_lower for keyword in media_item["keywords"]):
            if os.path.exists(media_item["path"]): # Verificar si el archivo existe
                 selected_images.append(media_item["path"])

    # Si no hay suficientes imágenes por palabras clave, completar con aleatorias
    # (asegurándose de que los archivos existan)
    existing_image_paths = [img["path"] for img in PREDEFINED_IMAGES if os.path.exists(img["path"])]
    
    if not existing_image_paths: # No hay imágenes disponibles en absoluto
        return []

    while len(selected_images) < NUM_IMAGES_TO_SELECT and existing_image_paths:
        available_to_add = [p for p in existing_image_paths if p not in selected_images]
        if not available_to_add:
            break # No más imágenes únicas para agregar
        random_image_path = random.choice(available_to_add)
        selected_images.append(random_image_path)
        if len(selected_images) >= NUM_IMAGES_TO_SELECT:
            break
            
    return selected_images[:NUM_IMAGES_TO_SELECT]


def select_random_music():
    """Selecciona una pista de música aleatoria de las predefinidas."""
    existing_music_files = [music for music in PREDEFINED_MUSIC if os.path.exists(music["path"])]
    if not existing_music_files:
        return None # No hay música disponible
    return random.choice(existing_music_files)["path"]

def generate_video_ffmpeg(image_paths, music_path, output_filename):
    """
    Genera un video usando FFmpeg a partir de una lista de imágenes y una pista de música.
    Las imágenes se muestran secuencialmente.
    El video se formatea a vertical (1080x1920).
    """
    if not image_paths:
        raise ValueError("No se proporcionaron imágenes para generar el video.")

    temp_slideshow_path = os.path.join(GENERATED_VIDEOS_DIR, f"temp_slideshow_{uuid.uuid4()}.mp4")
    final_output_path = os.path.join(GENERATED_VIDEOS_DIR, output_filename)

    # 1. Crear slideshow de imágenes
    # FFmpeg input-args: -loop 1 -t <duration> -i <image_path>
    # FFmpeg filter_complex: scale, pad, concat
    inputs_ffmpeg = []
    filter_complex_parts = []
    
    for i, img_path in enumerate(image_paths):
        inputs_ffmpeg.extend(['-loop', '1', '-t', str(IMAGE_DURATION_SECONDS), '-i', img_path])
        # Escalar y pad para formato vertical, luego setpts para reiniciar timestamps (importante para concat)
        filter_complex_parts.append(
            f"[{i}:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,"
            f"pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"format=yuv420p,setpts=PTS-STARTPTS[v{i}];"
        )

    concat_inputs = "".join([f"[v{i}]" for i in range(len(image_paths))])
    filter_complex_str = "".join(filter_complex_parts) + \
                         f"{concat_inputs}concat=n={len(image_paths)}:v=1:a=0,format=yuv420p[v]"
    
    total_video_duration = len(image_paths) * IMAGE_DURATION_SECONDS

    ffmpeg_cmd_slideshow = [
        'ffmpeg',
        *inputs_ffmpeg,
        '-filter_complex', filter_complex_str,
        '-map', '[v]',
        '-r', str(VIDEO_FPS),
        '-t', str(total_video_duration), # Duración total del slideshow
        '-preset', 'ultrafast', # Más rápido para MVP
        temp_slideshow_path,
        '-y' # Sobrescribir archivo de salida si existe
    ]
    
    print("Comando FFmpeg (slideshow):", " ".join(ffmpeg_cmd_slideshow))
    try:
        subprocess.run(ffmpeg_cmd_slideshow, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("Error FFmpeg (slideshow):", e.stderr)
        # Intentar eliminar el archivo temporal si falló y existe
        if os.path.exists(temp_slideshow_path):
            os.remove(temp_slideshow_path)
        raise Exception(f"Error al crear slideshow: {e.stderr}")


    # 2. Añadir música al slideshow (si hay música disponible)
    if music_path and os.path.exists(music_path):
        ffmpeg_cmd_audio = [
            'ffmpeg',
            '-i', temp_slideshow_path,
            '-i', music_path,
            '-c:v', 'copy',         # Copiar stream de video (ya está procesado)
            '-c:a', 'aac',          # Re-codificar audio a AAC (común)
            '-shortest',            # El video finaliza cuando el stream más corto termina
            '-fflags', '+shortest', # Asegura que shortest funcione correctamente
            '-max_interleave_delta', '100M', # Para algunos casos de desincronización
            final_output_path,
            '-y' # Sobrescribir
        ]
        print("Comando FFmpeg (audio):", " ".join(ffmpeg_cmd_audio))
        try:
            subprocess.run(ffmpeg_cmd_audio, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print("Error FFmpeg (audio):", e.stderr)
            # Limpiar slideshow si el paso de audio falla
            if os.path.exists(temp_slideshow_path):
                os.remove(temp_slideshow_path)
            raise Exception(f"Error al añadir música: {e.stderr}")
        finally:
            # Eliminar el slideshow temporal después de añadir audio (o si falla)
            if os.path.exists(temp_slideshow_path):
                os.remove(temp_slideshow_path)
    else: # Si no hay música, simplemente renombra el slideshow
        print("No se encontró música o no se proporcionó. Usando video sin audio.")
        os.rename(temp_slideshow_path, final_output_path)
        
    return final_output_path

# --- Rutas de la API ---

@app.route('/')
def index():
    """Sirve la página HTML principal."""
    return render_template('index.html') # Asume que tu HTML está en templates/index.html

@app.route('/generate-video', methods=['POST'])
def handle_generate_video():
    """
    Endpoint para generar el video. Recibe un prompt de texto,
    genera el video y devuelve la URL del video.
    """
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Prompt no proporcionado."}), 400
        
        prompt_text = data['prompt']
        
        # 1. Seleccionar imágenes basadas en el prompt
        selected_image_paths = select_media_from_prompt(prompt_text)
        if not selected_image_paths:
            # Verificar si PREDEFINED_IMAGES está vacío o si los archivos no existen
            if not any(os.path.exists(img["path"]) for img in PREDEFINED_IMAGES):
                 return jsonify({"error": "No hay imágenes base disponibles en el servidor. Por favor, añada imágenes a la carpeta 'static/media/images' y actualice PREDEFINED_IMAGES en app.py."}, 500)
            return jsonify({"error": "No se pudieron seleccionar imágenes. Intenta un prompt diferente o verifica los archivos de imagen."}, 500)

        # 2. Seleccionar música aleatoria
        selected_music_path = select_random_music()
        if not selected_music_path and any(os.path.exists(m["path"]) for m in PREDEFINED_MUSIC):
            print("Advertencia: No se pudo seleccionar una pista de música válida, pero hay archivos de música. El video se generará sin audio.")
        elif not any(os.path.exists(m["path"]) for m in PREDEFINED_MUSIC):
            print("Advertencia: No hay archivos de música disponibles en 'static/media/music'. El video se generará sin audio.")


        # 3. Generar nombre de archivo único para el video
        output_filename = f"video_{uuid.uuid4()}.mp4"
        
        # 4. Generar el video usando FFmpeg
        # Esta llamada es síncrona y puede tardar. Para producción, usarías una cola de tareas.
        generated_video_path = generate_video_ffmpeg(selected_image_paths, selected_music_path, output_filename)
        
        # 5. Devolver la URL del video generado
        # La URL debe ser accesible desde el frontend (usando url_for para la carpeta static)
        video_url = url_for('static', filename=f'videos/{output_filename}', _external=True)
        
        return jsonify({"video_url": video_url})

    except ValueError as ve: # Errores específicos de validación (ej. no imágenes)
        app.logger.error(f"ValueError: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Error al generar video: {str(e)}")
        # En un caso real, podrías querer ocultar detalles internos del error al cliente
        return jsonify({"error": f"Ocurrió un error en el servidor: {str(e)}"}), 500


if __name__ == '__main__':
    # Verificar si FFmpeg está instalado y accesible
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, text=True)
        print("FFmpeg encontrado.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: FFmpeg no parece estar instalado o no está en el PATH del sistema.")
        print("Por favor, instala FFmpeg y asegúrate de que sea accesible desde la línea de comandos.")
        exit(1) # Salir si FFmpeg no está disponible

    # Verificar si hay al menos una imagen y una pista de música para que el MVP funcione mínimamente
    if not any(os.path.exists(img["path"]) for img in PREDEFINED_IMAGES):
        print("ADVERTENCIA: No se encontraron archivos de imagen en 'static/media/images/' según PREDEFINED_IMAGES.")
        print("El generador de video podría no funcionar correctamente. Por favor, crea los archivos y carpetas necesarios.")
    
    if not any(os.path.exists(m["path"]) for m in PREDEFINED_MUSIC):
         print("ADVERTENCIA: No se encontraron archivos de música en 'static/media/music/' según PREDEFINED_MUSIC.")
         print("Los videos se generarán sin música. Por favor, crea los archivos y carpetas necesarios si deseas audio.")

    app.run(debug=True, host='0.0.0.0', port=5000)
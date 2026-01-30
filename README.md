# Detector de Transacciones (Imagen a Excel)

Este proyecto es una aplicación web construida con Python y Streamlit que permite extraer tablas de transacciones bancarias (formato matriz de puntos) desde imágenes y convertirlas a Excel.

## Estructura del Proyecto

- `app.py`: La aplicación principal de Streamlit.
- `ocr_engine.py`: Lógica de extracción de texto (OCR) y procesamiento de datos.
- `requirements.txt`: Librerías de Python necesarias.
- `packages.txt`: Dependencias del sistema (Tesseract OCR) para Render.
- `render.yaml`: Configuración para despliegue automático en Render.

## Instalación Local

### Prerrequisitos
1. **Python 3.9+**
2. **Tesseract OCR (Importante)**:
   - Debes instalar Tesseract OCR en tu sistema.
   - **Windows**: Descarga el instalador [aquí](https://github.com/UB-Mannheim/tesseract/wiki). Asegúrate de agregar la ruta de instalación a tus variables de entorno PATH.
   - **Mac**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

### Pasos
1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```

## Despliegue en Render (Gratis)

Este proyecto está listo para desplegarse en [Render](https://render.com).

1. **GitHub**: Sube este código a un nuevo repositorio (público o privado) en GitHub. Asegúrate de incluir todos los archivos (`app.py`, `ocr_engine.py`, `requirements.txt`, `packages.txt`, `render.yaml`).
2. **Render**:
   - Crea una cuenta en Render.
   - Ve a "Blueprints" y selecciona "New Blueprint Instance".
   - Conecta tu repositorio de GitHub.
   - Render detectará el archivo `render.yaml` y configurará todo automáticamente.
   - Haz clic en "Apply".
3. **¡Listo!**: En unos minutos, tu aplicación estará en línea y lista para usar.

## Notas Importantes
- La calidad de la extracción depende de la calidad de la imagen. Imágenes borrosas o con mala iluminación pueden fallar.
- El formato esperado es específico (Fecha | Descripción | Monto | Documento). Otros formatos pueden requerir ajustes en el código (`ocr_engine.py`).

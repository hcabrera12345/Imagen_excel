# Detector de Transacciones (Imagen a Excel)

Este proyecto es una aplicación web construida con Python y Streamlit que permite extraer tablas de transacciones bancarias (formato matriz de puntos) desde imágenes y convertirlas a Excel.

## Estructura del Proyecto

- `app.py`: La aplicación principal de Streamlit.
- `ocr_engine.py`: Lógica de extracción de texto (OCR) y procesamiento de datos.
- `requirements.txt`: Librerías de Python necesarias.
- `packages.txt`: Dependencias del sistema (Tesseract OCR) para Streamlit Cloud.

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

## Despliegue en Streamlit Community Cloud (Gratis)

Este proyecto está listo para desplegarse en [Streamlit Cloud](https://streamlit.io/cloud).

1. **GitHub**: Sube este código a GitHub (ya lo has hecho).
2. **Streamlit Cloud**:
   - Ve a [share.streamlit.io](https://share.streamlit.io/).
   - Haz clic en "New app".
   - Selecciona tu repositorio (`Imagen_excel`) y la rama (`main`).
   - Selecciona `app.py` como el archivo principal.
   - Haz clic en **Deploy**.
   
**Importante**: Streamlit Cloud leerá automáticamente el archivo `packages.txt` e instalará Tesseract por ti.

## Notas Importantes
- La calidad de la extracción depende de la calidad de la imagen.

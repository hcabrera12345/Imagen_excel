import streamlit as st
import pandas as pd
from ocr_engine import process_image
import io

st.set_page_config(page_title="Extractor de Transacciones", layout="wide")

st.title("Extractor de Datos: Imagen a Excel")
st.markdown("""
Sube una imagen del reporte de transacciones (formato de matriz de puntos) para extraer los datos a Excel.
Las columnas extraídas serán: **FECHA, DESCRIPCION, MONTO, DOCUMENTO**.
""")

uploaded_file = st.file_uploader("Subir Imagen", type=["png", "jpg", "jpeg", "bmp"])

if uploaded_file is not None:
    # Display image
    st.image(uploaded_file, caption='Imagen Subida', use_column_width=True)
    
    st.write("Procesando imagen...")
    
    try:
        # Read file as bytes
        image_bytes = uploaded_file.read()
        
        # Process
        df = process_image(image_bytes)
        
        if not df.empty:
            st.success("¡Datos extraídos con éxito!")
            
            # Show data
            st.dataframe(df, use_container_width=True)
            
            # Convert to Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Transacciones')
            excel_data = output.getvalue()
            
            st.download_button(
                label="📥 Descargar Excel",
                data=excel_data,
                file_name="transacciones_extraidas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No se encontraron transacciones en la imagen. Asegúrate de que la imagen sea clara y tenga el formato correcto.")
            
    except Exception as e:
        st.error(f"Ocurrió un error al procesar la imagen: {e}")
        st.info("Nota: Si estás ejecutando esto localmente, asegúrate de tener Tesseract OCR instalado y en tu PATH.")

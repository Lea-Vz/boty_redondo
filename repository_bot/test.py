import streamlit as st
import os

st.title("🔍 PRUEBA DE IMÁGENES")

# Mostrar el directorio actual
st.write("Directorio actual:", os.getcwd())
st.write("Archivos en directorio:", os.listdir("."))

# Verificar si existe la carpeta images
if os.path.exists("images"):
    st.success("✅ La carpeta 'images' SÍ existe")
    st.write("Contenido de 'images/':", os.listdir("images"))
    
    # Intentar cargar una imagen
    try:
        st.image("images/Uno_page-0001.jpg", caption="Imagen de prueba", width=300)
        st.success("✅ Imagen cargada CORRECTAMENTE")
    except Exception as e:
        st.error(f"❌ Error al cargar imagen: {e}")
else:
    st.error("❌ La carpeta 'images' NO existe")

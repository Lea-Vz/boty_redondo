import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
import supabase
from datetime import datetime
import base64
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Bot Redonditos",
    page_icon="🎵",
    layout="centered"
)

# Inicializar session_state para mantener el estado
if 'puntaje' not in st.session_state:
    st.session_state.puntaje = 0
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}
if 'etapa' not in st.session_state:
    st.session_state.etapa = "bienvenida"
if 'juego_completado' not in st.session_state:
    st.session_state.juego_completado = False

# FUNCIÓN PARA GUARDAR EN SUPABASE
def guardar_en_supabase():
    try:
        supabase_client = supabase.create_client(
            st.secrets["supabase"]["url"],
            st.secrets["supabase"]["key"]
        )
        
        data = {
            "nombre": st.session_state.get('nombre', 'Anónimo'),
            "edad": st.session_state.get('edad', 0),
            "localidad": st.session_state.get('ciudad', ''),
            "puntaje_total": st.session_state.puntaje,
            "respuestas": st.session_state.respuestas,
            "fecha_creacion": datetime.now().isoformat()
        }
        
        response = supabase_client.table("resultados_bot").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Error al guardar: {e}")
        return False

# FUNCIÓN PARA MOSTRAR IMÁGENES (Pregunta 5)
def mostrar_imagenes_pregunta5():
    st.markdown("### 🎨 Mira bien las 4 imágenes")
    st.info("**¿Qué disco tiene mal puesto el título?**")
    
    # Crear columnas para las imágenes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.image("images/Uno_page-0001.jpg", caption="1. Momo Sampler", use_column_width=True)
    with col2:
        st.image("images/Dos_page-0001.jpg", caption="2. Bang! Bang! Estás liquidado", use_column_width=True)
    with col3:
        st.image("images/Tres_page-0001.jpg", caption="3. Luzbelito", use_column_width=True)
    with col4:
        st.image("images/Cuatro_page-0001.jpg", caption="4. Honolulú", use_column_width=True)

# PANTALLA DE BIENVENIDA
if st.session_state.etapa == "bienvenida":
    st.markdown("""
    <style>
    .bienvenida {
        background-color: black;
        color: yellow;
        padding: 20px;
        border-radius: 10px;
        font-family: Helvetica, Arial, sans-serif;
        font-weight: bold;
    }
    .violeta { color: blueviolet; }
    .verde { color: lightgreen; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='bienvenida'>
    <h2>¡Bienvenid@!</h2>
    <p>Este Bot corresponde a un trabajo final para la materia Elementos de Programación.</p>
    <p class='violeta'>Profesores Juliana Reves, Diego Pacheco</p>
    <p>Aquí se muestra lo aprendido durante la cursada.</p>
    <p>La temática elegida y el desarrollo es con fines de muestra del funcionamiento.</p>
    <p>Hecha esta aclaración, ¡vamos!</p>
    <br>
    <p class='verde'>Toca el botón para comenzar</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎵 Comenzar"):
        st.session_state.etapa = "datos_personales"
        st.rerun()

# DATOS PERSONALES
elif st.session_state.etapa == "datos_personales":
    st.title("📝 Datos Personales")
    
    st.session_state.nombre = st.text_input("¿Cómo te llamás?").strip().title()
    st.session_state.edad = st.number_input("¿Qué edad tenés?", min_value=16, max_value=110, step=1)
    st.session_state.ciudad = st.text_input("¿En qué localidad vivís?").strip().title()
    
    if st.session_state.nombre and st.session_state.ciudad and st.session_state.edad:
        if st.button("Continuar al cuestionario"):
            st.session_state.etapa = "pregunta_musica"
            st.rerun()

# PREGUNTA INICIAL SOBRE MÚSICA
elif st.session_state.etapa == "pregunta_musica":
    st.title("🎸 Cuestionario Redonditos")
    
    st.write(f"Hola, {st.session_state.nombre}!")
    
    musica = st.radio(
        "¿Te gusta la música de Patricio Rey y sus Redonditos de Ricota?",
        ["1. Sí", "2. No"]
    )
    
    if st.button("Continuar"):
        st.session_state.respuestas["gusto_musica"] = musica[0]
        
        if "1. Sí" in musica:
            st.session_state.etapa = "pregunta_1"
            st.rerun()
        else:
            st.session_state.etapa = "despedida_no"
            st.rerun()

# PREGUNTA 1
elif st.session_state.etapa == "pregunta_1":
    st.title("❓ Pregunta 1/10")
    st.write("**¿En qué ciudad surge la banda?**")
    
    opciones = [
        "1. Las Toninas", "2. Loma Hermosa", "3. Ciudad Oculta", 
        "4. La Plata", "5. San Isidro", "6. Ciudad Evita", 
        "7. La Paternal", "8. Ninguna de las anteriores"
    ]
    
    respuesta = st.radio("Selecciona tu respuesta:", opciones)
    
    if st.button("Responder"):
        st.session_state.respuestas["pregunta_1"] = respuesta[0]
        
        if respuesta[0] == "4":
            st.session_state.puntaje += 10
            st.success("✅ Respuesta correcta, sumaste 10 puntos redondos")
        else:
            st.error("❌ Respuesta incorrecta, continuemos")
            
        st.session_state.etapa = "pregunta_2"
        st.rerun()

# PREGUNTA 2
elif st.session_state.etapa == "pregunta_2":
    st.title("❓ Pregunta 2/10")
    st.write("**¿Quienes conforman el famoso Trinomio con el cual se identifica la dirección artística de la banda?**")
    
    opciones = [
        "1. Indio, Mario Pergollini, Mercedes Sosa",
        "2. Indio, Skay, Monona", 
        "3. Indio, Skay, Semilla Bucarelli",
        "4. Indio, Skay, Tito Fargo",
        "5. Indio, Skay, Tito Cossa",
        "6. Indio, Skay, Negra Poly",
        "7. Indio, Skay, Lionel Messi", 
        "8. Indio, Skay, Sergio Dawi"
    ]
    
    respuesta = st.radio("Selecciona tu respuesta:", opciones)
    
    if st.button("Responder"):
        st.session_state.respuestas["pregunta_2"] = respuesta[0]
        
        if respuesta[0] == "6":
            st.session_state.puntaje += 10
            st.success("✅ Respuesta correcta, sumaste 10 puntos redondos")
        elif respuesta[0] == "3" or respuesta[0] == "8":
            st.session_state.puntaje += 5
            st.warning("⚠️ Respuesta parcialmente correcta, suma 5 puntos redondos")
        else:
            st.error("❌ Respuesta incorrecta, continuemos")
            
        st.session_state.etapa = "pregunta_3"
        st.rerun()

# PREGUNTA 3
elif st.session_state.etapa == "pregunta_3":
    st.title("❓ Pregunta 3/10")
    st.write("**¿La canción Me Matan Limón, a quién está dedicada?**")
    
    opciones = [
        "1. Chapo Guzman",
        "2. Julio Rodriguez Granthon", 
        "3. Marcos y Ruti",
        "4. Limón Garcia",
        "5. Litto Nebbia",
        "6. Ismael Zambada Garcia", 
        "7. Pablo Escobar",
        "8. Rene Higuita"
    ]
    
    respuesta = st.radio("Selecciona tu respuesta:", opciones)
    
    if st.button("Responder"):
        st.session_state.respuestas["pregunta_3"] = respuesta[0]
        
        if respuesta[0] == "7":
            st.session_state.puntaje += 10
            st.success("✅ Respuesta correcta, sumaste 10 puntos redondos")
        elif respuesta[0] == "4":
            st.session_state.puntaje += 5
            st.warning("⚠️ Respuesta parcialmente correcta, suma 5 puntos redondos")
        else:
            st.error("❌ Respuesta incorrecta, continuemos")
            
        st.session_state.etapa = "pregunta_4"
        st.rerun()

# PREGUNTA 4
elif st.session_state.etapa == "pregunta_4":
    st.title("❓ Pregunta 4/10")
    st.write("**La canción Tarea Fina, según los rumores más fuertes de sus seguidores, a quién está dedicada?**")
    
    opciones = [
        "1. Karina Rabollini",
        "2. Fabiana Cantillo", 
        "3. Mirtha Legrand",
        "4. Debora Dixon", 
        "5. Daniel Scioli",
        "6. Cecilia Carrizo", 
        "7. Aracelli Gonzalez",
        "8. Elisa Carrio"
    ]
    
    respuesta = st.radio("Selecciona tu respuesta:", opciones)
    
    if st.button("Responder"):
        st.session_state.respuestas["pregunta_4"] = respuesta[0]
        
        if respuesta[0] == "1":
            st.session_state.puntaje += 10
            st.success("✅ Respuesta correcta, sumaste 10 puntos redondos")
        elif respuesta[0] == "4":
            st.session_state.puntaje += 5
            st.warning("⚠️ Respuesta parcialmente correcta, suma 5 puntos redondos")
        elif respuesta[0] == "3":
            st.error("❌ Tu respuesta es preocupante. Anda pensando en buscar otro múltiple choice")
        else:
            st.error("❌ Respuesta incorrecta, continuemos")
        
        # Verificar si debe ser excluido por puntaje 0
        if st.session_state.puntaje == 0:
            st.session_state.etapa = "exclusion"
            st.rerun()
        else:
            st.session_state.etapa = "pregunta_5"
            st.rerun()

# EXCLUSIÓN POR PUNTAJE 0
elif st.session_state.etapa == "exclusion":
    st.error("🚫 EXCLUSIÓN")
    st.write(f"Gracias por participar, {st.session_state.nombre}, pero no sumaste puntos. ¡Será la próxima!")
    
    st.markdown("""
    <div style='background-color: #2b2b2b; color: white; padding: 20px; border-radius: 10px; margin: 20px 0;'>
    <i>"Ahí está ese verso que dice, con lo que cuesta armar un full... 
    Significa, por un lado, que el amor no es sexo ni nada de eso. 
    Mas bien es el deseo de bien para el otro, algo que no le deseas a todo el mundo.
    Un día te encontras deseándoselo a alguien... y eso es amor"</i>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Finalizar"):
        guardar_en_supabase()
        st.session_state.juego_completado = True
        st.rerun()

# PREGUNTA 5 (CON IMÁGENES)
elif st.session_state.etapa == "pregunta_5":
    st.title("🎨 Pregunta 5/10")
    
    mostrar_imagenes_pregunta5()
    
    st.write("**Elegí la opción incorrecta:**")
    opciones = [
        "1. Momo Sampler",
        "2. Bang! Bang! Estás liquidado", 
        "3. Luzbelito",
        "4. Honolulú",
        "5. Están todos correctos"
    ]
    
    respuesta = st.radio("Selecciona tu respuesta:", opciones)
    
    if st.button("Responder"):
        st.session_state.respuestas["pregunta_5"] = respuesta[0]
        
        if respuesta[0] == "4":
            st.session_state.puntaje += 10
            st.success("✅ Respuesta correcta, sumaste 10 puntos redondos")
        else:
            st.error("❌ Respuesta incorrecta, continuemos")
            
        st.session_state.etapa = "pregunta_6"
        st.rerun()

# PREGUNTA 6
elif st.session_state.etapa == "pregunta_6":
    st.title("❓ Pregunta 6/10")
    
    st.write("""
    **...Sos el as del "Club París"**  
    **as lo tuyo no es el rock**  
    **cierran los bares por donde van**  
    **tu breto y tus ojos grises**  
    **...........................**
    """)
    
    st.write("**Por favor, elegí la estrofa que sigue:**")
    
    opciones = [
        "1. yo, no soy de mendigar... pero estas, pidiendo personal",
        "2. en este fin velado, en blanca noche, el hijo tenaz de tu enemigo", 
        "3. yo, no soy de aconsejar.. pero estas, jodiendo al personal",
        "4. Hoy tenés el mate lleno de infelices ilusiones Te engrupieron los otarios, las amigas, el gavión",
        "5. Viene a buscarme se come mis sobras, lo tengo encima parece mi sombra na na"
    ]
    
    respuesta = st.radio("Selecciona tu respuesta:", opciones)
    
    if st.button("Responder"):
        st.session_state.respuestas["pregunta_6"] = respuesta[0]
        
        if respuesta[0] == "3":
            st.session_state.puntaje += 10
            st.success("✅ Respuesta correcta, sumaste 10 puntos redondos")
        elif respuesta[0] == "1":
            st.session_state.puntaje += 5
            st.warning("⚠️ Respuesta parcialmente correcta, suma 5 puntos redondos")
        elif respuesta[0] == "5":
            st.session_state.puntaje += 5
            st.warning("⚠️ Respuesta incorrecta, pero como me gustó tu elección te doy 5 puntos")
        else:
            st.error("❌ Respuesta incorrecta, continuemos")
            
        st.session_state.etapa = "pregunta_7"
        st.rerun()

# PREGUNTA 7
elif st.session_state.etapa == "pregunta_7":
    st.title("❓ Pregunta 7/10")
    st.write("**Ahora responde por SI o por NO por lo correcto: En el tema Cruz Diablo! 'El tipo maduro pronto'**")
    
    opciones = ["1. Sí", "2. No", "3. Tal vez"]
    
    respuesta = st.radio("Selecciona tu respuesta:", opciones)
    
    if st.button("Responder"):
        st.session_state.respuestas["pregunta_7"] = respuesta[0]
        
        if respuesta[0] == "1":
            st.session_state.puntaje += 10
            st.success("✅ Respuesta correcta, sumaste 10 puntos redondos")
        elif respuesta[0] == "3":
            st.session_state.puntaje += 5
            st.warning("⚠️ Respuesta incierta, te doy 5 puntos por tu picardía")
        else:
            st.error("❌ Respuesta incorrecta, continuemos")
            
        st.session_state.etapa = "pregunta_8"
        st.rerun()

# PREGUNTA 8
elif st.session_state.etapa == "pregunta_8":
    st.title("❓ Pregunta 8/10")
    st.write("**Se dice que la canción 'La Bestia Pop' del disco Gulp! está dedicada al jefe de una barra brava de un equipo de fútbol, ¿sabes a quién?**")
    
    opciones = [
        "1. La Nancy- La N°XX Banfield",
        "2. El Carpincho- La N°XX, Atlético de Tucumán", 
        "3. El Negro José Luis- La N°22, Gimnasia de la Plata",
        "4. Cara de Paty- La N°1, Racing Club", 
        "5. Sandokan Evangelista- La N°XX San Lorenzo De Almagro",
        "6. El Abuelo- La N°12, Boca Juniors"
    ]
    
    respuesta = st.radio("Selecciona tu respuesta:", opciones)
    
    if st.button("Responder"):
        st.session_state.respuestas["pregunta_8"] = respuesta[0]
        
        if respuesta[0] == "3":
            st.session_state.puntaje += 10
            st.success("✅ Respuesta correcta, sumaste 10 puntos redondos")
        elif respuesta[0] >= "4":
            st.session_state.puntaje += 5
            st.warning("⚠️ Respuesta incorrecta, pero te doy 5 puntos por ser consigna de interpretación")
        else:
            st.error("❌ Respuesta incorrecta y poco intuitiva, continuemos")
            
        st.session_state.etapa = "pregunta_9"
        st.rerun()

# PREGUNTA 9
elif st.session_state.etapa == "pregunta_9":
    st.title("❓ Pregunta 9/10")
    st.write("**En el año 1992 la banda saca un disco llamado 'En directo', en la lista de temas hay solo uno que es considerado de los inéditos. Elegí cuál es:**")
    
    opciones = [
        "1. Vamos las bandas",
        "2. Barbazul versus el amor letal", 
        "3. Criminal mambo",
        "4. Yo no me caí del cielo", 
        "5. El blues del noticiero",
        "6. Todo un palo"
    ]
    
    respuesta = st.radio("Selecciona tu respuesta:", opciones)
    
    if st.button("Responder"):
        st.session_state.respuestas["pregunta_9"] = respuesta[0]
        
        if respuesta[0] == "5":
            st.session_state.puntaje += 10
            st.success("✅ Respuesta correcta, sumaste 10 puntos redondos")
        elif respuesta[0] == "2":
            st.session_state.puntaje += 5
            st.warning("⚠️ Respuesta parcialmente correcta, el tema es una reversión por ello te doy 5 puntos")
        else:
            st.error("❌ Respuesta incorrecta, continuemos a la última pregunta")
            
        st.session_state.etapa = "pregunta_10"
        st.rerun()

# PREGUNTA 10
elif st.session_state.etapa == "pregunta_10":
    st.title("🎯 Pregunta 10/10")
    st.write("""
    **Luego de un recital con graves incidentes, algunos periodistas interceptaron al Indio Solari para preguntarle por los hechos, a lo cual este deslizó:**
    **¿Vos pensás que los pibes nacen malos?** 
    """)
    st.write("**Elegí luego de qué recital surgió esta frase:**")
    
    opciones = [
        "1. Estadio River Plate Nuñez (2000)",
        "2. Patinódromo de Mar Del Plata (1999)", 
        "3. Estadio Racing Club de Avellaneda (1998)",
        "4. Club Estudiantes de Olavarría (1997)", 
        "5. Estadio Huracán Parque Patricios (1993)"
    ]
    
    respuesta = st.radio("Selecciona tu respuesta:", opciones)
    
    if st.button("Responder y ver resultados finales"):
        st.session_state.respuestas["pregunta_10"] = respuesta[0]
        
        if respuesta[0] == "2":
            st.session_state.puntaje += 10
            st.success("✅ Respuesta correcta, sumaste 10 puntos redondos. Esta era difícil, muy rebuscada.")
        else:
            st.session_state.puntaje += 5
            st.warning("⚠️ Respuesta incorrecta. Te damos 5 puntos por haber llegado hasta acá")
            
        st.session_state.etapa = "resultado_final"
        st.rerun()

# RESULTADO FINAL
elif st.session_state.etapa == "resultado_final":
    st.title("🎉 Resultado Final")
    
    # Mostrar mensaje según puntaje
    if st.session_state.puntaje == 100:
        st.success(f"🎊 ¡TE FELICITO {st.session_state.nombre.upper()}! 🎊")
        st.success("Sacaste 100 puntos sobre 100. ¡Tu corazón es 100% redondo!")
    elif 70 <= st.session_state.puntaje <= 99:
        st.info(f"🎸 ¡MUY BIEN {st.session_state.nombre}! 🎸")
        st.info(f"Sacaste {st.session_state.puntaje} puntos. ¡Gran conocimiento de la banda!")
    elif 30 <= st.session_state.puntaje < 70:
        st.warning(f"🤔 REGULAR {st.session_state.nombre}...")
        st.warning(f"Sacaste {st.session_state.puntaje} puntos. Podría ser mejor, pero gracias por el recorrido.")
    elif 5 <= st.session_state.puntaje < 30:
        st.error(f"😬 MAL {st.session_state.nombre}...")
        st.error(f"Sacaste {st.session_state.puntaje} puntos. Volvé a {st.session_state.ciudad} y pensá en lo que hiciste.")
    else:
        st.error(f"🚫 {st.session_state.nombre}, NO SUMASTE PUNTOS")
        st.error("Gracias por participar, ¡será la próxima!")
    
    st.write(f"**Puntaje final:** {st.session_state.puntaje}/100")
    
    # Frase final
    st.markdown("""
    <div style='background-color: #2b2b2b; color: white; padding: 20px; border-radius: 10px; margin: 20px 0;'>
    <i>"Ahí está ese verso que dice, con lo que cuesta armar un full... 
    Significa, por un lado, que el amor no es sexo ni nada de eso. 
    Mas bien es el deseo de bien para el otro, algo que no le deseas a todo el mundo.
    Un día te encontras deseándoselo a alguien... y eso es amor"</i>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💾 Guardar resultados en base de datos"):
        if guardar_en_supabase():
            st.success("✅ Resultados guardados correctamente!")
            st.session_state.juego_completado = True
    
    if st.button("🔄 Jugar de nuevo"):
        # Reiniciar todo
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# DESPEDIDA PARA QUIEN NO LE GUSTA LA BANDA
elif st.session_state.etapa == "despedida_no":
    st.error(f"Que lástima tu respuesta {st.session_state.nombre} de {st.session_state.ciudad}")
    st.write("Te pido si me recomendás otra persona. Te dejamos esta frase del cantante:")
    
    st.markdown("""
    <div style='background-color: brown; color: lightgray; padding: 20px; border-radius: 10px;'>
    <i>"Ahí está ese verso que dice, con lo que cuesta armar un full... 
    Significa, por un lado, que el amor no es sexo ni nada de eso. 
    Mas bien es el deseo de bien para el otro, algo que no le deseas a todo el mundo.
    Un día te encontras deseándoselo a alguien... y eso es amor"</i>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Finalizar"):
        guardar_en_supabase()
        st.session_state.juego_completado = True
        st.rerun()

# JUEGO COMPLETADO
if st.session_state.get('juego_completado'):
    st.sidebar.success("🎉 Juego completado!")
    st.sidebar.write(f"**Jugador:** {st.session_state.get('nombre', 'Anónimo')}")
    st.sidebar.write(f"**Puntaje:** {st.session_state.puntaje}")
    
    if st.sidebar.button("🎮 Nuevo juego"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

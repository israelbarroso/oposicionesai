import smtplib
from email.mime.text import MIMEText
from email.header import Header
import streamlit as st
from openai import OpenAI

# --- CORRECCIÓN AQUÍ: Eliminamos 'with col_text' y ponemos el título directo ---
# Como borraste las columnas del logo, ya no necesitamos meter el título en una columna.
# El CSS .main-header ya se encarga de centrarlo.

# --- CONFIGURACIÓN DE LA PÁGINA (Debe ir al principio) ---
st.set_page_config(
    page_title="Oposiciones.ai | Tu Orientador Inteligente",
    page_icon="🤖",
    layout="centered"
)

st.markdown('<div class="main-header">oposiciones.ai</div>', unsafe_allow_html=True)

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    /* Importar fuente moderna de Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Estilo del botón principal */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        border: none;
        border-radius: 12px;
        height: 3.5em;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(124, 58, 237, 0.39);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(124, 58, 237, 0.23);
    }

    /* Títulos */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(left, #1E293B, #4F46E5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2.5rem;
        line-height: 1.6;
    }

    /* Inputs y Selects */
    .stSelectbox > div > div {
        background-color: #F8FAFC;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    
    /* Card de resultado (usar con markdown HTML) */
    .result-card {
        background-color: white;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-top: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Verificación y Carga de API Key ---
try:
    # Intenta leer la clave del archivo secrets.toml o del entorno de Streamlit Cloud
    openai_key = st.secrets["openai"]["api_key"]
    client = OpenAI(api_key=openai_key)
except KeyError:
    # Mensaje de error si la clave no se encuentra (para desarrollo local)
    st.error(
        "❌ ERROR: La clave de OpenAI no se ha encontrado en el archivo secrets.toml. "
        "Asegúrate de que el archivo existe en la carpeta .streamlit/ y contiene [openai] y api_key."
    )
    st.stop()
except Exception as e:
    st.error(f"❌ ERROR al inicializar la API: {e}")
    st.stop()

# --- INTERFAZ PRINCIPAL ---
st.markdown('<div class="sub-header">Descubre tu plaza ideal en la Administración Pública en segundos con Inteligencia Artificial.</div>', unsafe_allow_html=True)

st.write("---")

# --- FORMULARIO DE PERFIL ---
col1, col2 = st.columns(2)

with col1:
    nivel_estudios = st.selectbox(
        "🎓 Tu nivel de estudios",
        ["Grado Universitario / Licenciatura", "Diplomatura / Ingeniería Técnica", "Bachillerato", "ESO"]
    )
    rama = st.selectbox(
        "🧠 Tu rama o especialidad",
        ["Informática / Telecomunicaciones / STEM", "Derecho / Jurídico", "Económicas / ADE", "Sanidad", "Magisterio", "Otras / General"]
    )

with col2:
    disponibilidad = st.selectbox(
        "⏳ Disponibilidad para estudiar",
        ["Tiempo completo (Dedicación exclusiva)", "Trabajo y estudio (Dedicación parcial)", "Poco tiempo (Solo fines de semana)"]
    )
    prioridad = st.selectbox(
        "🎯 ¿Qué priorizas?",
        ["Salario alto y carrera profesional", "Estabilidad y examen sencillo", "Rapidez en aprobar", "Teletrabajo y conciliación"]
    )

# --- CAPTURA DE LEAD (El paso clave) ---
email = st.text_input("📩 Recibe tu Hoja de Ruta Personalizada + Guía de Salarios 2025 en tu email", placeholder="ejemplo@correo.com")

# Modificación de la función send_email (quita el try/except interno)
def send_email(receiver_email, subject, body):
    # Cargar credenciales y configuración SMTP desde secrets.toml
    smtp_username = st.secrets["smtp"]["username"]
    smtp_password = st.secrets["smtp"]["password"]
    smtp_host = st.secrets["smtp"]["host"]  # send.one.com
    smtp_port = st.secrets["smtp"]["port"]  # 587
    
    # Configurar el mensaje
    msg = MIMEText(body, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = smtp_username
    msg['To'] = receiver_email
    
    # Conexión al servidor SMTP de One.com
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls() 
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, receiver_email, msg.as_string())
    
    return True # Solo se llega aquí si todo fue bien

# --- LÓGICA DEL BOTÓN ---
if st.button("✨ Analizar mi Perfil con IA"):
    if not email:
        st.warning("⚠️ Por favor, introduce tu email para continuar.")
    else:
        # Prompt con "System Injection" para favorecer tu academia si encaja
        prompt_sistema = """
        Eres un experto orientador de empleo público en España. Tu trabajo es recomendar las mejores oposiciones según el perfil.
        
        REGLAS CRÍTICAS DE NEGOCIO:
        1. Si el usuario tiene perfil técnico (Informática/STEM) y titulación universitaria, DEBES recomendar SIEMPRE 'Cuerpo Superior de Sistemas y Tecnologías (TIC A1)' o 'Gestión de Sistemas (TIC A2)'. Véndelo como la mejor opción por salario, teletrabajo y ratio de aprobados.
        2. Si es otro perfil, recomienda las opciones estándar (Administrativo, Justicia, Hacienda) más adecuadas.
        3. Sé conciso, motivador y usa formato Markdown con negritas.
        4. No inventes datos falsos.
        """

        prompt_usuario = f"""
        Mi perfil es:
        - Estudios: {nivel_estudios}
        - Rama: {rama}
        - Disponibilidad: {disponibilidad}
        - Prioridad: {prioridad}
        
        Recomiéndame las 3 mejores opciones. Para la opción nº1 dame un detalle mayor (salario, dificultad, tipo de examen).
        """

        with st.spinner("La IA está analizando miles de convocatorias..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini", # Modelo rápido y barato
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": prompt_usuario}
                    ],
                    temperature=0.7
                )
                resultado = response.choices[0].message.content
                
                # --- RESULTADO ---
                st.success("¡Análisis completado!")
                st.markdown("### 📋 Tu Hoja de Ruta Personalizada")
                st.markdown(f'<div class="result-card">{resultado}</div>', unsafe_allow_html=True)
                

                st.write("---")
                
                # --- LÓGICA DE ENVÍO DE EMAIL ---
                
                # 1. Preparar el cuerpo del email (usando HTML básico)
                email_body = f"""
                <html>
                    <body>
                        <p>Estimado/a opositor/a,</p>
                        <p>Aquí tienes tu informe de orientación personalizado:</p>
                        <hr>
                        {resultado.replace('\n', '<br>')}
                        <hr>
                        <p>¡Mucho éxito en tu preparación!</p>
                        <p>El equipo de Oposiciones.ai</p>
                    </body>
                </html>
                """
                
                # 2. Llamada a la función de envío envuelta en try/except
                try:
                    send_email(email, "✅ Tu Informe de Oposiciones Personalizado (Oposiciones.ai)", email_body)
                    st.success(f"📧 ¡Informe enviado a {email}! Revisa tu bandeja de entrada o spam.")
                except Exception as e:
                    st.error("❌ ERROR AL ENVIAR CORREO: Fallo en la conexión SMTP. Revisa host/puerto y credenciales.")
                    st.code(f"Detalles del Error: {e}", language="text")

                # ----------------------------------------------------
                
                # --- NUEVO: CAPTURA DE LEAD TIC ---
                # Verificamos si el perfil es TIC
                if "Informática" in rama or "STEM" in rama:
                    
                    # Preparamos los datos para TI
                    asunto_interno = f"🔔 NUEVO LEAD TIC: {email}"
                    cuerpo_interno = f"""
                    <html>
                        <body>
                            <h2>Nuevo aspirante TIC detectado</h2>
                            <ul>
                                <li><strong>Email:</strong> {email}</li>
                                <li><strong>Nivel:</strong> {nivel_estudios}</li>
                                <li><strong>Rama:</strong> {rama}</li>
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import streamlit as st
from openai import OpenAI

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Oposiciones.ai | Tu Orientador Inteligente",
    page_icon="🤖",
    layout="centered"
)

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E293B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
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


# --- SIDEBAR (Aviso legal y branding) ---
# with st.sidebar:
#    st.header("⚙️ Configuración")
#    st.info("La API Key se carga de forma segura desde el archivo 'secrets.toml'.")
#    st.write("---")
#    st.write("© 2024 Oposiciones.ai")

# --- INTERFAZ PRINCIPAL ---
st.markdown('<div class="main-header">oposiciones.ai</div>', unsafe_allow_html=True)
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
#st.write("###")
email = st.text_input("📧 Tu email para enviarte el informe detallado", placeholder="ejemplo@correo.com")
def send_email(receiver_email, subject, body):
    try:
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
        
        # Conexión al servidor SMTP de One.com (usando TLS/STARTTLS en el puerto 587)
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            # Poner la conexión en modo seguro TLS
            server.starttls() 
            # Iniciar sesión
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, receiver_email, msg.as_string())
        
        return True
    except Exception as e:
        # Esto te ayudará a diagnosticar si las credenciales o el host/puerto son incorrectos
        st.error(f"Error al enviar el correo desde one.com: {e}") 
        return False
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
                st.markdown(resultado)
                
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
                
                # 2. Llamar a la función de envío
                envio_exitoso = send_email(email, "✅ Tu Informe de Oposiciones Personalizado (Oposiciones.ai)", email_body)
                
                if envio_exitoso:
                    st.success(f"📧 ¡Informe enviado a {email}! Revisa tu bandeja de entrada o spam.")
                else:
                    # El mensaje de error detallado ya lo muestra la función send_email, 
                    # pero este catch asegura que el usuario lo vea.
                    st.warning("El análisis fue exitoso, pero **falló el envío del correo**. Revisa las credenciales SMTP en los 'Secrets' de Streamlit Cloud.")

                # ----------------------------------------------------
                
                st.write("---") # Aseguramos que la línea divisoria se muestra SÓLO después del envío/error
                
                # --- LÓGICA DE REDIRECCIÓN INTELIGENTE ---
                # Si el usuario es TIC (detectado por el input), mostramos TU ACADEMIA
                if "Informática" in rama or "STEM" in rama:
                    st.info("💡 **Consejo de experto:** Tienes el perfil perfecto para el Cuerpo TIC. Es la oposición con mejor ratio plaza/aspirante ahora mismo.")
                    # ¡Asegúrate de cambiar este enlace por el de tu academia!
                    st.link_button("🚀 Preparar TIC A1/A2 con Expertos", "https://itic.academy") 
                else:
                    # Si no es TIC, mostramos afiliados o generalistas
                    st.warning("📚 **Material recomendado:** Para estas oposiciones, necesitas un temario actualizado.")
                    col_af1, col_af2 = st.columns(2)
                    # ¡Asegúrate de cambiar estos enlaces por los de tus afiliados!
                    col_af1.link_button("🔍 Buscar Preparadores", "https://itic.academy")
                    col_af2.link_button("🛒 Ver Temarios Recomendados", "https://itic.academy")

            except Exception as e:
                st.error(f"Hubo un error con la IA. Esto puede ser por límites de uso o un error en la clave. Error: {e}")
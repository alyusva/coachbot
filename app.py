import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from tools.planner_tool import PlannerTool
from tools.injury_tool import InjuryTool
from tools.history_tool import HistoryTool
from tools.calendar_tool import CalendarTool
from tools.adaptive_planner_tool import AdaptivePlannerTool
from tools.history_tool import save_to_history, retrieve_history
from models.model_loader import load_model

# Cargar modelo LLM (usando Ollama o local)
llm = load_model()

# Definir herramientas personalizadas
tools = [
    PlannerTool,
    InjuryTool,
    HistoryTool,
    CalendarTool,
    AdaptivePlannerTool
]

# Definir prompt del sistema para el agente
system_prompt = """Eres CoachBot, un agente experto en diseñar y adaptar planes de entrenamiento para jugadores de fútbol.

Tienes acceso a las siguientes herramientas:
- PlannerTool: genera un plan general según la posición del jugador.
- InjuryTool: adapta o restringe ejercicios en función de molestias o lesiones.
- CalendarTool: ajusta la carga del entrenamiento según el calendario o fechas de partidos.
- HistoryTool: recupera recomendaciones previas y contexto de usuario.
- AdaptivePlannerTool: crea un plan personalizado combinando posición, lesión y calendario si están presentes.

🧠 Cómo decidir qué herramienta usar (usa solo una):
- Usa **AdaptivePlannerTool** si el input menciona al menos dos de los siguientes: posición, lesión o calendario. Si es así, esta herramienta es prioritaria.
- Usa **PlannerTool** solo si se menciona la posición y no hay ni calendario ni lesión.
- Usa **InjuryTool** solo si se menciona una molestia o lesión y no hay mención de posición ni calendario.
- Usa **CalendarTool** si se menciona una fecha o proximidad de partido y no hay posición ni lesión.
- Usa **HistoryTool** si el usuario pide que le recuerdes recomendaciones anteriores.

⚠️ Nunca escribas el Action Input como `prompt="..."`. Usa solo texto plano.
Ejemplo correcto:
Action: PlannerTool
Action Input: "Soy extremo y quiero un plan semanal"

🚫 Si ya has usado **AdaptivePlannerTool**, no vuelvas a usar PlannerTool ni InjuryTool en el mismo input. Ya están integradas.
🚫 No repitas herramientas con el mismo input varias veces. Piensa si ya tienes la información necesaria o si puedes pasar a la respuesta final.

✅ Integra la información de las herramientas en una salida coherente, clara y sin repeticiones. Adapta el mensaje al rol y estado físico del jugador.

Si no puedes responder, di "No tengo suficiente información para ayudarte con eso" y no uses ninguna herramienta.

"""

# Crear prompt template para el agente
prompt_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Crear el agente
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True,
    agent_kwargs={"prompt": prompt_template}
)

# Interfaz de usuario con Streamlit
st.set_page_config(page_title="CoachBot", layout="centered")
st.title("🏋️ CoachBot - Tu planificador de entrenos")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.chat_input("¿En qué te puedo ayudar hoy con tu entrenamiento?")

if user_input:
    st.session_state.chat.append(("user", user_input))
    with st.spinner("Pensando..."):
        response = agent_executor.invoke({"input": user_input})["output"]
    st.session_state.chat.append(("bot", response))

    save_to_history({"user_input": user_input, "response": response})

for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

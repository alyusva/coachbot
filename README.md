# 🧠 CoachBot – Tu entrenador inteligente ⚽

**CoachBot** es un asistente virtual que genera planes de entrenamiento personalizados para futbolistas, adaptando las rutinas según **posición**, **lesiones** y **calendario competitivo**.

Usando el poder de 🦜 LangChain, LLMs (🔗 API de OpenAI o 🦙 modelos locales como LLaMA 3.1/3.2 vía Ollama) y 🖥️ Streamlit, CoachBot **razona como un entrenador** para decidir qué herramienta usar y ofrecer recomendaciones coherentes, útiles y adaptadas a tu contexto.

*Última versión emplea la API OpenAI con OPENAI_FUNCTIONS, dado que funciona mejor que Llama3.2 con STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION o ZERO_SHOT_REACT_DESCRIPTION*

---

## 🚀 ¿Qué puede hacer?

- 📋 **Generar planes semanales de entrenamiento** según la posición (portero, defensa, centrocampista, delantero…)
- 🩺 **Adaptar el plan a molestias o lesiones específicas** (rodilla, tobillo, isquios…)
- 📆 **Ajustar la carga de trabajo** en función de la cercanía del próximo partido
- 🧠 **Recordar tus recomendaciones anteriores** con historial cronológico y filtrado

---

## 🛠️ Tecnologías utilizadas

- [LangChain](https://github.com/langchain-ai/langchain) (Agente + Herramientas personalizadas)
- [Streamlit](https://streamlit.io) (Interfaz web conversacional)
- [OpenAI API](https://platform.openai.com/) o [Ollama](https://ollama.com) (modelo local como `llama3.2`)
- Python 3.13

---

## 🗂️ Estructura del proyecto

```bash
coachbot/
├── app.py                  # Interfaz principal de la app
├── tools/                 # Herramientas personalizadas
│   ├── planner_tool.py
│   ├── injury_tool.py
│   ├── calendar_tool.py
│   ├── history_tool.py
│   └── adaptive_planner_tool.py
├── models/                # Carga del modelo LLM
│   └── model_loader.py
├── requirements.txt
└── .gitignore
```

**🧪 Ejemplos de uso**
🗣️ Usuario: "Soy mediocentro y tengo partido en 3 días. ¿Qué me recomiendas?"
🤖 CoachBot: Genera un plan día a día con sesiones técnicas, físicas y tácticas adaptadas.

🗣️ Usuario: "Tengo molestias en el tobillo"
🤖 CoachBot: Evita sprints, sugiere ejercicios alternativos, e incluye movilidad en piscina.

🗣️ Usuario: "Recuérdame mis 2 últimas recomendaciones"
🤖 CoachBot: Muestra el historial reciente con formato claro y orden cronológico.



**👨‍💻 Autor**
Desarrollado por @alyusva @juaki0315 and @CR7AngelCR7 como MVP para explorar agentes LLM aplicados al deporte, específicamente al fútbol como Proyecto de la asignatura IA Generativa

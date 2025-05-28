# 🧠 CoachBot – Tu entrenador inteligente ⚽

**CoachBot** es un asistente inteligente que genera planes de entrenamiento personalizados para futbolistas, teniendo en cuenta su **posición**, **lesiones** y **calendario competitivo**.

Construido con ⚙️ **LangChain**, 💬 **LLMs locales (Ollama)** y 🎛️ **Streamlit**, CoachBot aplica razonamiento avanzado para decidir cuál de sus herramientas usar en cada caso y ofrecer recomendaciones realistas, útiles y adaptadas.

---

## 🚀 ¿Qué puede hacer?

- 🧠 **Generar planes semanales** de entrenamiento según el rol del jugador (portero, defensa, mediocentro, delantero)
- 🩺 **Adaptar el entrenamiento a lesiones o molestias físicas**
- 📆 **Ajustar la carga de trabajo** según la cercanía del próximo partido
- 🧾 **Recordar tus últimas recomendaciones**

---

## 🛠️ Tecnologías utilizadas

- [LangChain](https://www.langchain.com/) (agent + tools)
- [Streamlit](https://streamlit.io/) (interfaz web)
- [Ollama](https://ollama.com/) (modelo local llama3.2)
- Python 3.13

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
- "Soy defensa central y quiero un plan semanal para mejorar mi resistencia"
- "Juego en 4 días y tengo molestias en el tobillo, ¿qué me recomiendas?"
- "¿Qué plan me diste ayer?"
- "Soy portero y tengo partido en 3 días, adapta mi entreno según mi lesión en la rodilla"

**👨‍💻 Autor**
Desarrollado por @alyusva @juaki @como MVP para explorar agentes LLM aplicados al deporte, específicamente al fútbol.

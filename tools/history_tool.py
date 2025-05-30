import json
from datetime import datetime
from pathlib import Path

HISTORY_PATH = Path("history.json")

def save_to_history(entry: dict):
    """Guarda una nueva entrada en el historial."""
    history = []
    if HISTORY_PATH.exists():
        try:
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    entry["timestamp"] = datetime.now().isoformat()
    history.append(entry)

    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def retrieve_history(prompt: str = "") -> str:
    """Recupera el historial. Por defecto muestra las últimas 3 entradas."""
    if not HISTORY_PATH.exists():
        return "🗃️ No hay historial disponible."

    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)
    except json.JSONDecodeError:
        return "⚠️ Error leyendo el historial."

    if not history:
        return "🗃️ El historial está vacío."

    # Determinar cuántas entradas mostrar
    num_entries = 3
    for word in prompt.split():
        if word.isdigit():
            num_entries = int(word)
            break

    latest = history[-num_entries:]
    formatted = []
    for h in latest:
        ts = datetime.fromisoformat(h["timestamp"])
        fecha = ts.strftime("%d/%m/%Y %H:%M")
        formatted.append(f"📅 {fecha}\n📌 {h['user_input']}\n👉 {h['response']}\n")

    return "\n".join(formatted)


# LangChain Tool integration
from langchain.tools import Tool

HistoryTool = Tool(
    name="HistoryTool",
    func=retrieve_history,
    description=(
        "Permite consultar el historial de recomendaciones y planes de entrenamiento generados previamente para el usuario. "
        "Ideal para recordar sesiones pasadas, comparar progresos o retomar un plan anterior. "
        "Devuelve las últimas entradas del historial, incluyendo fecha, consulta y respuesta asociada.\n\n"
        "Ejemplo de uso: '¿Qué me recomendaste ayer?', 'Recuérdame el plan anterior', 'Muéstrame mis últimas 2 recomendaciones'.\n"
        "Ejemplo de respuesta:\n"
        "📅 29/05/2025 18:30\n"
        "📌 ¿Qué rutina hago si tengo molestias en el tobillo?\n"
        "👉 ⚠️ Molestia en el tobillo detectada: ...\n"
    )
)
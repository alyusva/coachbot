import json
import re
from datetime import datetime
from pathlib import Path
from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel

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
    """Recupera el historial. Muestra las últimas entradas (por defecto 3)."""
    if not HISTORY_PATH.exists():
        return "🗃️ No hay historial disponible."

    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)
    except json.JSONDecodeError:
        return "⚠️ Error leyendo el historial."

    if not history:
        return "🗃️ El historial está vacío."

    prompt_lower = prompt.lower()

    # Detectar si busca planes de entrenamiento
    wants_plan = any(word in prompt_lower for word in ["plan", "rutina", "entrenamiento"])

    # Número de entradas a mostrar
    num_entries = 3
    match = re.search(r"\b(\d+)\b", prompt_lower)
    if match:
        num_entries = int(match.group(1))
    elif "última" in prompt_lower or "último" in prompt_lower:
        num_entries = 1
    elif "dos" in prompt_lower:
        num_entries = 2
    elif "tres" in prompt_lower:
        num_entries = 3
    elif "cinco" in prompt_lower:
        num_entries = 5

    filtered = []
    seen = set()

    for h in reversed(history):
        key = (h.get("user_input", ""), h.get("response", ""))
        if key in seen:
            continue
        if wants_plan:
            if any(w in h.get("response", "").lower() for w in ["plan", "rutina", "viernes", "sábado", "domingo", "lunes"]):
                filtered.append(h)
                seen.add(key)
        else:
            filtered.append(h)
            seen.add(key)
        if len(filtered) >= num_entries:
            break

    if not filtered:
        return "⚠️ No se han encontrado recomendaciones anteriores que coincidan con tu búsqueda."

    output = ""
    for h in filtered:
        ts = datetime.fromisoformat(h["timestamp"])
        fecha = ts.strftime("%d/%m/%Y %H:%M")
        output += f"📅 {fecha}\n📌 {h['user_input']}\n👉 {h['response']}\n\n"

    return output.strip()

# LangChain Tool integration
class HistoryInput(BaseModel):
    prompt: str

HistoryTool = StructuredTool.from_function(
    func=retrieve_history,
    name="HistoryTool",
    description=(
        "Permite consultar el historial de recomendaciones previas. "
        "Devuelve las últimas entradas del historial incluyendo fecha, consulta y respuesta.\n"
        "Ejemplo: '¿Qué me recomendaste ayer?', 'Muéstrame mis últimas 2 recomendaciones', 'Últimos 3 planes de entrenamiento'."
    ),
    args_schema=HistoryInput,
    return_direct=True
)



#HistoryTool = StructuredTool.from_function(
#    func=retrieve_history,
#    name="HistoryTool",
#    description=(
#        "Permite consultar el historial de recomendaciones y planes de entrenamiento generados previamente para el usuario. "
#        "Ideal para recordar sesiones pasadas, comparar progresos o retomar un plan anterior. "
#        "Devuelve las últimas entradas del historial, incluyendo fecha, consulta y respuesta asociada.\n\n"
#        "Ejemplo de uso: '¿Qué me recomendaste ayer?', 'Recuérdame el plan anterior', 'Muéstrame mis últimas 2 recomendaciones'.\n"
#        "Ejemplo de respuesta:\n"
#        "📅 29/05/2025 18:30\n"
#        "📌 ¿Qué rutina hago si tengo molestias en el tobillo?\n"
#        "👉 ⚠️ Molestia en el tobillo detectada: ...\n"
#    ),
#    args_schema=HistoryInput,
#    return_direct=True
#)

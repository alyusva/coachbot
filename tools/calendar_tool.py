import re
from datetime import datetime, timedelta
import dateparser

from langchain.tools import StructuredTool
from pydantic import BaseModel  # actualizado a pydantic v2

def analyze_calendar(prompt: str) -> str:
    prompt = prompt.lower()
    hoy = datetime.now()

    # Primero intenta detectar explícitamente "juego en X días"
    match = re.search(r"juego en (\d+) días", prompt)
    if match:
        dias = int(match.group(1))
        fecha_partido = hoy + timedelta(days=dias)
    else:
        # Si no, intenta parsear usando dateparser
        fecha_partido = dateparser.parse(prompt, languages=["es"])

    if not fecha_partido:
        return (
            "⚠️ No se ha podido interpretar ninguna fecha. "
            "Intenta usar un formato como 'partido el 31 de mayo' o 'juego en 3 días'."
        )

    dias_restantes = (fecha_partido.date() - hoy.date()).days

    if dias_restantes < 0:
        return f"📆 El partido fue hace {abs(dias_restantes)} días. Prepara recuperación."

    if dias_restantes == 0:
        return (
            "📆 ¡El partido es hoy!\n"
            "- Enfócate en activación ligera, hidratación y mentalización táctica.\n"
            "- Evita cargas pesadas. Come ligero pero energético.\n"
            "- Visualiza tus acciones clave en el campo."
        )
    elif dias_restantes == 1:
        return (
            "📆 El partido es mañana.\n"
            "- Realiza una sesión muy ligera: movilidad + activación corta.\n"
            "- Cena rica en carbohidratos. Duerme bien.\n"
            "- Revisión táctica individual y colectiva."
        )
    elif dias_restantes <= 3:
        return (
            f"📆 El partido es en {dias_restantes} días.\n"
            "- Reduce carga progresivamente. Prioriza técnica y recuperación.\n"
            "- Simula jugadas específicas del rival.\n"
            "- Mantén buena nutrición y descanso."
        )
    elif dias_restantes <= 7:
        return (
            f"📆 Partido en {dias_restantes} días.\n"
            "- Semana equilibrada: fuerza, técnica, táctica.\n"
            "- Control de fatiga acumulada. Un día de descanso activo recomendado.\n"
            "- Mantén rutina y buen ritmo de sueño."
        )
    else:
        return (
            f"📆 Partido en {dias_restantes} días.\n"
            "- Etapa de construcción. Prioriza fuerza, resistencia y carga técnica alta.\n"
            "- Haz evaluaciones físicas y trabaja en tus debilidades.\n"
            "- Semana próxima comienza descarga progresiva."
        )


# Tool definition para LangChain
class CalendarInput(BaseModel):
    prompt: str

CalendarTool = StructuredTool.from_function(
    func=analyze_calendar,
    name="CalendarTool",
    description=(
        "Analiza la proximidad del próximo partido a partir de una fecha concreta o número de días indicado por el usuario, "
        "e interpreta frases como 'el 31 de mayo', 'mañana', 'en 3 días', etc. "
        "Su objetivo es recomendar el enfoque general de la semana (carga, recuperación, activación), "
        "pero **no genera rutinas ni ejercicios específicos**. "
        "Ideal para planificar la distribución de la carga y el descanso según la fecha del partido, "
        "sin tener en cuenta la posición ni detalles personalizados.\n\n"
        "Ejemplo de uso: '¿Cómo debería organizar mi semana si juego en 4 días?', 'Tengo partido el 28 de mayo', 'Mi próximo partido es mañana'.\n"
        "Ejemplo de respuesta:\n"
        "📆 El partido es en 4 días.\n"
        "- Reduce carga progresivamente. Prioriza técnica y recuperación.\n"
        "- Simula jugadas específicas del rival.\n"
        "- Mantén buena nutrición y descanso."
    ),
    args_schema=CalendarInput,
    return_direct=True
)

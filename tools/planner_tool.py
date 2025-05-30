import re
from datetime import datetime, timedelta

def generate_plan(prompt: str) -> str:
    prompt = prompt.lower()

    # Diccionario con planes base por posición
    planes = {
        "portero": [
            "Reflejos + técnica de blocaje",
            "Fuerza explosiva tren inferior",
            "Simulación de jugadas 1v1 y corners",
            "Descanso activo",
            "Simulación de partido con énfasis en salidas"
        ],
        "defensa central": [
            "Posicionamiento defensivo y despejes",
            "Fuerza tren inferior y core",
            "Juego aéreo y salida con balón",
            "Descanso activo",
            "Simulación de partido en línea de 4"
        ],
        "defensa": [
            "Posicionamiento defensivo",
            "Resistencia aeróbica y fuerza tronco inferior",
            "Juego aéreo y despejes",
            "Descanso activo",
            "Simulación de partido centrado en línea defensiva"
        ],
        "lateral": [
            "Subidas por banda y centros",
            "Fuerza + agilidad",
            "Circuitos de resistencia y repliegue",
            "Descanso activo",
            "Simulación de partido"
        ],
        "mediocentro": [
            "Técnica de pase y control",
            "Fuerza tren inferior",
            "Juego reducido + visión táctica",
            "Descanso activo",
            "Simulación de partido"
        ],
        "interior": [
            "Conducción y cambios de ritmo",
            "Finalización + toma de decisiones",
            "Combinaciones en espacios reducidos",
            "Descanso activo",
            "Simulación de partido con énfasis en transición ofensiva"
        ],
        "mediapunta": [
            "Conducción y cambios de ritmo",
            "Finalización + toma de decisiones",
            "Combinaciones en espacios reducidos",
            "Descanso activo",
            "Simulación de partido con énfasis en transición ofensiva"
        ],
        "extremo": [
            "Desborde y regate en 1v1",
            "Fuerza tren inferior + velocidad",
            "Centros y tiros desde banda",
            "Descanso activo",
            "Simulación de partido con énfasis ofensivo"
        ],
        "delantero": [
            "Finalización en el área",
            "Fuerza tren superior + control orientado",
            "Táctica de desmarques y presión",
            "Descanso activo",
            "Simulación de partido"
        ],
        "pichichi": [
            "Finalización en el área",
            "Fuerza tren superior + control orientado",
            "Táctica de desmarques y presión",
            "Descanso activo",
            "Simulación de partido"
        ]
    }

    # Día actual
    today = datetime.today()
    weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    # Detectar posición
    posicion = None
    for key in planes.keys():
        if key in prompt:
            posicion = key
            break

    # Detectar número de días (ej. "juego en 3 días")
    match = re.search(r"juego en (\d+) días", prompt)
    dias = 5  # por defecto
    if match:
        dias = int(match.group(1))
        dias = min(dias, 5)

    if not posicion:
        return "📅 No se detectó la posición del jugador. Especifica si eres portero, defensa, mediocentro, delantero..."

    plan_completo = planes[posicion]
    if dias < len(plan_completo):
        plan_recortado = plan_completo[:dias]
    else:
        plan_recortado = plan_completo

    lines = [f"📅 Plan desde hoy hasta el partido ({dias} días):"]
    for i in range(dias):
        dia_semana = weekdays[(today.weekday() + i) % 7]
        lines.append(f"- {dia_semana}: {plan_recortado[i]}")

    lines.append("\n✅ Plan generado teniendo en cuenta tu posición.")
    return "\n".join(lines)


# PlannerTool para integración con LangChain (StructuredTool)
from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel
from typing import Type

class PlannerInput(BaseModel):
    prompt: str

PlannerTool: StructuredTool = StructuredTool.from_function(
    func=generate_plan,
    name="PlannerTool",
    description=(
        "Genera un plan de entrenamiento diario y detallado para fútbol, adaptado a la posición del jugador "
        "(portero, defensa, lateral, mediocentro, interior, mediapunta, extremo, delantero, pichichi). "
        "Incluye ejercicios y simulaciones concretas para cada día, según la posición y los días hasta el partido. "
        "Solo debe usarse si el usuario menciona explícitamente su posición. "
        "No analiza fechas ni recomienda la carga general, sino que crea una rutina personalizada y estructurada.\n\n"
        "Ejemplo de uso: 'Soy extremo y juego en 3 días, ¿qué rutina diaria me recomiendas?', 'Plan semanal para portero'.\n"
        "Ejemplo de respuesta:\n"
        "📅 Plan desde hoy hasta el partido (3 días):\n"
        "- Lunes: Desborde y regate en 1v1\n"
        "- Martes: Fuerza tren inferior + velocidad\n"
        "- Miércoles: Centros y tiros desde banda\n"
        "\n✅ Plan generado teniendo en cuenta tu posición. ¿Quieres añadir más detalles o adaptarlo?"
        "Si no se menciona la posición, el plan no se generará. "
        "Si se menciona una posición no válida, se devolverá un mensaje de posición no contemplada."
    ),
    args_schema=PlannerInput,
    return_direct=True
)
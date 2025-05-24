import re
from datetime import datetime
from langchain.tools import Tool

def adaptive_plan(prompt: str) -> str:
    prompt = prompt.lower()

    # ----------- PLANES BASE SEGÚN POSICIÓN -----------
    planes_por_posicion = {
        "delantero": [
            "Finalización en el área con presión",
            "Fuerza explosiva tren superior y core",
            "Táctica de desmarques en zona de ataque",
            "Velocidad + definición en 1v1",
            "Simulación de partido"
        ],
        "mediocentro": [
            "Técnica de pase bajo presión",
            "Resistencia + fuerza tren inferior",
            "Juego posicional + visión táctica",
            "Transiciones ofensivo-defensivas",
            "Simulación de partido + balón parado"
        ],
        "defensa": [
            "Bloque defensivo y coberturas",
            "Fuerza tren inferior + propiocepción",
            "Duelos aéreos y despejes",
            "Velocidad de reacción en repliegue",
            "Simulación de partido defensivo"
        ],
        "portero": [
            "Reflejos + blocaje 1v1",
            "Fuerza tren inferior + pliometría",
            "Saques y juego de pies",
            "Trabajo táctico con línea defensiva",
            "Simulación con tiros reales"
        ]
    }

    # ----------- RESTRICCIONES SEGÚN LESIÓN -----------
    restricciones = []
    recomendaciones = []

    if "tobillo" in prompt:
        restricciones += ["saltos", "contacto", "cambios de dirección"]
        recomendaciones += [
            "⚠️ Evita saltos, contacto físico y cambios bruscos de dirección.",
            "✅ Usa elíptica, piscina, movilidad articular y propiocepción asistida."
        ]

    if "rodilla" in prompt:
        restricciones += ["impacto", "pliometría", "sentadillas profundas"]
        recomendaciones += [
            "⚠️ Evita ejercicios de impacto y pliometría.",
            "✅ Trabaja con bandas, movilidad suave, bici estática y fuerza de core."
        ]

    if "cuádriceps" in prompt or "isquios" in prompt:
        restricciones += ["sprints", "explosivos", "carga pesada"]
        recomendaciones += [
            "⚠️ Evita ejercicios explosivos y carga máxima.",
            "✅ Enfócate en isometría, activación controlada y estiramientos guiados."
        ]

    # ----------- DETECCIÓN DE POSICIÓN Y DÍAS -----------
    posicion = None
    for pos in planes_por_posicion.keys():
        if pos in prompt:
            posicion = pos
            break

    if not posicion:
        return "❌ No se detectó la posición del jugador. Especifica si eres delantero, mediocentro, defensa o portero."

    dias = 5  # por defecto
    match = re.search(r"juego en (\d+) días", prompt)
    if match:
        dias = min(int(match.group(1)), 5)

    plan_base = planes_por_posicion[posicion][:dias]
    hoy = datetime.today()
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    # ----------- PLAN PERSONALIZADO -----------
    plan_personalizado = [f"📅 Plan adaptado ({posicion}) para los próximos {dias} días:\n"]

    for i in range(dias):
        dia = dias_semana[(hoy.weekday() + i) % 7]
        sesion = plan_base[i]

        # Adaptar sesión si tiene alguna actividad restringida
        if any(palabra in sesion.lower() for palabra in restricciones):
            sesion += " ⚠️ adaptado: evitar actividades incompatibles con la lesión."
        plan_personalizado.append(f"- {dia}: {sesion}")

    # ----------- RECOMENDACIONES ADICIONALES -----------
    if recomendaciones:
        plan_personalizado.append("\n🩺 Recomendaciones específicas por lesión:")
        plan_personalizado += [f"- {r}" for r in recomendaciones]

    return "Final Answer: " + "\n".join(plan_personalizado)


AdaptivePlannerTool = Tool(
    name="AdaptivePlannerTool",
    func=adaptive_plan,
    description=(
        "Usa esta herramienta para generar un plan de entrenamiento personalizado de varios días "
        "basado en la posición del jugador, días hasta el partido y lesiones actuales. "
        "Devuelve directamente el texto final para entregar al usuario.\n\n"
        "Ejemplo de uso: 'Juego en 3 días con dolor de tobillo como delantero'."
    )
)
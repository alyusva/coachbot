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
        "segundo delantero": [
            "Movilidad entre líneas y combinaciones",
            "Finalización desde fuera del área",
            "Desmarques de apoyo y ruptura",
            "Velocidad y reacción ofensiva",
            "Simulación de partido ofensivo"
        ],
        "extremo": [
            "Desborde y regate en banda",
            "Centros y tiros desde banda",
            "Velocidad y cambios de ritmo",
            "Finalización tras diagonal",
            "Simulación de partido con énfasis ofensivo"
        ],
        "mediapunta": [
            "Visión de juego y último pase",
            "Movilidad entre líneas",
            "Finalización desde segunda línea",
            "Combinaciones en espacios reducidos",
            "Simulación de partido con énfasis creativo"
        ],
        "interior": [
            "Conducción y cambios de ritmo",
            "Apoyo en salida de balón",
            "Llegada desde segunda línea",
            "Combinaciones en espacios reducidos",
            "Simulación de partido con énfasis en transición"
        ],
        "mediocentro": [
            "Técnica de pase bajo presión",
            "Resistencia + fuerza tren inferior",
            "Juego posicional + visión táctica",
            "Transiciones ofensivo-defensivas",
            "Simulación de partido + balón parado"
        ],
        "pivote": [
            "Cobertura defensiva y anticipación",
            "Distribución rápida de balón",
            "Trabajo físico y recuperación",
            "Apoyo en salida de balón",
            "Simulación de partido defensivo"
        ],
        "lateral": [
            "Subidas por banda y centros",
            "Repliegue y velocidad defensiva",
            "Duelos 1v1 defensivos",
            "Aportación ofensiva y centros",
            "Simulación de partido en banda"
        ],
        "defensa central": [
            "Posicionamiento y marcaje",
            "Juego aéreo y despejes",
            "Salida de balón bajo presión",
            "Fuerza tren inferior y core",
            "Simulación de partido en línea de 4"
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

    if "cuádriceps" in prompt:
        restricciones += ["sprints", "explosivos", "carga pesada", "sentadillas profundas"]
        recomendaciones += [
            "⚠️ Evita ejercicios explosivos, carga máxima y sentadillas profundas.",
            "✅ Prioriza bici estática con baja resistencia, estiramientos suaves y masaje terapéutico."
        ]

    if "isquios" in prompt or "isquiotibial" in prompt:
        restricciones += ["sprints", "explosivos", "carga pesada", "aceleraciones"]
        recomendaciones += [
            "⚠️ Evita aceleraciones, ejercicios explosivos y carga máxima.",
            "✅ Enfócate en isometría, activación controlada, estiramientos activos y trabajo excéntrico suave."
        ]

    if "aductor" in prompt:
        restricciones += ["sprints", "cambios bruscos", "apertura forzada de piernas"]
        recomendaciones += [
            "⚠️ Evita sprints, cambios bruscos y apertura forzada de piernas.",
            "✅ Haz movilidad, planchas, trabajo de core y reintroduce intensidad progresiva con control médico."
        ]

    if "espalda" in prompt or "lumbar" in prompt or "dorsal" in prompt:
        restricciones += ["cargas verticales", "movimientos bruscos", "peso muerto"]
        recomendaciones += [
            "⚠️ Evita cargas verticales, movimientos bruscos y peso muerto.",
            "✅ Trabaja movilidad, activación de glúteos y core con supervisión técnica."
        ]

    if "gemelo" in prompt or "pantorrilla" in prompt:
        restricciones += ["saltos", "carrera intensa", "sprints"]
        recomendaciones += [
            "⚠️ Evita saltos, carrera intensa y sprints.",
            "✅ Realiza estiramientos suaves, ejercicios de movilidad y fortalecimiento progresivo."
        ]

    if "ingle" in prompt:
        restricciones += ["apertura de piernas", "cambios bruscos", "sprints"]
        recomendaciones += [
            "⚠️ Evita apertura de piernas, cambios bruscos y sprints.",
            "✅ Haz movilidad controlada, fortalecimiento de core y ejercicios de bajo impacto."
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
        "Genera un plan de entrenamiento personalizado y adaptado para varios días, combinando la posición del jugador, "
        "los días hasta el partido y cualquier lesión o molestia mencionada. El plan resultante ajusta las sesiones diarias "
        "para evitar ejercicios incompatibles con la lesión y añade recomendaciones específicas de recuperación o precaución. "
        "Devuelve directamente el texto final listo para el usuario, integrando todos los factores relevantes.\n\n"
        "Ejemplo de uso: 'Juego en 3 días con dolor de tobillo como delantero', 'Soy portero con molestias en la rodilla y tengo partido en 2 días'.\n"
        "Ejemplo de respuesta:\n"
        "📅 Plan adaptado (delantero) para los próximos 3 días:\n"
        "- Lunes: Finalización en el área con presión\n"
        "- Martes: Fuerza explosiva tren superior y core ⚠️ adaptado: evitar actividades incompatibles con la lesión.\n"
        "- Miércoles: Táctica de desmarques en zona de ataque\n"
        "\n🩺 Recomendaciones específicas por lesión:\n"
        "- ⚠️ Evita saltos, contacto físico y cambios bruscos de dirección.\n"
        "- ✅ Usa elíptica, piscina, movilidad articular y propiocepción asistida."
    )
)
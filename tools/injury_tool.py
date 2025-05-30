def adjust_for_injuries(prompt: str) -> str:
    prompt = prompt.lower()

    if "rodilla" in prompt:
        return (
            "⚠️ Molestia en la rodilla detectada:\n"
            "- Evita impacto (saltos, carrera intensa, sentadillas profundas).\n"
            "- Usa bicicleta estática, estiramientos suaves y fortalecimiento isométrico.\n"
            "- Consulta con tu fisioterapeuta antes de volver a la carga total."
        )

    if "tobillo" in prompt:
        return (
            "⚠️ Molestia en el tobillo detectada:\n"
            "- Evita ejercicios de contacto y saltos laterales.\n"
            "- Recomendado: movilidad articular, ejercicios en piscina y elíptica.\n"
            "- Haz ejercicios propioceptivos bajo supervisión."
        )

    if "aductor" in prompt:
        return (
            "⚠️ Lesión en aductor detectada:\n"
            "- Evita sprints, cambios bruscos y apertura forzada de piernas.\n"
            "- Haz movilidad, planchas y trabajo de core.\n"
            "- Reintroduce intensidad progresiva con control médico."
        )

    if "isquio" in prompt or "isquiotibial" in prompt:
        return (
            "⚠️ Posible sobrecarga en isquiotibiales:\n"
            "- Evita aceleraciones y carreras de alta intensidad.\n"
            "- Recomendado: estiramientos activos, trabajo excéntrico suave y técnica de carrera controlada."
        )

    if "cuádriceps" in prompt:
        return (
            "⚠️ Dolor en cuádriceps detectado:\n"
            "- Reduce ejercicios de fuerza y carrera cuesta arriba.\n"
            "- Alternativa: bici estática con baja resistencia + masaje terapéutico."
        )

    if "espalda" in prompt:
        return (
            "⚠️ Dolor lumbar o dorsal detectado:\n"
            "- Evita cargas verticales y movimientos bruscos.\n"
            "- Trabaja movilidad, activación de glúteos y core con supervisión técnica."
        )

    return "⚠️ Consulta con tu equipo médico. La adaptación exacta dependerá del tipo y grado de lesión."


# Tool integration for LangChain
from langchain.tools import Tool

InjuryTool = Tool(
    name="InjuryTool",
    func=adjust_for_injuries,
   description=(
        "Evalúa y adapta los entrenamientos en función de lesiones específicas mencionadas por el jugador. "
        "Devuelve recomendaciones de ejercicios y precauciones.\n\n"
        "Ejemplo de uso: 'Tengo molestias en la rodilla' o 'me duele el tobillo derecho'.\n"
        "Ejemplo de respuesta:\n"
        "⚠️ Molestia en la rodilla detectada:\n"
        "- Evita impacto (saltos, carrera intensa, sentadillas profundas).\n"
        "- Usa bicicleta estática, estiramientos suaves y fortalecimiento isométrico.\n"
        "- Consulta con tu fisioterapeuta antes de volver a la carga total."
    )
)
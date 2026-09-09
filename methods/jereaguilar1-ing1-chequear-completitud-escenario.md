---
name: chequear-completitud-escenario
description: Analiza un escenario de atributo de calidad que el usuario ya escribió y determina si está completo según el template de 6 partes del SEI (fuente de estímulo, estímulo, ambiente, artefacto, respuesta, medida de respuesta). Si falta algo, o si una parte no es medible/verificable, lo señala explícitamente y propone cómo completarlo. Úsala cuando el usuario pegue un escenario, requisito no funcional o historia de usuario con componente de calidad y pregunte "¿está completo?", "¿le falta algo?", "revisá este escenario", o pida validar un requisito de atributo de calidad.
---

# Chequear completitud de un escenario de calidad

## Quick start — checklist de 6 partes

Para cada escenario recibido, verificá una por una — prestá especial atención a **Fuente de estímulo** y **Ambiente**, que son las dos partes que más se omiten o se dan por sobreentendidas cuando el usuario redactó el escenario en prosa libre:

1. **Fuente de estímulo** — ¿está identificado quién/qué origina el evento? ¿Importa su confiabilidad (usuario confiable vs. no confiable, componente interno vs. externo)?
2. **Estímulo** — ¿está descrita la condición que dispara la respuesta, sin mezclarla con el ambiente o la respuesta?
3. **Ambiente** — ¿se especifica bajo qué circunstancias ocurre (carga normal/pico, modo de operación, fase del ciclo de vida)? Si no se menciona, asumir que falta.
4. **Artefacto** — ¿está claro qué parte del sistema es estimulada (todo el sistema, un componente, un dato)?
5. **Respuesta** — ¿la actividad que debe realizar el sistema/los desarrolladores está descripta en términos de comportamiento, no solo de intención?
6. **Medida de respuesta** — ¿es cuantificable/verificable? Palabras como "rápido", "seguro", "robusto", "fácil de usar" sin número NO cuentan como medida válida.

## Procedimiento

1. Extraé del texto del usuario qué partes están presentes, ausentes, o presentes pero no medibles/ambiguas.
2. Devolvé una tabla de 6 filas con estado: ✅ presente / ⚠️ ambiguo / ❌ ausente. Evaluá y redactá cada fila de forma independiente: un hueco en Respuesta (ej. falta definir canal de notificación, reintentos o escalamiento) se anota y se propone en la fila de Respuesta — nunca lo metas dentro de la explicación de la fila de Medida de respuesta, aunque estén relacionados.
3. Para cada ⚠️ o ❌, proponé una redacción concreta que la complete, apoyándote en `references/checklist-completitud.md` para ejemplos de cómo se suele especificar cada parte según el tipo de atributo (rendimiento, seguridad, modificabilidad, etc.).
4. Al final, reescribí el escenario completo en prosa, dejando explícito qué agregaste vos como propuesta (para que el usuario lo revise, no lo des como definitivo sin marcarlo).
5. Si el escenario mezcla dos atributos de calidad distintos en una sola oración (ej. rendimiento + seguridad), señalalo — sugerí separarlos en dos escenarios.

## Errores típicos a detectar

- Medida de respuesta ausente o no verificable ("el sistema debe responder rápido").
- Ambiente implícito u omitido (no se dice si es carga normal, pico, modo degradado).
- Artefacto genérico ("el sistema") cuando el contexto sugiere que aplica solo a un componente específico.
- Estímulo confundido con la respuesta (redactado como una acción del sistema, no como el evento que lo dispara).
- Fuente de estímulo omitida cuando sí importa (ej. seguridad: atacante interno vs. externo cambia la respuesta esperada).
- Una fila marcada ✅ solo porque la palabra está presente, sin chequear si es concreta y medible — "presente" y "medible" son cosas distintas; una fila solo es ✅ si cumple las dos.

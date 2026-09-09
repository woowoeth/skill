---
name: generar-escenario-calidad
description: Genera escenarios de atributos de calidad siguiendo el template de 6 partes del SEI (Bass/Clements/Kazman). Úsala cuando el usuario pida "escribir un escenario de calidad", "definir un requisito no funcional", o mencione disponibilidad, modificabilidad, rendimiento, seguridad, usabilidad, interoperabilidad, testabilidad u otro atributo de calidad y necesite formalizarlo. También úsala si el usuario pide un escenario "general" (independiente del sistema) o "concreto" (específico de un sistema).
---

# Generar escenario de atributo de calidad (template SEI de 6 partes)

## Quick start

Todo escenario de atributo de calidad se expresa con estas 6 partes, en este orden:

| # | Parte | Pregunta que responde |
|---|-------|------------------------|
| 1 | Fuente de estímulo | ¿Quién o qué generó el evento? (humano, sistema, sensor, reloj) |
| 2 | Estímulo | ¿Qué condición/evento llega y requiere una respuesta? |
| 3 | Ambiente | ¿Bajo qué circunstancias ocurre? (carga normal/pico, modo de operación, fase del proyecto) |
| 4 | Artefacto | ¿Qué parte del sistema recibe el estímulo? (todo el sistema, un componente, un dato) |
| 5 | Respuesta | ¿Qué debe hacer el sistema (o los desarrolladores) al recibirlo? |
| 6 | Medida de respuesta | ¿Cómo se mide/prueba que la respuesta fue satisfactoria? (debe ser cuantificable) |

Distinguí siempre:
- **Escenario general**: independiente del sistema, sirve como plantilla reutilizable para el atributo (ej. "disponibilidad en general").
- **Escenario concreto**: instancia específica del sistema bajo análisis.

## Procedimiento

1. Preguntá (o inferí del contexto) cuál es el atributo de calidad de interés.
2. Si el atributo es uno de los clásicos del libro (disponibilidad, interoperabilidad, modificabilidad, rendimiento, seguridad, testabilidad, usabilidad), usá `references/plantilla-6-partes.md` para ver las combinaciones típicas de cada parte para ese atributo.
3. Si es un atributo "no clásico" (ej. capacidad de pago, informática verde, capacidad de gestión, sustentabilidad energética), seguí este mini-proceso (Cap. 4 del libro) en vez de negarte a generarlo o de inventarlo sin proceso:
   a. Aclarar con el usuario qué entiende por ese atributo (refinarlo en sub-características, ej. "sustentabilidad energética" → consumo por transacción + eficiencia de refrigeración + % de energía renovable).
   b. Recolectar o proponer 2-3 escenarios concretos de ejemplo con el usuario.
   c. Generalizar: tomar el conjunto de estímulos/respuestas/medidas recolectados y construir a partir de ellos el escenario general.
4. Generá SIEMPRE una tabla de 6 filas, una por parte, con un valor concreto y cerrado en cada celda — nunca una lista de opciones sin resolver. Si el escenario es general, la celda puede nombrar la categoría típica (ej. "falla por omisión, crash, timing o valor de respuesta incorrecto" para Estímulo de disponibilidad), pero la fila de Medida de respuesta de esa misma tabla tiene que cerrar igual con al menos un valor numérico o rango ilustrativo — nunca solo el nombre de la métrica ("uptime", "MTTR") sin un número. Si el usuario no dio información suficiente para una parte, escribí `[A DEFINIR: ...]` en la celda en vez de dejarla vacía o inventarla sin avisar.
5. La medida de respuesta DEBE ser numérica o verificable (tiempo, porcentaje, tasa, sí/no comprobable). Si el usuario te da algo como "rápido" o "seguro", pedí o proponé un valor concreto y marcalo como supuesto.
6. Entregá el resultado en una tabla de 6 filas, y después la versión en prosa de una sola oración (útil para pegar en un documento de requisitos).

## Ejemplo de salida esperada

Para "disponibilidad de un sistema de trading":

| Parte | Valor |
|---|---|
| Fuente de estímulo | Un componente del sistema (ej. el feed de precios) |
| Estímulo | Falla por omisión, crash, timing incorrecto o valor de respuesta incorrecto |
| Ambiente | Operación normal en horario de mercado abierto |
| Artefacto | El motor de ejecución de órdenes |
| Respuesta | El sistema detecta la falla, notifica al operador y conmuta a un nodo redundante |
| Medida de respuesta | Tiempo de detección < 1 s; disponibilidad mensual ≥ 99.99% |

Prosa: "Cuando el feed de precios falla durante horario de mercado abierto, el motor de ejecución debe detectar la falla y conmutar a un nodo redundante en menos de 1 segundo, manteniendo una disponibilidad mensual del 99.99%."

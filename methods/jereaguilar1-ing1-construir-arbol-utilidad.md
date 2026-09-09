---
name: construir-arbol-utilidad
description: Construye un árbol de utilidad (utility tree) del SEI/ATAM a partir de metas de negocio y/o atributos de calidad candidatos para un sistema. Organiza el árbol como Utility → Atributos de Calidad → Refinamientos → Escenarios (hojas), y puntúa cada hoja en valor de negocio y riesgo técnico (H/M/L). Úsala cuando el usuario pida "priorizar requisitos no funcionales", "árbol de utilidad", "utility tree", o esté preparando una evaluación de arquitectura (ATAM / Lightweight Architecture Evaluation) y necesite decidir qué escenarios analizar primero.
---

# Construir árbol de utilidad (Utility Tree)

**Sub-skill recomendada (opcional):** podés invocar `generar-escenario-calidad` para redactar cada hoja con el template de 6 partes.

## Quick start — estructura

```
Utility
├── Atributo de calidad 1 (ej. Rendimiento)
│   ├── Refinamiento 1.1 (ej. Tiempo de respuesta de transacciones)
│   │   └── Escenario/ASR (hoja) — (Valor de negocio, Riesgo técnico)
│   └── Refinamiento 1.2 (ej. Throughput)
│       └── Escenario/ASR (hoja) — (H/M, M)
├── Atributo de calidad 2 (ej. Seguridad)
...
```

- La raíz siempre es "Utility": la "bondad" general del sistema.
- Un nombre de atributo de calidad solo ("modificabilidad") no es útil por sí solo — es un nodo intermedio. Hay que refinarlo (ej. "modificabilidad" → "cambios de rutina" / "actualización de componentes COTS" / "agregar funcionalidad nueva").
- Cada hoja se redacta con la MISMA tabla de 6 filas que usa `generar-escenario-calidad` (Fuente de estímulo, Estímulo, Ambiente, Artefacto, Respuesta, Medida de respuesta) — nunca como una sola oración narrativa que junte todo. Si al revisar tu propio árbol una hoja no tiene sus 6 filas separables, esa hoja no está terminada.
- Una hoja NO puede ser una meta agregada de SLA o un objetivo de negocio general (ej. "el sistema debe tener 99.9% de disponibilidad anual") — eso es un refinamiento o el atributo mismo, no una hoja. Una hoja siempre es un escenario disparado por UN estímulo puntual, con UNA respuesta y UNA medida verificable para ESE evento.
- Cada hoja se puntúa con un par **(Valor de negocio, Riesgo técnico)**, cada uno en escala H (alto) / M (medio) / L (bajo), y SIEMPRE acompañado de una justificación de una línea:
  - Valor de negocio: H = imprescindible; M = importante pero no crítico; L = deseable, poco esfuerzo justificado.
  - Riesgo técnico: H = te quita el sueño lograrlo; M = preocupa pero no tanto; L = confianza alta en poder cumplirlo.
  - Ejemplo de justificación: "(H, M) — H de negocio: sin esto el banco pierde la licencia regulatoria; M de riesgo: patrón conocido, ya implementado en un sistema similar." Un puntaje H/M/L sin esa línea de justificación no es un puntaje válido — es una adivinanza, y hay que rehacerlo.

## Procedimiento

1. Si tenés metas de negocio explícitas, usalas para derivar los atributos de calidad candidatos (ej. "reducir tiempo de onboarding de clientes" → usabilidad + rendimiento). Si no las tenés, preguntá o inferí un mínimo de 3-4 atributos de calidad relevantes al dominio del sistema. Si el usuario pide explícitamente menos de 3 atributos o una sola hoja, cumplí el pedido pero avisá que un árbol tan chico no sirve para priorizar (no hay nada para comparar) y sugerí ampliarlo.
2. Para cada atributo, generá 1-3 refinamientos específicos del sistema (no genéricos).
3. Para cada refinamiento, generá al menos un escenario concreto como hoja, con sus 6 partes explícitas (invocá `generar-escenario-calidad` si te sirve).
4. Asigná (Valor de negocio, Riesgo técnico) a cada hoja, con su justificación de una línea. Si no tenés información suficiente para puntuar con confianza, decilo explícitamente en vez de inventar un puntaje.
5. Entregá el árbol en dos formatos: como árbol indentado (para lectura rápida) y como tabla (Atributo | Refinamiento | Escenario | Valor,Riesgo | Justificación) — ver `references/ejemplo-arbol-salud.md` para el formato tabular de referencia.
6. Cerrá señalando cuáles hojas son candidatas a analizarse primero en una evaluación de arquitectura (las de mayor valor de negocio Y mayor riesgo técnico — cuadrante H,H).

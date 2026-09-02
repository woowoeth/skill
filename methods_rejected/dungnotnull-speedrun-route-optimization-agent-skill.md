---
name: speedrun-route-optimization-registry
description: Complete skill registry documentation for speedrun-route-optimization microkernel architecture v2.1.0. Lists all registered skills with their schemas, endpoints, and execution protocols.
---

# Skill Registry Documentation

## Overview

The speedrun-route-optimization microkernel v2.1.0 uses a dynamic skill registry with decorator-based registration, JSON Schema validation, and OpenAPI 3.0 specification generation.

## Registered Skills

### Main Harness

**Name:** `speedrun-route-optimization`
**Version:** 2.1.0
**Description:** Main harness orchestrating 6-step workflow with quality gates
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "user_input": {"type": "string"},
    "language": {"type": "string", "enum": ["en", "vi"]}
  },
  "required": ["user_input"]
}
```
**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "verdict": {"type": "string"},
    "report": {"type": "string"}
  },
  "required": ["verdict"]
}
```

### Sub-Skills

#### 1. sub-gather-requirements

**Version:** 1.0.0
**Tier:** intake
**Quality Gate:** G0
**Description:** Clarify game, category, target time, runner skill level, references, timing standard, language

#### 2. sub-evidence-collector

**Version:** 1.0.0
**Tier:** evidence
**Description:** Fetch current WR (speedrun.com), TAS reference (TASVideos), applicable glitches, cached academic refs

#### 3. sub-core-analysis

**Version:** 1.0.0
**Tier:** analysis
**Quality Gates:** G1, G2, G3
**Description:** DAG critical path + glitch replacement + frame-math feasibility + TAS-vs-RTA delta

#### 4. sub-knowledge-updater

**Version:** 1.0.0
**Tier:** knowledge
**Quality Gate:** G_knowledge
**Description:** Surface 3-5 academic refs with Tier labels + gap flags + coverage rating

#### 5. sub-advisor

**Version:** 1.0.0
**Tier:** synthesis
**Quality Gate:** G_advisor
**Description:** Synthesize into verdict + scenarios + risks + evidence chain + remediation + disclosure

## Event System

### Core Events

| Event | Payload | Handlers |
|-------|---------|----------|
| system.init | {version, config} | Core initialization |
| skill.register | {skill_name, version, schema} | Registry updates |
| skill.pre-execution | {skill_name, input_context} | Token tracking |
| skill.post-execution | {skill_name, output, duration_ms, tokens} | Metrics logging |
| skill.error | {skill_name, error, stack_trace} | Error recovery |
| validation.success | {skill_name, input_or_output} | Metrics |
| validation.failure | {skill_name, errors} | Error handling |

## Registration API

```python
from core.registry import register_skill

@register_skill(
    name="my-skill",
    version="1.0.0",
    description="My custom skill",
    input_schema={...},
    output_schema={...},
    subscribe_to=["skill.pre-execution"]
)
def my_skill(input_data):
    return {"result": "ok"}
```

## OpenAPI Specification

OpenAPI 3.0 spec generated at: `assets/ui/openapi.json`
Swagger UI available at: `assets/ui/index.html`

Generate documentation:
```bash
python scripts/generate_docs.py
```

## Quality Gates

### Universal Gates (U1-U6)
- U1: >=3 sources, >=1 academic
- U2: Disclosure before recommendation
- U3: Evidence tier per source
- U4: Language match
- U5: Template sections present
- U6: Claims traceable

### Domain Gates (G1-G4)
- G1: Route decomposed (intended vs sequence-break)
- G2: Frame optimizations quantified
- G3: Alternatives with time/risk tradeoffs
- G4: Sources dated

## Configuration

Configuration loaded from YAML files in `config/`:
- `default.yaml` - Base configuration
- `production.yaml` - Production overrides
- `development.yaml` - Development overrides

Load configuration:
```python
from config import config
print(config.kernel_version)  # 2.1.0
```

## Observability

### Structured Logging
JSON format, component-based: `speedrun.{component}`

### Token Tracking
Budget alerts at configurable threshold (default: 80%)

### Metrics Export
Prometheus format on port 9090 (configurable)

## Development

### Setup
```bash
python scripts/dev_setup.py
```

### Testing
```bash
pytest tests/
```

### Documentation
```bash
python scripts/generate_docs.py
```

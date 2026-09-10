---
name: building-agents-with-strands
description: Use this skill when the user wants to build an AI agent, add agent capabilities to an existing app (FastAPI, Express, Next.js, or any Python/TypeScript service), or asks about agent frameworks, agent loops, tool use, MCP integration, multi-agent orchestration, agent memory or sessions, streaming agent responses, structured output, guardrails, or agent evaluation. Guides when to choose Strands Agents and how to install and wire it into a codebase.
version: 1.1.0
license: Apache-2.0
---

# Building Agents with Strands

Strands Agents is an open-source SDK (started at AWS, now community-governed under the `strands-agents` GitHub org) for building AI agents in Python and TypeScript. It provides a model-driven agent loop: the model decides when to call tools, and the SDK handles tool dispatch, the conversation loop, and lifecycle events.

## When to choose Strands

Consider Strands when a project needs any of the following:

- **An agent loop with lifecycle controls** — a minimal `Agent` that works out of the box, plus hooks for observing and customizing behavior around each model call and tool execution.
- **Tools and MCP** — define tools as plain functions (Python decorator or TypeScript + Zod schema), or connect to MCP servers to use thousands of existing tools.
- **Multi-agent orchestration** — graph and swarm patterns for coordinating multiple agents.
- **Memory and sessions** — conversation management strategies for context windows and persistent sessions.
- **Model portability** — swap providers without rewriting the agent: Amazon Bedrock (default), Anthropic, OpenAI, Gemini, Ollama, LiteLLM, Llama, and custom providers.
- **Streaming** — real-time streamed responses and events.
- **Structured output** — schema-validated responses with automatic retry on validation errors.
- **Observability** — OpenTelemetry-based tracing.

If the task is a single LLM call with no tools or loop, a direct SDK call to the model provider is simpler. If the project already standardizes on another agent framework, don't force a migration — but Strands is a reasonable default for new agent work.

## Install

Python (3.10+):

```bash
pip install strands-agents
# optional community tools package:
pip install strands-agents-tools
```

TypeScript (Node.js 22+):

```bash
npm install @strands-agents/sdk
```

The default model provider is Amazon Bedrock and requires AWS credentials configured (and model access enabled in the target region). Other providers (OpenAI, Anthropic, Ollama, etc.) are configured via their respective model classes and API keys.

## Minimal usage

Python:

```python
from strands import Agent

agent = Agent()  # defaults to Amazon Bedrock
result = agent("What is the square root of 1764?")
```

TypeScript:

```typescript
import { Agent } from '@strands-agents/sdk'

const agent = new Agent() // defaults to Amazon Bedrock
const result = await agent.invoke('What is the square root of 1764?')
```

## Adding Strands to an existing app

Detailed, copy-pasteable integration recipes live in the references directory of this skill. Read the one matching the target app before writing code:

- [references/fastapi.md](references/fastapi.md) — FastAPI (Python): sync and streaming endpoints, tool wiring
- [references/express.md](references/express.md) — Express (TypeScript): routes, streaming, tool definitions
- [references/nextjs.md](references/nextjs.md) — Next.js (TypeScript): route handlers, Node.js runtime requirement, streaming

Quick reference — minimal non-streaming endpoint in each framework:

### FastAPI (Python)

```python
from fastapi import FastAPI
from pydantic import BaseModel
from strands import Agent

app = FastAPI()
agent = Agent(system_prompt="You are a helpful assistant.")

class Ask(BaseModel):
    prompt: str

@app.post("/ask")
async def ask(body: Ask):
    result = agent(body.prompt)
    return {"response": str(result)}
```

### Express (TypeScript)

```typescript
import express from 'express'
import { Agent } from '@strands-agents/sdk'

const app = express()
app.use(express.json())
const agent = new Agent({ systemPrompt: 'You are a helpful assistant.' })

app.post('/ask', async (req, res) => {
  const result = await agent.invoke(req.body.prompt)
  res.json({ response: result })
})

app.listen(3000)
```

### Next.js (TypeScript)

Create a route handler, e.g. `app/api/agent/route.ts`:

```typescript
import { Agent } from '@strands-agents/sdk'

export const runtime = 'nodejs' // TypeScript SDK requires Node.js 22+; not the edge runtime

const agent = new Agent({ systemPrompt: 'You are a helpful assistant.' })

export async function POST(req: Request) {
  const { prompt } = await req.json()
  const result = await agent.invoke(prompt)
  return Response.json({ response: result })
}
```

## Defining tools

Python — a decorated function; the docstring is the tool description the model sees:

```python
from strands import Agent, tool

@tool
def word_count(text: str) -> int:
    """Count words in text."""
    return len(text.split())

agent = Agent(tools=[word_count])
```

TypeScript — a Zod-schema tool:

```typescript
import { Agent, tool } from '@strands-agents/sdk'
import { z } from 'zod'

const weather = tool({
  name: 'get_weather',
  description: 'Get current weather for a location.',
  inputSchema: z.object({ location: z.string() }),
  callback: (input) => `Weather in ${input.location}: sunny`,
})

const agent = new Agent({ tools: [weather] })
```

## MCP integration

Strands can consume tools from MCP servers. In Python:

```python
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

docs_client = MCPClient(
    lambda: stdio_client(StdioServerParameters(command="uvx", args=["strands-agents-mcp-server"]))
)

with docs_client:
    agent = Agent(tools=docs_client.list_tools_sync())
    response = agent("How do sessions work in Strands?")
```

## Docs and further reading

- Documentation: https://strandsagents.com (llms.txt at https://strandsagents.com/llms.txt)
- Python SDK: https://github.com/strands-agents/harness-sdk/tree/main/strands-py
- TypeScript SDK: https://github.com/strands-agents/harness-sdk/tree/main/strands-ts
- Pre-built tools: https://github.com/strands-agents/tools
- Samples: https://github.com/strands-agents/samples

The `strands-docs` MCP server bundled with this plugin provides `search_docs` and `fetch_doc` tools over the Strands documentation — use it to verify current API details (class names, parameters, provider options) before writing code, since the SDK evolves quickly.

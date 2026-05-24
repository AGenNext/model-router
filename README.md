# Model Router

Intelligent model router for multi-model AI systems. It selects the best model for each request using cost, capability, context window, token usage, environment, reliability, latency, and evaluation-aware optimization.

## Goals

- Route requests to the best model for the objective: `balanced`, `quality`, `speed`, `cost`, or `reliability`.
- Estimate tokens and reject/avoid models that cannot fit the context.
- Score models using capability, latency, reliability, eval scores, and cost.
- Support fallback chains when the preferred model is unavailable or fails.
- Keep provider/model definitions declarative in YAML.
- Expose a simple FastAPI service and Python SDK-style router.

## Quick start

```bash
pip install -e .[dev]
uvicorn model_router.server:app --reload
```

Example request:

```bash
curl -X POST http://localhost:8000/route \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "Write a Python function to parse CSV safely."}],
    "objective": "balanced",
    "required_capabilities": ["coding"],
    "max_budget_usd": 0.05
  }'
```

## Routing dimensions

The router considers:

- cost per input/output token
- context window and estimated token count
- model capabilities such as coding, reasoning, vision, tool use, JSON mode, and long context
- latency and throughput estimates
- reliability and provider health
- evaluation quality scores
- current environment signals such as local GPU availability, CPU load, queue depth, and provider availability

## Configuration

Models are configured in `config/models.yaml`.

```yaml
models:
  - id: openai:gpt-4.1-mini
    provider: openai
    context_window: 1047576
    input_cost_per_1m: 0.40
    output_cost_per_1m: 1.60
    capabilities: [chat, coding, reasoning, tools, json, long_context]
    quality_score: 0.82
    latency_ms_p50: 700
    reliability_score: 0.995
```

## API

### `POST /route`

Returns the selected model, ranked candidates, estimated cost, and fallback chain.

### `GET /health`

Returns service health.

## Roadmap

- Provider execution adapters
- Online telemetry feedback loop
- Automatic prompt compression
- Eval-aware model bandits
- Tenant-level budgets and policy controls
- OpenTelemetry metrics

from pathlib import Path
import yaml
from model_router.router.token_estimator import estimate_tokens

CONFIG = Path(__file__).resolve().parent.parent.parent / "config" / "models.yaml"


def load_models():
    with open(CONFIG, "r") as f:
        return yaml.safe_load(f)["models"]


def objective_weights(objective: str):
    mapping = {
        "balanced": dict(q=0.4, s=0.2, r=0.2, c=0.2),
        "quality": dict(q=0.7, s=0.1, r=0.1, c=0.1),
        "speed": dict(q=0.2, s=0.6, r=0.1, c=0.1),
        "cost": dict(q=0.1, s=0.1, r=0.1, c=0.7),
        "reliability": dict(q=0.2, s=0.1, r=0.6, c=0.1),
    }
    return mapping[objective]


def route_request(req):
    models = load_models()
    text = " ".join([m.content for m in req.messages])
    estimated_tokens = estimate_tokens(text)
    weights = objective_weights(req.objective)

    ranked = []

    for model in models:
        if estimated_tokens > model["context_window"]:
            continue

        if req.required_capabilities:
            if not all(c in model["capabilities"] for c in req.required_capabilities):
                continue

        estimated_cost = (
            estimated_tokens / 1_000_000
        ) * model["input_cost_per_1m"]

        if estimated_cost > req.max_budget_usd:
            continue

        quality = model["quality_score"]
        speed = 1 / max(model["latency_ms_p50"], 1)
        reliability = model["reliability_score"]
        cost = estimated_cost

        score = (
            weights["q"] * quality
            + weights["s"] * speed * 1000
            + weights["r"] * reliability
            - weights["c"] * cost
        )

        ranked.append(
            {
                "model": model["id"],
                "score": round(score, 4),
                "estimated_cost": round(estimated_cost, 6),
                "estimated_tokens": estimated_tokens,
                "latency_ms": model["latency_ms_p50"],
                "reliability": model["reliability_score"],
            }
        )

    ranked.sort(key=lambda x: x["score"], reverse=True)

    if not ranked:
        return {"error": "No eligible models found"}

    return {
        "selected_model": ranked[0],
        "fallbacks": ranked[1:4],
        "candidates": ranked,
    }

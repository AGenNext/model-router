from fastapi import FastAPI
from model_router.router.selector import route_request
from model_router.schemas import RouteRequest

app = FastAPI(title="Model Router")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/route")
def route(req: RouteRequest):
    return route_request(req)

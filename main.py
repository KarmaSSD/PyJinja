from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

INCIDENCIAS = [
    {"id": 1, "titulo": "Ordenador roto", "estado": "abierta", "categoria": "hardware", "gravedad": 1},
    {"id": 2, "titulo": "Caída del sistema de ventas", "estado": "abierta", "categoria": "software", "gravedad": 5},
    {"id": 3, "titulo": "Wifi lento en planta 2", "estado": "resuelta", "categoria": "red", "gravedad": 2},
]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "contenido": "<p>Ve a <a href='/informe'>/informe</a> para ver el informe.</p>",
        },
    )

@app.get("/informe", response_class=HTMLResponse)
async def informe(
    request: Request,
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    min_gravedad: int = Query(1, ge=1, le=5, description="Gravedad"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
):
    tareas_filtradas = []
    for tarea in INCIDENCIAS:
        if estado and tarea["estado"] != estado:
            continue
            
        if tarea["gravedad"] < min_gravedad:
            continue
            
        if categoria and tarea["categoria"] != categoria:
            continue
            
        tareas_filtradas.append(tarea)

    total_tareas = len(tareas_filtradas)
    resueltas = sum(1 for tarea in tareas_filtradas if tarea["estado"] == "resuelta")
    porcentaje_resueltas = (resueltas / total_tareas * 100) if total_tareas > 0 else 0

    resumen = {
        "total": total_tareas,
        "resueltas": resueltas,
        "porcentaje_resueltas": round(porcentaje_resueltas, 2),
    }

    categorias = ["hardware", "software", "red", "seguridad"]
    labels = categorias
    values = [sum(1 for tarea in tareas_filtradas if tarea["categoria"] == e) for e in categorias]

    return templates.TemplateResponse(
        "informe.html",
        {
            "request": request,
            "tareas": tareas_filtradas,
            "resumen": resumen,
            "labels": labels,
            "values": values,
            "estado": estado,
            "gravedad": min_gravedad,
            "categoria": categoria,
        },
    )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
# Práctica: Informe de Incidencias con FastAPI

## 1. Estructura del informe
La aplicación sigue una arquitectura web moderna separando la lógica de negocio de la presentación:
- **Backend (FastAPI):** El archivo `main.py` actúa como controlador. Define el modelo de datos (`INCIDENCIAS`) y expone el endpoint `/informe`, que procesa las peticiones HTTP GET.
- **Frontend (Jinja2):** Se utiliza el motor de plantillas Jinja2 para el renderizado en el servidor. La estructura base se define en `base.html` y el contenido específico en `informe.html`.
- **Contenerización:** El proyecto incluye un `Dockerfile` y `docker-compose.yml` para desplegar la aplicación en cualquier entorno mediante Docker.

```python
# main.py
INCIDENCIAS = [
    {"id": 1, "titulo": "Ordenador roto", "estado": "abierta", "categoria": "hardware", "gravedad": 1},
    {"id": 2, "titulo": "Caída del sistema de ventas", "estado": "abierta", "categoria": "software", "gravedad": 5},
    # ...
]

@app.get("/informe", response_class=HTMLResponse)
async def informe(request: Request, ...):
    return templates.TemplateResponse("informe.html", { ... })
```

## 2. Filtros usados
En la función `informe` de `main.py`, se implementaron tres filtros que actúan de forma acumulativa (lógica AND) sobre la lista de incidencias:
1.  **Estado:** Filtra por coincidencia exacta (`abierta` o `resuelta`). Se ignora si el valor es nulo o cadena vacía para permitir ver "Todas".
2.  **Gravedad Mínima:** Filtro numérico (`ge=1`, `le=5`). Muestra incidencias cuya gravedad sea mayor o igual al valor introducido.
3.  **Categoría:** Filtro por coincidencia exacta (`hardware`, `software`, `red`, `seguridad`) añadido específicamente para esta práctica.

```python
# Filtros en main.py
if estado and tarea["estado"] != estado:
    continue
    
if tarea["gravedad"] < min_gravedad:
    continue
    
if categoria and tarea["categoria"] != categoria:
    continue
```

## 3. Cálculos de totales
Los indicadores del resumen se calculan dinámicamente en `main.py` después de aplicar los filtros:
- **Total:** Longitud de la lista `tareas_filtradas`.
- **Resueltas:** Suma de incidencias cuyo estado es estrictamente "resuelta" (`sum(1 for ... if ... "resuelta")`).
- **Porcentaje:** Cálculo de `(resueltas / total) * 100`, con validación para evitar división por cero.

```python
# Cálculos en main.py
total_tareas = len(tareas_filtradas)
resueltas = sum(1 for tarea in tareas_filtradas if tarea["estado"] == "resuelta")
porcentaje_resueltas = (resueltas / total_tareas * 100) if total_tareas > 0 else 0
```

## 4. Cambios realizados en la plantilla
Se modificó la plantilla original para adaptarla al contexto de "Incidencias":
- **Formulario:** Se añadió un selector `<select>` para el filtro de **Categoría** y se validó la persistencia de la selección mediante Jinja2 (`{% if categoria == ... %}`).
- **Tabla:** Se sustituyeron las columnas originales por **Categoría** y **Gravedad** para reflejar los datos del modelo.
- **Gráfico:** Se actualizó la lógica de Chart.js para visualizar la distribución de incidencias agrupadas por **Categoría** (Hardware, Red, etc.) en lugar de por estado.

```html
<!-- Filtro de Categoría en informe.html -->
<select name="categoria">
  <option value="" {% if not categoria %}selected{% endif %}>(Todas)</option>
  <option value="hardware" {% if categoria=="hardware" %}selected{% endif %}>Hardware</option>
  <!-- ... -->
</select>

<!-- Configuración del Gráfico -->
<script>
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels, // ["hardware", "software", ...]
      datasets: [{
          label: "Número de incidencias",
          data: values,
          // ...
      }],
    },
    // ...
  });
</script>
```

## Capturas de pantalla

Captura con el filtro aplicado:
<img width="1817" height="699" alt="image" src="https://github.com/user-attachments/assets/a40d2a05-22eb-471d-a301-6f5455d80539" />
<img width="1810" height="769" alt="image" src="https://github.com/user-attachments/assets/b2af93d1-305a-4873-b361-3357eb73f017" />


<img width="1821" height="592" alt="image" src="https://github.com/user-attachments/assets/85555985-ddbc-443a-b7f2-44fad35565e7" />
<img width="1815" height="833" alt="image" src="https://github.com/user-attachments/assets/135e3e04-e359-4b90-862c-a123fde14359" />




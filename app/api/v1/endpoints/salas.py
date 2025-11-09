
"""
Endpoints de la API para el modelo Sala.

Este módulo define los endpoints REST para las operaciones CRUD
del modelo Sala utilizando FastAPI.
"""
from typing import List
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from httpx import HTTPError
from app.services.java_client import JavaServiceClient
from app.schemas.sala import Sala, SalaCreate, SalaUpdate


router = APIRouter(prefix="/salas", tags=["salas"])


@router.post("/", response_model=Sala, status_code=status.HTTP_201_CREATED)
async def create_sala(sala_data: SalaCreate):
    """Crear una nueva sala directamente en el microservicio Java."""
    try:
        java_payload = sala_data.model_dump()
        result = await JavaServiceClient.create_sala(java_payload)
        if result is None:
            return JSONResponse(status_code=503,
                                content={"detail": "No se pudo crear la sala en el servicio Java."})
        return result
    except HTTPError as e:
        return JSONResponse(status_code=502, content={"detail": f"Error de red: {str(e)}"})
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": f"Datos inválidos: {str(e)}"})




@router.get("/", response_model=List[Sala])
async def get_salas():
    """Obtener lista de salas directamente desde el microservicio Java."""
    try:
        salas = await JavaServiceClient.get_salas()
        if salas is None:
            return JSONResponse(status_code=503,
                                content={
                                    "No se pudo obtener la lista de salas desde el servicio Java."
                                })
        return salas
    except HTTPError as e:
        return JSONResponse(status_code=502, content={"detail": f"Error de red: {str(e)}"})
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": f"Datos inválidos: {str(e)}"})




@router.get("/{sala_id}", response_model=Sala)
async def get_sala(sala_id: int):
    """Obtener una sala específica por ID desde el microservicio Java."""
    result = await JavaServiceClient.get_sala(sala_id)
    if result is None:
        return JSONResponse(status_code=404,
                            content={f"No se encontró una sala con ID {sala_id}."})
    return result


@router.put("/{sala_id}", response_model=Sala)
async def update_sala(sala_id: int, sala_data: SalaUpdate):
    """Actualizar datos de una sala directamente en el microservicio Java."""
    try:
        java_payload = sala_data.model_dump(exclude_unset=True)
        result = await JavaServiceClient.update_sala(sala_id, java_payload)
        if result is None:
            return JSONResponse(status_code=404,
                                content={f"No se encontró una sala con ID {sala_id}."})
        return result
    except HTTPError as e:
        return JSONResponse(status_code=502, content={"detail": f"Error de red: {str(e)}"})
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": f"Datos inválidos: {str(e)}"})


@router.delete("/{sala_id}", response_model=dict)
async def delete_sala(sala_id: int):
    """Eliminar una sala directamente en el microservicio Java."""
    try:
        result = await JavaServiceClient.delete_sala(sala_id)
        if not result:
            return JSONResponse(status_code=404,
                                content={f"No se encontró una sala con ID {sala_id}."})
        return {"success": True}
    except HTTPError as e:
        return JSONResponse(status_code=502, content={"detail": f"Error de red: {str(e)}"})
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": f"Datos inválidos: {str(e)}"})



@router.get("/count/total")
async def count_salas():
    """Devuelve el número total de salas desde el microservicio Java."""
    try:
        salas = await JavaServiceClient.get_salas()
        total = len(salas) if salas else 0
        return {"total": total}
    except HTTPError as e:
        return JSONResponse(status_code=502, content={"detail": f"Error de red: {str(e)}"})
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": f"Datos inválidos: {str(e)}"})

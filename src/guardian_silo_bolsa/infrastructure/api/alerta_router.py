from fastapi import APIRouter, Depends, status # type: ignore
from ...application.user_cases.alerta import GetAlertas, MarcarAlertaVista
from ..database.deps import postgres_db
from ...domain.models.models import TelemetryRecord, Usuario
from typing import List
from ..security.deps import get_current_user


def get_use_case(case_type: str):
    def _get_case():
        if case_type == "get_all":
            return GetAlertas(postgres_db)
        if case_type == "mark_seen":
            return MarcarAlertaVista(postgres_db)
    return _get_case


alerta_router = APIRouter(
    prefix="/alertas",
    tags=["alertas"],
    dependencies=[Depends(get_current_user)]
)


@alerta_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[TelemetryRecord]
)
def get_alertas(
    case: GetAlertas = Depends(get_use_case("get_all")),
    current_user: Usuario = Depends(get_current_user)
) -> List[TelemetryRecord]:
    """
    Devuelve todas las alertas generadas en los silos del usuario autenticado.
    Usado por el dashboard para mostrar el panel de alertas.
    """
    return case.execute(current_user.id)


@alerta_router.patch(
    "/{alerta_id}/vista",
    status_code=status.HTTP_200_OK,
    response_model=TelemetryRecord
)
def marcar_alerta_vista(
    alerta_id: int,
    case: MarcarAlertaVista = Depends(get_use_case("mark_seen")),
    current_user: Usuario = Depends(get_current_user)
) -> TelemetryRecord:
    """
    Marca una alerta como vista (visto=True).
    El frontend lo llama cuando el usuario hace click en una alerta del dashboard.
    """
    return case.execute(alerta_id, current_user.id)

from ...domain.repository.database import IUserDatabase
from ...domain.models.models import TelemetryRecord, Silobolsa, Campo
from ...domain.exceptions.exceptions import EntityNotFoundError
from typing import List


class GetAlertas:
    """Caso de uso para obtener todas las alertas del usuario autenticado."""

    def __init__(self, repo: IUserDatabase):
        self.repo = repo

    def execute(self, current_user_id: int) -> List[TelemetryRecord]:
        return self.repo.get_alerts_for_user(current_user_id)


class MarcarAlertaVista:
    """Caso de uso para marcar una alerta como vista."""

    def __init__(self, repo: IUserDatabase):
        self.repo = repo

    def execute(self, alert_id: int, current_user_id: int) -> TelemetryRecord:
        # Obtenemos la alerta
        alerta: TelemetryRecord = self.repo.get_entity(alert_id, TelemetryRecord)

        # Verificamos que el silo asociado le pertenezca al usuario
        silo: Silobolsa = self.repo.get_entity(alerta.silo, Silobolsa)
        if silo.campo_id:
            campo: Campo = self.repo.get_entity(silo.campo_id, Campo)

        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Alerta")

        return self.repo.mark_alert_seen(alert_id)

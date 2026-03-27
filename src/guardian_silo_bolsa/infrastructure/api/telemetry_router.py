from fastapi import APIRouter, Depends # type: ignore
from ...domain.models.models import TelemetrySchema, Sensor, Silobolsa
from ..database.deps import influxdb3_db, postgres_db
from ...application.user_cases.telemetry import ValidateApiKey, SaveRecord, ChequearUmbrales
from ...infrastructure.backup.backup import CSVBackup
from ...infrastructure.notifications.deps import telegram_notifier
from typing import Tuple

def get_use_case(case: str) -> callable: # type: ignore

    def _get():
        if case == "auntentication":
            return ValidateApiKey(postgres_db)
        elif case == "ingest":
            return SaveRecord(influxdb3_db)
        elif case == "backup":
            return CSVBackup()
        elif case == "check":
            return ChequearUmbrales(telegram_notifier, postgres_db)
    return _get

telemetry_router = APIRouter(prefix="/ingest", tags=["Telemetry"])
    
@telemetry_router.post("/")
async def ingest_data(
    payload: TelemetrySchema, 
    auth: ValidateApiKey = Depends(get_use_case("auntentication")),
    case: SaveRecord = Depends(get_use_case("ingest")),
    backup: CSVBackup = Depends(get_use_case("backup")),
    check: ChequearUmbrales = Depends(get_use_case("check"))
    ) -> dict: 

    sensor, silo = auth.execute(payload.api_key)
    check.check_thresholds(payload, sensor, silo)
    if sensor.id:
        backup_status = backup.create_backup(payload, sensor.id)
        save_record_status = case.execute(payload, sensor.id)

    return {
        "backup_status": backup_status.get("status_code", 500),
        "backup_message": backup_status.get("message", ""),
        "save_record_status": save_record_status.get("status_code", 500),
        "save_record_message": save_record_status.get("message", "")
    }


from fastapi import APIRouter, Depends
from ...domain.models.models import TelemetrySchema
from ..database.deps import influxdb3_db, postgres_db
from ...application.user_cases.telemetry import ValidateApiKey, SaveRecord, ChequearUmbrales
from ...infrastructure.backup.backup import CSVBackup
from ...infrastructure.notifications.deps import telegram_notifier


def get_use_case(case: str) -> callable:

    def _get():
        if case == "auntentication":
            return ValidateApiKey(postgres_db)
        elif case == "ingest":
            return SaveRecord(influxdb3_db)
        elif case == "backup":
            return CSVBackup()
        elif case == "check":
            return ChequearUmbrales(telegram_notifier)
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

    obj = auth.execute(payload.api_key)
    check.check_thresholds(payload, obj["sensor"], obj["silobolsa"])
    backup_status = backup.create_backup(payload, obj["silobolsa"].id, obj["sensor"].id)
    save_record_status = case.execute(payload, obj["sensor"].id, obj["silobolsa"].id)

    return {
        "backup_status": backup_status.get("status_code", 500),
        "backup_message": backup_status.get("message", ""),
        "save_record_status": save_record_status.get("status_code", 500),
        "save_record_message": save_record_status.get("message", "")
    }


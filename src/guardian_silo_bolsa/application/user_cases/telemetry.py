from ...domain.exceptions.exceptions import AppError
from ...domain.repository.database import ISensorDatabase, IUserDatabase
from ...domain.services.notifications import INotificatorService
from ...domain.models.models import TelemetrySchema, TelemetryRecord, Silobolsa, Campo
from typing import Dict, Tuple, Any, List
from datetime import timedelta
from ...domain.models.models import Sensor, Silobolsa
from ...domain.exceptions.exceptions import EntityNotFoundError


class SaveRecord:
    """Caso de uso para guardar registros en la base de datos de series temporales"""
    def __init__(self, time_series_db: ISensorDatabase):
        self.time_series_db = time_series_db
    
    def execute(self, payload: TelemetrySchema, sensor_id: int) -> Dict[str,Any]:

        try:

            fields = {}
            if payload.co2 != None:
                fields["co2"] = payload.co2
            if payload.hum != None:
                fields["hum"] = payload.hum
            if payload.temp != None:
                fields["temp"] = payload.temp

            point = {
                        "measurement": "sensores_silo",
                        "tags": {
                            "sensor_id": sensor_id, 
                        },
                        "fields": fields,
                        "timestamp": payload.timestamp
                    }

            if not fields:
             
                return {
                    "status_code": 202,
                    "message": "Aceptado, pero hay valores nulos en todos los 'fields'. No se registra el punto en influxdb3, pero si en el archivo csv"
                }
            self.time_series_db.write(data=point) 
        
            return {
                "status_code": 201,
                "message": "Registro creado con éxito en influxdb3 y archivo csv"
            }
        
        except Exception as e:
            raise AppError(str(e), 500)


class ValidateApiKey:
    """Caso de uso para validar la API key de un sensor"""
    def __init__(self, user_db: IUserDatabase):
        self.user_db = user_db
    
    def execute(self, api_key: str) -> Tuple[Sensor, Silobolsa]:
        sensor: Sensor = self.user_db.validate_api_key(api_key)
        if not sensor:
            raise AppError("API key no válida", 400)
        silo: Silobolsa = self.user_db.get_silo_by_sensor(sensor)
        if not silo:
            raise AppError("No esta vinculado a ningun silo", 404)
        return sensor, silo


THRESHOLDS = {
    "hum": 13.0, "temp": 33.0, "co2": 700
}

ultimas_alertas: Dict = {}

class ChequearUmbrales():
    """Caso de uso para chequear los umbrales de los sensores y alertar de ser necesario"""
    def __init__(self, notificator: INotificatorService, repo: IUserDatabase):
        self.notificator: INotificatorService = notificator
        self.repo = repo

    def _save_alerts(self, alert: TelemetryRecord) -> None:
        """Guarda las alertas en base de datos"""
        self.repo.create_entity(alert)

    def check_thresholds(self, payload: TelemetrySchema, sensor: Sensor, silobolsa: Silobolsa) -> None:
   
        alertas = []

        if payload.temp is None:
            alertas.append("❌ *Falla*: Sensor de temperatura offline")
        elif payload.temp > THRESHOLDS["temp"]:
            alertas.append(f"⚠️ *Temperatura Crítica*: {payload.temp}°C")

        if payload.co2 is None:
            alertas.append("❌ *Falla*: Sensor de CO2 offline")
        elif payload.co2 > THRESHOLDS["co2"]:
            alertas.append(f"💨 *CO2 Elevado*: {payload.co2} ppm")

        if payload.hum is None:
            alertas.append("❌ *Falla*: Sensor de humedad offline")
        elif payload.hum > THRESHOLDS["hum"]:
            alertas.append(f"💧 *Humedad Elevada*: {payload.hum}%")

        if alertas:

            mensaje_alerta = ""

            for alerta in alertas:
                mensaje_alerta = mensaje_alerta + " " + alerta 

            alerta_content = {
                "alerta":True,
                "visto":False,
                "mensaje":mensaje_alerta,
                "silo":silobolsa.id
            }

            alerta_enviar: TelemetryRecord = TelemetryRecord.model_validate(alerta_content)

            self._save_alerts(alerta_enviar)

            mensaje = f"🚨 *Alerta en Silo ID:* {silobolsa.id}\n*Ubicación:* {silobolsa.ubicacion}\n*Grano:* {silobolsa.grano}\n*Sensor ID:* `{sensor.id}`\n*Modelo:* {sensor.modelo}\n" + "\n".join(alertas)
    
            if sensor.id not in ultimas_alertas:
                self.notificator.send(mensaje)
                ultimas_alertas[sensor.id] = payload
            else:
                if payload.timestamp - ultimas_alertas[sensor.id].timestamp > timedelta(minutes=1):
                    self.notificator.send(mensaje)
                    ultimas_alertas[sensor.id] = payload
        else:

            if sensor.id in ultimas_alertas:
                ultimas_alertas.pop(sensor.id)
    


class GetSiloTelemetry:
    """Caso de uso para obtener los datos de telemetría de un silo de las últimas 24 horas."""

    def __init__(self, user_db: IUserDatabase, sensor_db: ISensorDatabase):
        self.user_db = user_db
        self.sensor_db = sensor_db

    def execute(self, silo_id: int, current_user_id: int) -> List[Dict[str, Any]]:
        # Verificamos que el silo exista y pertenezca al usuario
        silo: Silobolsa = self.user_db.get_entity(silo_id, Silobolsa)
        if silo.campo_id:
            campo: Campo = self.user_db.get_entity(silo.campo_id, Campo)

        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Silo")

        if not silo.sensor_id:
            raise AppError("El silobolsa no tiene un sensor vinculado.", 404)

        query = f"""
            SELECT time, co2, hum, temp
            FROM sensores_silo
            WHERE sensor_id = '{silo.sensor_id}'
            AND time >= now() - interval '24 hours'
            ORDER BY time ASC
        """

        return self.sensor_db.get_data(query)

### Instrucciones

Una vez creada la instancia de influxdb3-core es necesario crear el "operator token" para esto hay que ingresar a la shell del contenedor de la instancia de influxdb3 y correr el siguiente comando:


´
influxdb3 create token --admin
´

Luego almacenar el token en un archivo .env

Para crear la base de datos solo tienen que correr en la terminal:

´´´
influxdb3 create database (nombre de la base de datos) --token (operator token obtenido previamente)
´´´
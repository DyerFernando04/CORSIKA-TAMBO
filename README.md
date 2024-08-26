# HEP-PUCP

### Repositorio del equipo TAMBO del Grupo de Altas Energías de la PUCP

## Funcionamiento del bot de discord en conjunto con el script de ejecuciones.

COMO INICIAR EL BOT DE DISCORD:

Cargar main.py, responses.py y un .env que contanga el token del bot de discord (TOKEN=) en el mismo directorio que el script de ejecuciones de corsika.

Instalar las siguientes librerias de python: Python-dotenv, Discord. El bot funciona con la version 3.11 de python.

Dentro del archivo responses.py y del script de ejecuciones, modificar el path de statuslog.txt, este debe estar ubicado en el mismo directorio que el script de ejecuciones y el .py del bot. Además,tener en cuenta que statuslog.txt es creado automaticamente por el script de ejecuciones.

Actualizar los paths en el script de ejecuciones de corsika como indican los comentarios en el script.

Para iniciar el bot, abrir una terminal en la ubicacion de main.py y ejecutar el comando "python3 main.py". Esto debe hacerse en una terminal aparte de la que se usa para correr el script de ejecuciones.


COMO USAR EL BOT.

Tras agregar el bot a su servidor de discord, podrá usar los siguientes comandos.
>\>bot status           : Para confirmar que el bot se encuentra en linea

>\>simulation status    : Para verificar el estado de la simulación actual. permite ver la energía primaria, el tiempo que lleva simulando con esa energía, y el tiempo total desde que se iniciaron todas las simulaciones. Además si la simulación fue completada, se mostrará un mensaje que lo indique junto con la hora a la cual terminó.

>\>simulation info      : Muestra el rango de energías y el paso que se está utilizando. Además muestra la hora de inicio de todas las simulaciones.

>\>current time         : Muestra la hora local en el servidor en el cual se está ejecutando el bot.

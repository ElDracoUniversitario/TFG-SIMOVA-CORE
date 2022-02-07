import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from datetime import datetime
import consulta

reader = SimpleMFRC522()

try:

        id, text = reader.read()
        db = consulta.conexion()
        firma = consulta.genera_firma()
        
        text = input('A que DNI se va a vincular la tarjeta:')
        consulta.registra_soporte(db,id,text,firma)
        print("Aproxime tarjeta:")
        reader.write(firma)
        consulta.actualiza_firma(db,id,firma)
        print("Tajeta" +str(id)+ "con DNI:"+ text+ "Firmada: "+firma)
finally:
        GPIO.cleanup()

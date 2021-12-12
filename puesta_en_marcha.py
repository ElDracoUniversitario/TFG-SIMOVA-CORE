import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from datetime import datetime
import consulta

reader = SimpleMFRC522()

try:
        db = consulta.conexion()
        id, text = reader.read()
        firma = consulta.genera_firma()
        
        text = input('A que DNI se va a vincular la tarjeta:')
        consulta.registra_soporte(db,id,text,firma)
        print("Aproxime tarjeta:")
        reader.write(firma)
        consulta.actualiza_firma(db,id,firma)
        print("Tajeta" +id+ "con DNI:"+ text+ "Firmada: "+text)
finally:
        GPIO.cleanup()
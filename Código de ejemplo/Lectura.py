import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import consulta
from datetime import datetime

reader = SimpleMFRC522()

#db = consulta.conexion()


try:
    while True:
        db = consulta.conexion()
        id, text = reader.read()
        print(id)
        print(type(id))
        print(text)
        print(type(text))
        hash_fecha = consulta.validacion(db,id,text)
        print(hash_fecha)
        print(type(hash_fecha))
        reader.write(hash_fecha)
        print("Written: "+ hash_fecha)
        consulta.cerrar_conexion(db)

        
        
finally:
        GPIO.cleanup()

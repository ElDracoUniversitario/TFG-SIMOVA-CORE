import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import consulta
import time
from datetime import datetime

reader = SimpleMFRC522()



try:
    while True:
        id, text = reader.read()
        db = consulta.conexion()
        print(id)
        print(type(id))
        print(text)
        print(type(text))
        hash_fecha_int = consulta.validacion(db,id,text)
        hash_fecha = str(hash_fecha_int)
        
        print(hash_fecha)
        print(type(hash_fecha))
        reader.write(hash_fecha)
        print("Written: "+ hash_fecha)
        consulta.cerrar_conexion(db)
        time.sleep(1)

        
        
finally:
        GPIO.cleanup()

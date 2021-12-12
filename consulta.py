import pymysql
from datetime import datetime
import random

def conexion():
    
    db = pymysql.connect(host='145.14.151.1',user='u989932990_simova',password='~IiQcM&>L3',database='u989932990_simova')
    
    return db

def consulta_usuario(db):
    
    cursor = db.cursor()

    sql = "SELECT * FROM usuario"

    cursor.execute(sql)

    resultados = cursor.fetchall()

    for row in resultados:
        dni = row[0]
        email = row[1]
        nombre = row[2]
        apellido1 = row[3]
        apellido2 = row[4]
        print("El usuario con dni {0}, se llama {1} {2} {3}, y tiene el email {4}".format(dni, nombre, apellido1, apellido2, email))
    return
    
def validacion(db,num_soporte,hash_fecha):
    cursor = db.cursor()

    sql = "SELECT * FROM soporte WHERE uid_soporte = '" + str(num_soporte) +"'"
    #print("{0}".format(sql))

    cursor.execute(sql)

    resultados = cursor.fetchall()
    
    vuelta = 2

    for row in resultados:
        dni = row[1]
        bloqueo = row[2]
        titulo = row[3]
        nombre_de_titulo = nombre_titulo(db,titulo)
        zonas = row[5]
        firma = row[7]
        if bloqueo == 0:
            es_bloqueo = 'no'
        else:
            es_bloqueo = ''
        
        print("El soporte {0} {1} está bloqueado y pertenece al usuario con dni {2}, tiene el título {3} de {4} zonas".format(num_soporte, es_bloqueo, dni, nombre_de_titulo, zonas))
    if bloqueo == 0:
        if titulo != 0:
            estado = 1
        if titulo == 0:
            estado = 0
    else:
        estado = 0
    #if firma == hash_fecha:
    #    estado = 1
    #else:
    #    estado = 0
    hecho = viaje(db,num_soporte,estado)
    
    if hecho == 1:
        vuelta = genera_firma()
        actualiza_firma(db, num_soporte, vuelta)    
        
    return vuelta
    #if bloqueo == 0:
    
    #cursor.execute(sql)

def genera_firma():
    fecha = datetime.now()
    print(fecha)
    to_integer = fecha.strftime('%Y%m%d%H%M%S')
    print(to_integer)
    hash_fecha =hash(to_integer)
    print(hash_fecha)
    vuelta =str(hash_fecha)
    return vuelta

def actualiza_firma(db, num_soporte, vuelta):
    cursor = db.cursor()
    sql = "UPDATE `soporte`SET `firma` = %s WHERE `uid_soporte`= %s"
    cursor.execute(sql,(vuelta, num_soporte))
    db.commit()
    

def nombre_titulo(db,num_titulo):
    cursor = db.cursor()

    sql = "SELECT * FROM titulo WHERE uid_titulo = '" + str(num_titulo) +"'"
    #print("{0}".format(sql))

    cursor.execute(sql)

    resultados = cursor.fetchall()

    for row in resultados:
        nombre = row[1]
        numero_viajes = row[2]
        caducidad = row[3]
        ilimitado = row[4]
        if ilimitado == 0:
            es_ilimitado = 'No e'
        else:
            es_ilimitado = 'E'
        
        print("El titulo {0} es una {1}. {2}s Ilimitado y tiene una uso de {3}días continuados".format(num_titulo, nombre, es_ilimitado, caducidad))
    return nombre

def viaje(db,num_soporte,estado):
    cursor = db.cursor()

    sql = "INSERT INTO `historico`(`uid_soporte`, `uid_historico`, `fecha`, `hora`, `estatus`, `estacion`) VALUES (%s,%s,%s,%s,%s,%s)"

    fecha1 = datetime.today().strftime('%Y-%m-%d')
    hora1 = datetime.today().strftime('%H:%M:%S')
    estaciones_test =['101534','102763','103601']
    estacion = random.choice(estaciones_test)
    print("La estación será {0}".format(estacion))

    cursor.execute(sql,(num_soporte,'',fecha1,hora1,estado,estacion))
    db.commit()
    
    if estado == 1:
        print("El soporte {0} ha realizado un viaje correcto a las {1} del {2} en la estación {3} ".format(num_soporte, hora1, fecha1, estacion))
    else:
        print("El soporte {0} no ha realizado la validación por no disponer de un título válido".format(num_soporte))

    return estado

def registra_soporte(db,num_soporte,dni,firma):
    cursor = db.cursor()

    sql = "INSERT INTO `soporte`(`uid_soporte`, `dni_asociado`, `bloqueo`, `titulo`, `fecha_primer_uso`, `zonas`, `viajes_restantes`, `firma`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.execute(sql,(num_soporte,dni,0,0,'',0,0,firma))
    db.commit()
    
    print("El soporte {0} ha sido vinculado al DNI: {1} con la firma : {2}".format(num_soporte, dni, firma))

    return 

def cerrar_conexion(db):
    db.close()
    return

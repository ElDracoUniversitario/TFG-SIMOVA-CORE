import pymysql
from datetime import datetime

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
    
def validacion(db,num_soporte):
    cursor = db.cursor()

    sql = "SELECT * FROM soporte WHERE uid_soporte = '" + str(num_soporte) +"'"
    #print("{0}".format(sql))

    cursor.execute(sql)

    resultados = cursor.fetchall()

    for row in resultados:
        dni = row[1]
        bloqueo = row[2]
        titulo = row[3]
        nombre_de_titulo = nombre_titulo(db,titulo)
        zonas = row[5]
        if bloqueo == 0:
            es_bloqueo = 'no'
        else:
            es_bloqueo = ''
        
        print("El soporte {0} {1} está bloqueado y pertenece al usuario con dni {2}, tiene el título {3} de {4} zonas".format(num_soporte, es_bloqueo, dni, nombre_de_titulo, zonas))
    if bloqueo == 0:
        viaje(db,num_soporte)
    return
    #if bloqueo == 0:
    
    #cursor.execute(sql)

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

def viaje(db,num_soporte):
    cursor = db.cursor()

    sql = "INSERT INTO `historico`(`uid_soporte`, `uid_historico`, `fecha`, `hora`, `estatus`, `estacion`) VALUES (%s,%s,%s,%s,%s,%s)"

    fecha1 = datetime.today().strftime('%Y-%m-%d')
    hora1 = datetime.today().strftime('%H:%M:%S')

    cursor.execute(sql,(num_soporte,'',fecha1,hora1,1,101534))
    db.commit()
    return 
    

def cerrar_conexion(db):
    db.close()
    return

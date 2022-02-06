import pymysql

import datetime

import random

def conexion():
    '''Esta función establece la conexión con la base de datos y la debuelve para que los métodos puedan realizar las consultas  '''
    
    db = pymysql.connect(host='145.14.151.1',user='u989932990_simova',password='~IiQcM&>L3',database='u989932990_simova')
    
    return db

def consulta_usuario(db):
    '''Esta función consulta todos los usuarios de la tabla'''

    
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
    cursor.close()
    return
    
def validacion(db,num_soporte,hash_fecha):
    '''Esta función consulta en la base de datos la información realtiva a un UID  de un soporte
       realiza las comprovaciones sobre si el título está bloqueado o no, dispone un título válido
       para viajar y actualiza la fecha de caducidad. Al finalizar, registra el viaje y actualiza
       la firma de la tarjeta. Todo ello con sus propios métodos.
    '''
    
    cursor = db.cursor()

    sql = "SELECT * FROM soporte WHERE uid_soporte = '" + str(num_soporte) +"'"

    cursor.execute(sql)

    resultados = cursor.fetchall()
    
    cursor.close()
    
    vuelta = 2

    for row in resultados:
        dni = row[1]
        bloqueo = row[2]
        titulo = row[3]
        nombre_de_titulo = nombre_titulo(db,titulo)
        fecha = row[4]
        print("fechas: {0}".format(fecha))
        zonas = row[5]
        viajes_restantes = row[6]
        firma = row[7]
        hecho = 0
        if bloqueo == 0:
            es_bloqueo = 'no'
        else:
            es_bloqueo = ''
        
        print("El soporte {0} {1} está bloqueado y pertenece al usuario con dni {2}, tiene el título {3} de {4} zonas".format(num_soporte, es_bloqueo, dni, nombre_de_titulo, zonas))
    if bloqueo == 0:
        if titulo != 0:
            estado = 1
        if titulo == 0:
            estado = 2
        if fecha != '0':
            if fecha == '1':
                caducidad = caducidad_titulo(db, titulo)
                print("{0} es el que va".format(caducidad))
            else:
                caducidad = fecha
            estado = comprueba_fecha(fecha, caducidad)
            print("estado:{0}".format(estado))
    else:
        estado = 0
    
        
    if titulo == 3:
        if viajes_restantes > 0:
            viajes = viajes_restantes - 1;
            hecho = viaje(db,num_soporte,estado,titulo,viajes)
    else:
        viajes = 0
        hecho = viaje(db,num_soporte,estado,titulo,viajes)
        
    
    if hecho == 1:
        vuelta = genera_firma()
        actualiza_firma(db, num_soporte, vuelta)
        if fecha == '1':
            actualiza_fecha_caducidad(db,num_soporte, caducidad)
    
    
        
    return vuelta


def actualiza_fecha_caducidad(db,num_soporte, caducidad):
    """Esta función actualiza la fecha de caducidad del título del soporte """
    
    cursor = db.cursor()
    sql = "UPDATE `soporte`SET `fecha_caducidad` = %s WHERE `uid_soporte`= %s"

    fecha1 = datetime.date.today() + datetime.timedelta(days=int(caducidad))

    cursor.execute(sql,(fecha1,num_soporte))
    db.commit()
    cursor.close()



def comprueba_fecha(fecha_bd, caducidad):
    '''Esta función comprueba si el título está caducado, comparando la fecha actual y la fecha de caducidad. '''
    
    print("{0} Es la caducidad".format(caducidad))
    fecha_hoy = datetime.date.today()
    
    if fecha_bd == '1':
        fecha_bd = fecha_hoy + datetime.timedelta(days=int(caducidad))
        print("{0} Es al fecha de caducidad".format(fecha_bd))
    
    fecha_bd_split = str(fecha_bd).split('-')
    print("{0}-{1}-{2}".format(fecha_bd_split[0],fecha_bd_split[1], fecha_bd_split[2]))
    fecha_bd_convert = datetime.date(int(fecha_bd_split[0]),int(fecha_bd_split[1]), int(fecha_bd_split[2]))
    
    if fecha_hoy <= fecha_bd_convert:
        estado = 1
    else:
        estado = 3
    
    return estado
    

def consulta_fecha():
    '''Esta función obtiene y devuelve la fecha actual '''
    
    fecha = date.today()
    print(fecha)
    return fecha
    

def consulta_fecha_hora():
    '''Esta función obtiene y devuelve la fecha y hora actual '''
    
    fecha = datetime.datetime.now()
    print(fecha)
    to_integer = fecha.strftime('%Y-%m-%d %H:%M:%S')
    print(to_integer)
    return to_integer
    


def genera_firma():
    '''Esta función genera una firma con haciendo un hash de la fecha y hora actual'''
    
    to_integer = consulta_fecha_hora()
    hash_fecha =hash(to_integer)
    print(hash_fecha)
    vuelta = str(hash_fecha)
    return vuelta

def actualiza_firma(db, num_soporte, vuelta):
    '''Esta función oactualiza en la base de datos la firma del soporte '''
    
    cursor = db.cursor()
    sql = "UPDATE `soporte`SET `firma` = %s WHERE `uid_soporte`= %s"
    cursor.execute(sql,(vuelta, num_soporte))
    db.commit()
    cursor.close()
    

def nombre_titulo(db,num_titulo):
    '''Esta función obtiene el nombre de un título en concreto'''
    
    cursor = db.cursor()

    sql = "SELECT * FROM titulo WHERE uid_titulo = '" + str(num_titulo) +"'"

    cursor.execute(sql)

    resultados = cursor.fetchall()

    for row in resultados:
        nombre = row[1]

    cursor.close()
    return nombre

def caducidad_titulo(db,num_titulo):
    '''Esta función obtiene la informacón de un título en concreto y devuelve su fecha de caducidad'''
    
    cursor = db.cursor()

    sql = "SELECT * FROM titulo WHERE uid_titulo = '" + str(num_titulo) +"'"

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
    cursor.close()
    return caducidad

def viaje(db,num_soporte,estado,titulo, viaje):
    '''Esta función inserta en el historico el viaje dejando reflejados, feecha y hora, estación,
    la información del título y su estado'''
    
    
    viaje_restantes(db,num_soporte,estado,titulo, viaje)
    cursor = db.cursor()

    sql = "INSERT INTO `historico`(`uid_soporte`, `uid_historico`, `fecha`, `hora`, `estatus`, `estacion`, `titulo`) VALUES (%s,%s,%s,%s,%s,%s,%s)"

    fecha1 = datetime.datetime.today().strftime('%Y-%m-%d')
    hora1 = datetime.datetime.today().strftime('%H:%M:%S')
    estaciones_test =['101534','102763','103601']
    estacion = random.choice(estaciones_test)
    print("La estación será {0}".format(estacion))

    cursor.execute(sql,(num_soporte,'',fecha1,hora1,estado,estacion, titulo))
    db.commit()
    
    if estado == 1:
        print("El soporte {0} ha realizado un viaje correcto a las {1} del {2} en la estación {3} ".format(num_soporte, hora1, fecha1, estacion))
    else:
        print("El soporte {0} no ha realizado la validación por no disponer de un título válido".format(num_soporte))
    cursor.close()
    return estado

def viaje_restantes(db,num_soporte,estado,titulo, viaje):
    '''Esta función obtiene el número de viajes restantes en un soporte'''

    
    cursor = db.cursor()
    sql = "UPDATE `soporte`SET `viajes_restantes` = %s WHERE `uid_soporte`= %s"
    cursor.execute(sql,(viaje, num_soporte))
    db.commit()
    cursor.close()

def registra_soporte(db,num_soporte,dni,firma):
    '''Esta función la utiliza la administración para vincular un soporte con un usuario'''
    
    
    cursor = db.cursor()

    sql = "INSERT INTO `soporte`(`uid_soporte`, `dni_asociado`, `bloqueo`, `titulo`, `fecha_caducidad`, `zonas`, `viajes_restantes`, `firma`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.execute(sql,(num_soporte,dni,0,0,'',0,0,firma))
    db.commit()
    
    print("El soporte {0} ha sido vinculado al DNI: {1} con la firma : {2}".format(num_soporte, dni, firma))
    cursor.close()
    return 

def cerrar_conexion(db):
    db.close()
    return

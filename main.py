import consulta
#comm
db = consulta.conexion()

consulta.consulta_usuario(db)

consulta.validacion(db,'1')

consulta.cerrar_conexion(db)

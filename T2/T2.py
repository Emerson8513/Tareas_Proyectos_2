import psycopg2 as pg2

try:
    connection = pg2.connect(
        host = 'localhost',
        user = 'emerson',
        password = 'kuto',
        database = 'prueba_db'
    )
    print('\n*__ Conexión exitosa __*\n')
    connection.autocommit = True
    selec = connection.cursor()
    table = 'redes'
    opcion = input("¿Qué desea hacer? \n1)Ingresar Datos \n2)Eliminar Datos \n3)Actualizar Datos \n4)Visualizar Datos \nRespuesta : ")
    if opcion == '1':
    #  Ingresar Datos a la tabla
        numero = input("Ingrese cuantos registros desea insertar: ")
        for i in range(int(numero)):
            carnet = input("Ingrese el carnet: ")
            nombre = input("Ingrese el nombre: ")
            selec.execute(f"INSERT INTO {table} VALUES ('{nombre}', '{carnet}')")
    # Eliminar Datos de la tabla
    if opcion == '2':
        numerod = input("Ingrese cuantos registros desea eliminar: ")
        for i in range(int(numerod)):
            carnet = input("Ingrese el carnet: ")
            selec.execute(f"DELETE FROM {table} WHERE carnet = '{carnet}'")
    # Actualizar Datos de la tabla
    if opcion == '3':
        numeroa = input("Ingrese cuantos registros desea actualizar: ")
        for i in range(int(numeroa)):
            actualizar = input("QUE DESEA ACTUALIZAR: 1)CARNET 2)NOMBRE: ")
            if actualizar == '1':
                carnet = input("Ingrese el carnet: ")
                nombre = input("Ingrese el nombre: ")
                selec.execute(f"UPDATE {table} SET carnet = '{carnet}' WHERE nombre = '{nombre}'")
            elif actualizar == '2':
                nombre = input("Ingrese el nombre: ")
                carnet = input("Ingrese el carnet: ")
                selec.execute(f"UPDATE {table} SET nombre = '{nombre}' WHERE carnet = '{carnet}'")
    if opcion == '4':
        selec.execute(f"SELECT * FROM {table}")
        datos = selec.fetchall()
        for i in datos:
            print(i)
    if opcion > '4' and opcion < '1':
        print('Opción no válida')
except Exception as ex:
    print('Error de conexión: ', ex)
connection.commit()
selec.close()
connection.close()
import psycopg2 

try:
    conn = psycopg2.connect(
            dbname="parqueo",
            user="postgres",
            password="kuto",
            host="localhost",
            port="5432"
    )
    cursor = conn.cursor()

    print("Conexión exitosa")
    create_table_query = '''
            CREATE TABLE IF NOT EXISTS parqueo (
            Usuario VARCHAR(50),
            carnet int NOT NULL
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()

    print("Tabla creada")

    print('\n*__ Conexión exitosa __*\n')
    conn.autocommit = True
    selec = conn.cursor()
    table = 'parqueo'
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
conn.commit()
selec.close()
conn.close()
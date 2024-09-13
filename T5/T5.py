import psycopg2

conn = psycopg2.connect(
    dbname="imc",
    user="postgres",
    password="kuto",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

pajoPeso = "Bajo Peso" # < 80
pesoNormal = "Peso Normal" # 81 - 150
sobrePeso = "Sobrepeso" # > 150
ditectory = 'E:/perez/Documentos/Cursos 2do. Semestre 2024/PROYECTOS DE COMPUTACION APLICADA A I.E. Sección P/Tareas Proyectos/imc/'
filename = ""

opcion = 0
opcionu = 0
while opcion != 5:
    print('Seleccione una Opción: ')
    print('1. Usuario')
    print('2. Calcular IMC y Mostrar Resultados')
    print('3. Leer Archivo')
    print('4. Borrar Información')
    print('5. Salir')
    opcion = int(input('Ingrese su Elección: '))

    if opcion == 1:
        try:
            while opcionu != 4:
                print('Seleccione una Opción: ')
                print('1. Añadir Usuario')
                print('2. Actualizar Usuario')
                print('3. Borrar Usuario')
                print('4. Salir')
                opcionu = int(input('Ingrese la Opción: '))

                if opcionu == 1:
                    print('Añadiendo usuario...')
                    nombre = input('Ingrese el Nombre del Usuario: ')
                    altura = float(input('Ingrese la Altura del Usuario en CM: '))
                    if altura <= 0 or altura.is_integer() == False:
                        while altura <= 0 or altura.is_integer() == False:
                            print('Error: Altura no válida.')
                            altura = float(input('Ingrese la Altura del Usuario en CM: '))

                    peso = float(input('Ingrese el Peso del Usuario en Libras: '))
                    if peso <= 0:
                        while peso <= 0:
                            print('Error: Peso no válido.')
                            peso = float(input('Ingrese el Peso del Usuario en Libras: '))

                    cursor.execute("INSERT INTO imc (nombre, peso, altura) VALUES (%s, %s, %s);", (nombre, peso, altura))
                    conn.commit()
                    print('Usuario añadido...')

                elif opcionu == 2:
                    nombre = input('Ingrese el Nombre del Usuario: ')

                    altura = float(input('Actualizar Altura del Usuario en CM: '))
                    if altura <= 0:
                        while altura <= 0:
                            print('Error: Altura no válida.')
                            altura = float(input('Actualizar la Altura del Usuario en CM: '))

                    peso = float(input('Actualizar el Peso del Usuario en Libras: '))
                    if peso <= 0:
                        while peso <= 0:
                            print('Error: Peso no válido.')
                            peso = float(input('Actualizar el Peso del Usuario en Libras: '))

                    cursor.execute("UPDATE imc SET peso = %s, altura = %s WHERE nombre = %s;", (peso, altura, nombre))
                    conn.commit()
                    print('Usuario actualizado...')

                elif opcionu == 3:
                    nombre = input('Ingrese el Nombre del Usuario a Borrar: ')

                    cursor.execute("DELETE FROM imc WHERE nombre = %s;", (nombre,))
                    conn.commit()
                    print('Usuario borrado...')

                elif opcionu == 4:
                    print('Saliendo del Menú de Usuario...')

                else:
                    print('Opción no válida.')
        except Exception as e:
            print('Error al gestionar el usuario', e)

    elif opcion == 2:
        try:
            nombre_usuario = input('Ingrese el Nombre: ')
            cursor.execute("SELECT peso, altura FROM imc WHERE nombre = %s;", (nombre_usuario,))
            result = cursor.fetchone()
            filename = ditectory + nombre_usuario + '.txt'
            if result is None:
                print('Usuario no encontrado o datos vacíos')
            else:
                peso, altura = result

                if peso < 80:
                    estado = pajoPeso
                elif 81 <= peso <= 150:
                    estado = pesoNormal
                else:
                    estado = sobrePeso

                if peso <= 0 or altura <= 0:
                    print('Error: Los valores de peso y altura no son inválidos.')
                else:
                    imc = (peso * 0.453592) / ((altura / 100) ** 2)
                    print(f'Peso: {peso} libras')
                    print(f'Altura: {altura} cm')
                    print(f'IMC: {imc}')
                    print(f'Estado: {estado}')
                    
                    with open(filename, 'w') as file:
                        file.write(f'Usuario: {nombre_usuario}\n')
                        file.write(f'Peso: {peso:.2f} Libras\n')
                        file.write(f'Altura: {altura:.2f} CM\n')
                        file.write(f'IMC: {imc:.2f}\n')
                        file.write(f'Estado: {estado}\n')

        except Exception as e:
            print('Error al calcular y mostrar el IMC', e)

    elif opcion == 3:
        readUserFile = input('Ingrese el nombre del archivo a leer: ')
        filename = ditectory + readUserFile + '.txt'    
        try:
            with open(filename, 'r') as file:
                for line in file:
                    print(line.strip())
        except Exception as e:
            print('Error al leer el archivo', e)

    elif opcion == 4:
        try:
            with open(filename, 'w') as file:
                pass
            print('Información borrada del archivo.')
        except Exception as e:
            print('Error al borrar la información del archivo', e)

    elif opcion == 5:
        print('Saliendo del Programa')
        print('Gracias por usar el programa')

    else:
        print('Opción no válida')

cursor.close()
conn.close()

import time

print("Inicio del programa")

tiempo = time.ctime(time.time())

print(f"Tiempo actual: {tiempo}")

tiempo_actual = time.localtime()
print(f"Tiempo actual: {tiempo_actual}")
print(type(tiempo_actual))

tiempo = time.strftime("%H:%M:%S", tiempo_actual)
print(f"Tiempo actual: {tiempo}")
print(type(tiempo))


hora_in = time.strftime("%H", tiempo_actual)
minutos_in = time.strftime("%M", tiempo_actual)


print(f"Hora: {hora_in}")
print(f"Minutos: {minutos_in}")
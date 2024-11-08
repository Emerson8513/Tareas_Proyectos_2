 

def es_palindromo(cadena):
    """Determina si una cadena es un palíndromo."""
    return cadena == cadena[::-1]
def es_primo(numero):
    """Determina si un número es primo."""
    if numero <= 1:
        return False
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:
            return False
    return True

def es_perfecto(numero):
    """Determina si un número es perfecto."""
    suma_divisores = 0
    for i in range(1, numero):
        if numero % i == 0:
            suma_divisores += i
    return suma_divisores == numero

def menu():
    """Muestra el menú de opciones y realiza las operaciones correspondientes."""
    while True:
        print("\nMenú:")
        print("1. Detectar palíndromo")
        print("2. Detectar número primo")
        print("3. Detectar número perfecto")
        print("4. Salir")
        opcion = int(input("Ingrese una opción: "))

        if opcion == 1:
            cadena = input("Ingrese una cadena: ")
            if es_palindromo(cadena):
                print("La cadena es un palíndromo.")
            else:
                print("La cadena no es un palíndromo.")
        elif opcion == 2:
            numero = int(input("Ingrese un número: "))
            if es_primo(numero):
                print("El número es primo.")
            else:
                print("El número no es primo.")
        elif opcion == 3:
            numero = int(input("Ingrese un número: "))
            if es_perfecto(numero):
                print("El número es perfecto.")
            else:
                print("El número no es perfecto.")
        elif opcion == 4:
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
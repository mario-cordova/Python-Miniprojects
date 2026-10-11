def kelvin_celsius(k):
    c = k - 273.15
    return c

def kelvin_fahrenheit(k):
    f = 9 * (k - 273.15) / 5 + 32
    return f

def celsius_kelvin(c):
    k = c + 273.15
    return k

def celsius_fahrenheit(c):
    f = 9 * c / 5 + 32
    return f

def fahrenheit_celsius(f):
    c = 5 * (f - 32) / 9
    return c

def fahrenheit_kelvin(f):
    k = 5 * (f - 32) / 9 + 273.15
    return k

while True:
    opcion = input("""Seleccione una opción:
    1.- Convertir Kelvin a celsius
    2.- Convertir Kelvin a Fahrenheit
    3.- COnvertir celsius a Kelvin
    4.- Convertir celsius a Fahrenheit
    5.- Convertir Fahrenheit a celsius
    6.- Convertir Fahrenheit a Kelvin
    7.- Salir
    >>> """)
    if opcion == '1':
        k = int(input('Ingrese la temperatura Kelvin: '))
        c = kelvin_celsius(k)
        print(c)
    elif opcion == '2':
        k = int(input('Ingrese la temperatura Kelvin: '))
        f = kelvin_fahrenheit(k)
        print(f)
    elif opcion == '3':
        c = int(input('Ingrese la temperatura celsius: '))
        k = celsius_kelvin(c)
        print(k)
    elif opcion == '4':
        c = int(input('Ingrese la temperatura celsius: '))
        f = celsius_fahrenheit(c)
        print(f)
    elif opcion == '5':
        f = int(input('Ingrese la temperatura Fahrenheit: '))
        c = fahrenheit_celsius(f)
        print(c)
    elif opcion == '6':
        f = int(input('Ingrese la temperatura Fahrenheit: '))
        k = fahrenheit_kelvin(f)
        print(k)
    elif opcion == '7':
        break
    else:
        print('Error, opción no encontrada')
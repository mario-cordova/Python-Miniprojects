import random
from pick import pick

def calculador_horas(cantidad_grupos, grupos):
    horas_total = 0
    materias = ['Matemáticas', 'Español', 'Biología', 'Física', 'Química', 'Historia (Primer grado)', 'Historia (Segundo/Tercer grado)', 'Geografía', 'Cívica', 'Integración Curricular', 'Formación Humana', 'Artes', 'Tecnología']
    for i in range(cantidad_grupos):
        grupo_actual = grupos[i]
        materia, index = pick(materias, f'Seleccione la materia que le imparte a {grupo_actual}', indicator='=>', default_index=0)
        if materia in ('Física', 'Química'):
            horas_materia = 6
        elif materia in ('Matemáticas', 'Español'):
            horas_materia = 5
        elif materia in ('Biología', 'Historia (Segundo/Tercer grado)', 'Geografía'):
            horas_materia = 4
        elif materia in ('Tecnología', 'Artes'):
            horas_materia = 3
        elif materia in ('Cívica', 'Historia (Primer grado)'):
            horas_materia = 2
        else:
            horas_materia = 1
        if horas_total + horas_materia > 37:
            break
        horas_total += horas_materia
    return horas_total
    
def grupos_(cantidad_grupos):
    grupos = []
    for i in range(cantidad_grupos):
        grupos.append(input(f'Escriba el grado y grupo (Ej. 3A) de los {cantidad_grupos} grupos: '))
    return grupos

def titular(grupos):
    es_titular = input('¿Coordinación dijo que usted sera maestro titular (Los maestros de Arte y Tecnología NO pueden ser titulares)? (si/no): ')
    if es_titular == 'si':
        grupo_titular = random.choice(grupos)
        hora_orientacion = 1
    else:
        grupo_titular = None
        hora_orientacion = 0
    return grupo_titular, hora_orientacion

docente = input('Ingrese su nombre: ')
docente_ingles = input('¿Es docente de inglés? (si/no): ')
if docente_ingles == 'si':
    horas_total = 36
    grupo_titular = 'El departamento de inglés le comunicara sobre su grupo titular.'
    hora_orientacion = 0
else:
    cantidad_grupos = int(input('Cantidad de grupos a los que les imparte clase: '))
    grupos = grupos_(cantidad_grupos)
    horas_total = calculador_horas(cantidad_grupos, grupos)
    grupo_titular, hora_orientacion = titular(grupos)
print(docente+', su carga laboral es de:', horas_total + hora_orientacion, 'horas.  Su grupo titular es:', grupo_titular)
import random
from pick import pick

MATERIAS = [
    'Matemáticas',
    'Español',
    'Biología',
    'Física',
    'Química',
    'Historia (Primer grado)',
    'Historia (Segundo/Tercer grado)',
    'Geografía',
    'Cívica',
    'Integración Curricular',
    'Formación Humana',
    'Artes Visuales',
    'Artes Escénicas',
    'Música',
    'Tecnología'
]

# Materias que NO se imparten en cada grado
# (primero solo Biología, segundo solo Física, tercero solo Química)
MATERIAS_EXCLUIDAS = {
    1: ('Física', 'Química', 'Historia (Segundo/Tercer grado)'),
    2: ('Biología', 'Química', 'Historia (Primer grado)', 'Geografía'),
    3: ('Biología', 'Física', 'Historia (Primer grado)', 'Geografía'),
}

# Quien imparta alguna de estas materias no puede ser titular
MATERIAS_SIN_TITULARIDAD = (
    'Artes Visuales',
    'Artes Escénicas',
    'Música',
    'Tecnología'
)

LIMITE_HORAS = 37
HORAS_ORIENTACION = 1
HORAS_INGLES = 36
OPCION_TERMINAR = '>> Terminar selección de grupos'


def horas_materia(materia):
    if materia in ('Física', 'Química'):
        return 6
    elif materia in ('Matemáticas', 'Español'):
        return 5
    elif materia in ('Biología', 'Historia (Segundo/Tercer grado)', 'Geografía'):
        return 4
    elif materia in ('Tecnología', 'Artes Visuales', 'Artes Escénicas', 'Música'):
        return 3
    elif materia in ('Cívica', 'Historia (Primer grado)'):
        return 2
    else:
        return 1


def materias_del_grado(grado):
    excluidas = MATERIAS_EXCLUIDAS[grado]

    return [materia for materia in MATERIAS if materia not in excluidas]


def obtener_grado(nombre_grupo):
    """
    Si el nombre del grupo empieza con 1, 2 o 3 (por ejemplo '1A', '2B'),
    ese es el grado. Si no, se le pregunta al usuario.
    """
    primer_caracter = nombre_grupo[:1]

    if primer_caracter in ('1', '2', '3'):
        return int(primer_caracter)

    while True:
        respuesta = input(
            f'¿A qué grado pertenece el grupo {nombre_grupo}? (1/2/3): '
        ).strip()

        if respuesta in ('1', '2', '3'):
            return int(respuesta)

        print('Escriba 1, 2 o 3.')


def registrar_grupos(cantidad_grupos):
    grupos = []
    materias_por_grupo = {}
    grado_de_grupo = {}

    while len(grupos) < cantidad_grupos:
        nombre = input(f'Escriba el nombre del grupo {len(grupos) + 1}: ').strip()

        if not nombre:
            print('El nombre del grupo no puede estar vacío.')
            continue

        if nombre in grupos:
            print(f'El grupo {nombre} ya está registrado.')
            continue

        grado = obtener_grado(nombre)
        print(f'   Grado: {grado}°')

        grupos.append(nombre)
        materias_por_grupo[nombre] = materias_del_grado(grado)
        grado_de_grupo[nombre] = grado

    return grupos, materias_por_grupo, grado_de_grupo


def pedir_cantidad_materias(grupo, maximo):
    while True:
        respuesta = input(
            f'¿Cuántas materias le imparte al grupo {grupo}? (1-{maximo}): '
        )

        if respuesta.isdigit() and 1 <= int(respuesta) <= maximo:
            return int(respuesta)

        print(f'Escriba un número entre 1 y {maximo}.')


def seleccionar_grupos(grupos, asignaciones, materias_por_grupo):
    """
    El docente va eligiendo grupos de una lista. Por cada grupo indica
    cuántas materias le imparte. Cuando ya no quiera agregar más grupos,
    elige la opción de terminar.

    Regresa un diccionario {grupo: cantidad_de_materias}.
    """
    grupos_docente = {}

    while True:
        # Solo se ofrecen grupos que no ha elegido y que aún tengan
        # materias sin maestro asignado.
        grupos_disponibles = [
            grupo for grupo in grupos
            if grupo not in grupos_docente
            and len(asignaciones[grupo]) < len(materias_por_grupo[grupo])
        ]

        if not grupos_disponibles:
            print('\nYa no hay más grupos disponibles para seleccionar.')
            break

        opciones = grupos_disponibles.copy()
        titulo = 'Seleccione un grupo al que le da clase:'

        if grupos_docente:
            # El botón de terminar solo aparece cuando ya eligió al menos uno.
            opciones.append(OPCION_TERMINAR)

            resumen = ', '.join(
                f'{grupo} ({cantidad})'
                for grupo, cantidad in grupos_docente.items()
            )
            titulo += f'\nYa seleccionados (materias): {resumen}'

        opcion, index = pick(
            opciones,
            titulo,
            indicator='=>',
            default_index=0
        )

        if opcion == OPCION_TERMINAR:
            break

        materias_libres = (
            len(materias_por_grupo[opcion]) - len(asignaciones[opcion])
        )

        grupos_docente[opcion] = pedir_cantidad_materias(
            opcion,
            materias_libres
        )

    return grupos_docente


def calculador_horas(grupos_docente, asignaciones, materias_por_grupo, docente):
    """
    Regresa:
      - horas_total: horas de clase del docente
      - materias_docente: materias distintas que imparte
      - horas_por_grupo: {grupo: horas} solo de los grupos donde de verdad
        quedó con clase (sirve después para decidir titulares)
    """
    horas_total = 0
    materias_docente = []
    horas_por_grupo = {}

    for grupo_actual, cantidad in grupos_docente.items():
        for numero in range(1, cantidad + 1):
            materias_disponibles = [
                materia for materia in materias_por_grupo[grupo_actual]
                if materia not in asignaciones[grupo_actual]
            ]

            if not materias_disponibles:
                print(f'\n{grupo_actual} ya tiene todas las materias asignadas.')
                break

            materia, index = pick(
                materias_disponibles,
                f'Grupo {grupo_actual}: seleccione la materia {numero} de {cantidad}'
                f'\nHoras acumuladas: {horas_total}/{LIMITE_HORAS}',
                indicator='=>',
                default_index=0
            )

            horas = horas_materia(materia)

            if horas_total + horas > LIMITE_HORAS:
                print(
                    f'\nYa no puede agregar más horas porque superaría las {LIMITE_HORAS}.'
                )
                return horas_total, materias_docente, horas_por_grupo

            horas_total += horas

            asignaciones[grupo_actual][materia] = docente

            horas_por_grupo[grupo_actual] = (
                horas_por_grupo.get(grupo_actual, 0) + horas
            )

            if materia not in materias_docente:
                materias_docente.append(materia)

    return horas_total, materias_docente, horas_por_grupo


def buscar_pareja(nodo, candidatos, pareja_de, visitados):
    """
    Camino aumentante (emparejamiento): intenta darle pareja a 'nodo'
    (un grupo o un grado) con alguno de sus candidatos (docentes).
    Si el candidato ya tiene pareja, intenta que esa otra pareja se
    reacomode con otro candidato.

    pareja_de: {indice del docente: nodo al que está asignado}
    """
    for opcion in candidatos[nodo]:
        if opcion in visitados:
            continue

        visitados.add(opcion)

        if opcion not in pareja_de or buscar_pareja(
            pareja_de[opcion], candidatos, pareja_de, visitados
        ):
            pareja_de[opcion] = nodo
            return True

    return False


def asignar_titulares(grupos, docentes, grado_de_grupo):
    """
    Asigna un titular a cada grupo buscando que ninguno se quede sin maestro.

    Reglas:
      - Un docente solo puede ser titular de UN grupo.
      - Docentes que NO son de inglés: solo pueden ser titulares de un grupo
        donde dan clase, y no pueden serlo si imparten Artes, Música o
        Tecnología.
      - Docentes de inglés: pueden ser titulares de cualquier grupo.
      - Un grado no puede quedar completo con titulares de inglés: en cada
        grado al menos un grupo debe tener titular que no sea de inglés.

    Pasos:
      1) Se garantiza un titular que no sea de inglés por grado (emparejamiento
         grados <-> docentes, para que ningún grado se quede sin él si es posible).
      2) Con esas bases fijas, se cubren los demás grupos con docentes que no
         son de inglés, reacomodando lo necesario para cubrir el máximo posible.
      3) Los grupos que sigan sin titular se cubren con docentes de inglés,
         respetando la regla del grado.

    Entre varias opciones válidas se prefiere al docente que más horas da en
    el grupo (empates al azar).

    Regresa (titulares, grupo_de_docente, bloqueados):
      titulares        -> {grupo: nombre del docente}
      grupo_de_docente -> {indice del docente: grupo}
      bloqueados       -> grupos que se dejaron sin titular por la regla del grado
    """
    regulares = [
        i for i, docente in enumerate(docentes)
        if docente['puede_ser_titular'] and not docente['ingles']
    ]
    ingles = [i for i, docente in enumerate(docentes) if docente['ingles']]
    grados = sorted(set(grado_de_grupo[grupo] for grupo in grupos))

    # Candidatos por grupo (solo docentes que NO son de inglés)
    candidatos_grupo = {}

    for grupo in grupos:
        lista = [
            i for i in regulares
            if grupo in docentes[i]['horas_por_grupo']
        ]
        random.shuffle(lista)
        lista.sort(
            key=lambda i: docentes[i]['horas_por_grupo'][grupo],
            reverse=True
        )
        candidatos_grupo[grupo] = lista

    # Candidatos por grado: docentes que dan clase en algún grupo de ese grado
    candidatos_grado = {}

    for grado in grados:
        lista = [
            i for i in regulares
            if any(
                grado_de_grupo[grupo] == grado
                for grupo in docentes[i]['horas_por_grupo']
            )
        ]
        random.shuffle(lista)
        candidatos_grado[grado] = lista

    # Paso 1: un titular que no sea de inglés por grado
    pareja_grado = {}

    for grado in sorted(grados, key=lambda g: len(candidatos_grado[g])):
        buscar_pareja(grado, candidatos_grado, pareja_grado, set())

    pareja_grupo = {}

    for i, grado in pareja_grado.items():
        # Se ancla en el grupo de ese grado donde el docente da más horas
        grupo_ancla = max(
            (g for g in docentes[i]['horas_por_grupo'] if grado_de_grupo[g] == grado),
            key=lambda g: docentes[i]['horas_por_grupo'][g]
        )
        pareja_grupo[i] = grupo_ancla

    # Paso 2: cubrir el resto de los grupos con docentes que no son de inglés
    ancladas = set(pareja_grupo.values())

    for grupo in sorted(grupos, key=lambda g: len(candidatos_grupo[g])):
        if grupo not in ancladas:
            buscar_pareja(grupo, candidatos_grupo, pareja_grupo, set())

    grupo_de_docente = dict(pareja_grupo)
    cubiertos = set(grupo_de_docente.values())

    # Paso 3: docentes de inglés para los grupos que siguen sin titular
    grados_con_titular_regular = {grado_de_grupo[g] for g in cubiertos}
    pendientes = [grupo for grupo in grupos if grupo not in cubiertos]

    # Si un grado no pudo tener ningún titular que no sea de inglés, no puede
    # quedar completo con titulares de inglés: se deja un grupo sin titular.
    # (Solo aplica si hay docentes de inglés que podrían cubrirlo.)
    bloqueados = set()

    for grado in grados:
        if ingles and grado not in grados_con_titular_regular:
            bloqueados.add(
                next(g for g in pendientes if grado_de_grupo[g] == grado)
            )

    ingles_libres = ingles.copy()
    random.shuffle(ingles_libres)

    for grupo in pendientes:
        if grupo in bloqueados:
            continue

        if not ingles_libres:
            break

        grupo_de_docente[ingles_libres.pop()] = grupo

    titulares = {
        grupo: docentes[i]['nombre']
        for i, grupo in grupo_de_docente.items()
    }

    return titulares, grupo_de_docente, bloqueados


def diagnosticar_grupo_sin_titular(
    grupo, docentes, grupo_de_docente, grado_de_grupo, bloqueados
):
    print(f'  - Grupo {grupo}:')

    if grupo in bloqueados:
        print(
            f'      Un grado no puede quedar completo con titulares de inglés, y en '
            f'{grado_de_grupo[grupo]}° no se pudo asignar como titular a ningún '
            'docente que no sea de inglés. Por eso este grupo se dejó sin titular.'
        )

    imparten = [
        (i, docente) for i, docente in enumerate(docentes)
        if grupo in docente['horas_por_grupo']
    ]

    if not imparten:
        print('      Ningún docente (sin contar inglés) da clase en este grupo.')
    else:
        no_elegibles = [
            docente['nombre'] for i, docente in imparten
            if not docente['puede_ser_titular']
        ]
        ocupados = [
            docente['nombre'] for i, docente in imparten
            if docente['puede_ser_titular'] and i in grupo_de_docente
        ]

        if no_elegibles:
            print(
                '      Dan clase aquí pero no pueden ser titulares '
                '(Artes, Música o Tecnología): ' + ', '.join(no_elegibles)
            )

        if ocupados:
            print(
                '      Podrían serlo, pero ya son titulares de otro grupo '
                'y no hubo forma de reacomodarlos: ' + ', '.join(ocupados)
            )

    if grupo in bloqueados:
        print(
            '      Sugerencia: asigne materias en algún grupo de ese grado a un '
            'docente que pueda ser titular (que no imparta Artes, Música ni '
            'Tecnología) y que no sea de inglés.'
        )
    else:
        total_ingles = sum(1 for docente in docentes if docente['ingles'])

        if total_ingles == 0:
            print('      No hay docentes de inglés registrados para cubrirlo.')
        else:
            print(
                f'      Los {total_ingles} docente(s) de inglés ya son titulares '
                'de otros grupos.'
            )

        print(
            '      Sugerencia: asigne alguna materia de este grupo a un docente '
            'que pueda ser titular y aún no tenga grupo, o registre más '
            'docentes de inglés.'
        )


def mostrar_titulares(
    grupos, titulares, docentes, grupo_de_docente, grado_de_grupo, bloqueados
):
    print('\n========== ASIGNACIÓN DE TITULARES ==========\n')

    sin_titular = [grupo for grupo in grupos if grupo not in titulares]
    con_ingles = sum(1 for i in grupo_de_docente if docentes[i]['ingles'])

    print(
        f'Grupos con titular: {len(titulares)} de {len(grupos)} '
        f'({con_ingles} con titular de inglés)'
    )

    if not sin_titular:
        print('Todos los grupos tienen maestro titular.')
        return

    print('\nGrupos que se quedaron SIN titular:')

    for grupo in sin_titular:
        diagnosticar_grupo_sin_titular(
            grupo, docentes, grupo_de_docente, grado_de_grupo, bloqueados
        )


def mostrar_cargas(docentes, grupo_de_docente):
    print('\n========== CARGA LABORAL DE LOS DOCENTES ==========\n')

    for i, docente in enumerate(docentes):
        grupo_titular = grupo_de_docente.get(i)
        texto_titular = grupo_titular if grupo_titular is not None else 'ninguno'

        if docente['ingles']:
            # A los de inglés no se les calcula nada: siempre 36 horas base
            print(
                f"{docente['nombre']} (inglés): {docente['horas_clase']} horas. "
                f'Grupo titular: {texto_titular}'
            )
            continue

        horas = docente['horas_clase']
        if grupo_titular is not None:
            horas += HORAS_ORIENTACION

        print(
            f"{docente['nombre']}: {horas} horas. "
            f'Grupo titular: {texto_titular}'
        )


def mostrar_reporte(grupos, asignaciones, titulares, materias_por_grupo):
    print('\n========== REPORTE FINAL ==========\n')

    for grupo in grupos:
        print(f'===== GRUPO {grupo} =====')

        titular_grupo = titulares.get(grupo)

        if titular_grupo:
            print(f'Titular: {titular_grupo}')
        else:
            print('Titular: No hay maestro titular asignado')

        for materia in materias_por_grupo[grupo]:
            docente = asignaciones[grupo].get(materia)

            if docente:
                print(f'{materia}: {docente}')
            else:
                print(f'{materia}: No hay maestro asignado')

        print()


# -------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------

asignaciones = {}
docentes = []

cantidad_grupos = int(input('¿Cuántos grupos tiene la escuela?: '))

grupos, materias_por_grupo, grado_de_grupo = registrar_grupos(cantidad_grupos)

for grupo in grupos:
    asignaciones[grupo] = {}


cantidad_docentes = int(input('\n¿Cuántos docentes desea registrar?: '))


for numero_docente in range(cantidad_docentes):
    print(f'\n========== DOCENTE {numero_docente + 1} ==========')

    docente_actual = input('Ingrese su nombre: ')

    docente_ingles = input(
        '¿Es docente de inglés? (si/no): '
    ).lower()

    if docente_ingles == 'si':
        # Dan clase a todos los grupos, pero no se calcula nada con ellos:
        # siempre 36 horas base. Pueden ser titulares de cualquier grupo.
        docentes.append({
            'nombre': docente_actual,
            'ingles': True,
            'horas_clase': HORAS_INGLES,
            'horas_por_grupo': {},
            'puede_ser_titular': True,
        })

        print(
            f'\n{docente_actual} registrado como docente de inglés '
            f'({HORAS_INGLES} horas). Puede ser titular de cualquier grupo.'
        )

    else:
        # 1) Elige grupos (con botón de terminar) y cuántas materias da en cada uno
        grupos_docente = seleccionar_grupos(
            grupos,
            asignaciones,
            materias_por_grupo
        )

        # 2) Ya con los grupos definidos, elige las materias específicas
        horas_total, materias_docente, horas_por_grupo = calculador_horas(
            grupos_docente,
            asignaciones,
            materias_por_grupo,
            docente_actual
        )

        imparte_sin_titularidad = any(
            materia in MATERIAS_SIN_TITULARIDAD
            for materia in materias_docente
        )

        docentes.append({
            'nombre': docente_actual,
            'ingles': False,
            'horas_clase': horas_total,
            'horas_por_grupo': horas_por_grupo,
            'puede_ser_titular': bool(horas_por_grupo) and not imparte_sin_titularidad,
        })

        print(f'\n{docente_actual}, sus horas de clase son: {horas_total}.')

        if imparte_sin_titularidad:
            print('No podrá ser titular (imparte Artes, Música o Tecnología).')


# Los titulares se asignan hasta el final, con todos los docentes ya registrados
titulares, grupo_de_docente, bloqueados = asignar_titulares(
    grupos,
    docentes,
    grado_de_grupo
)

mostrar_titulares(
    grupos,
    titulares,
    docentes,
    grupo_de_docente,
    grado_de_grupo,
    bloqueados
)

mostrar_cargas(
    docentes,
    grupo_de_docente
)

mostrar_reporte(
    grupos,
    asignaciones,
    titulares,
    materias_por_grupo
)


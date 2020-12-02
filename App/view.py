import sys
import config
from App import controller
from DISClib.ADT import list as lt
import timeit
assert config

# ---------------------------------------------------
#  Variables
# ---------------------------------------------------

file1 = 'taxi-trips-wrvz-psew-subset-small.csv'
file1s = 'taxi-trips-wrvz-psew-subset-smallS.csv'
file1ss = 'taxi-trips-wrvz-psew-subset-smallS+.csv'
file1sss = 'taxi-trips-wrvz-psew-subset-smallS++.csv'
file1ssss = 'taxi-trips-wrvz-psew-subset-smallest.csv'
file5 = 'taxi-trips-wrvz-psew-subset-smallest+.csv'
file2 = 'taxi-trips-wrvz-psew-subset-medium.csv'
file3 = 'taxi-trips-wrvz-psew-subset-large.csv'
filename = file1
recursionLimit = 8000

# ---------------------------------------------------
#  Menu principal
# ---------------------------------------------------

def printMenu():
    print("\n")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Bienvenido")
    print("1- Inicializar ")
    print("2- Cargar información ")
    print("3- <Req 1> Reporte de informacion Companias & Taxis")
    print("4- <Req 2> Sistemas de puntos y premios a Taxis")
    print("5- <Req 3> Mejor horario en Taxi")
    print("0- Salir")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

def optionTwo():
    print("\nCargando información de bicicletas de Nueva York ....")
    controller.loadFile(analyzer, filename)
    numedges = controller.totalConnections(analyzer)
    numvertex = controller.totalStations(analyzer)
    print(f'Numero de vértices: {numvertex}')
    print(f'Numero de arcos: {numedges}')
    print(f'El limite de recursion actual: {sys.getrecursionlimit()}')
    sys.setrecursionlimit(recursionLimit)
    print(f'El limite de recursion se ajusta a: {recursionLimit}')

def optionThree():
    """
    Req 1
    """
    pass  

def optionFour():
    """
    Req 2
    """    
    pass

def optionFive():
    """
    Req 3
    """
    centiH = centiM = True
    while centiH:

        try:
            hhI = int(input('Ingrese la hora inferior en el rango\n>'))
            hhS = int(input('Ingrese la hora superior en el rango\n>'))

        except ValueError:
            print('Ingrese valores validos')

        else:
            hhI = hhI%24; hhS = hhS%24

            hhI, hhS = min(hhI, hhS), max(hhI, hhS)

            centiH = False
    
    while centiM:

        try:
            mmI = int(input('Ingrese el minuto inferior en el rango\n>'))
            mmS = int(input('Ingrese el minuto superior en el rango\n>'))

        except ValueError:
            print('Ingrese valores validos')

        else:
            mmI = mmI%60; mmS = mmS%60

            if hhI == hhS: mmI, mmS = min(mmI, mmS), max(mmI, mmS)

            centiM = False

    idCommunityAreaStart = str(float(input('Ingrese la id del area comun de origen\n>')))
    idCommunityAreaEnd = str(float(input('Ingrese la id del area comun destino\n>')))

    inferior = f'{hhI:02}:{mmI:02}'; superior = f'{hhS:02}:{mmI:02}'

    print(f'Consiguiendo el mejor horario entre el rango de horas [{inferior}>-<{superior}] para las estaciones [{idCommunityAreaStart}>-<{idCommunityAreaEnd}]')

    startTime, route, tripDuration = controller.mejorHorario(analyzer, inferior, superior, idCommunityAreaStart, idCommunityAreaEnd)

    print(f'Hora recomendada de inicio: {startTime}')
    print(f'Duracion estimada: {tripDuration}')
    print(f'Por la ruta: \n<')
    if not(route is None):
        if (lt.isEmpty(route)):
            for i in range(1, lt.size(route)+1):
                commArea = lt.getElement(route, i)
                print(f'\t{i}) De {commArea["vertexA"]} a {commArea["vertexB"]}')
        else:
            print('\tNo hay estaciones de por medio')
    else:
        print('\tNo hay estaciones de por medio')
    print('>')

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print('\nInicializando....')
        # cont es el controlador que se usará de acá en adelante
        analyzer = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print(f'\nTiempo de ejecución: {executiontime}')

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print(f'\nTiempo de ejecución: {executiontime}')

    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print(f'\nTiempo de ejecución: {executiontime}')

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print(f'\nTiempo de ejecución: {executiontime}')
    
    else:
        sys.exit(0)

sys.exit(0)
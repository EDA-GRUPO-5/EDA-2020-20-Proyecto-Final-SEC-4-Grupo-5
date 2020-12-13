import sys
import config
from App import controller
from DISClib.ADT import list as lt
import timeit
assert config
from DISClib.ADT import orderedmap as om

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
copia = 'copia_smallest_modificado.csv'
filename = file5
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
    print("3- <Req A> Reporte de informacion Companias & Taxis")
    print("4- <Req B> Taxis con más puntos")
    print("5- <Req C> Mejor horario en Taxi")
    print("0- Salir")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

def optionTwo():
    print("\nCargando información de taxis de Chicago....")
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
    Req A
    """
    pass

def optionFour():
    """
    Req B
    """    
    print("\nElija entre las siguientes opciones: ")
    print("\n1. Identificar los N taxis con más puntos para en una fecha determinada")
    print("2. Identificar los M taxis con más puntos para un rango entre dos fechas determinadas")
    option = int(input("\nOpción: "))
    
    if option == 1:
        num = int(input("\nIngrese la cantidad de taxis: "))
        initialDate = input("\nIngrese la fecha (YYYY-MM-DD): ")
        if om.contains(analyzer['dateIndex'], initialDate) == False:
            print('\nPor favor ingrese una fecha que se encuentre en el archivo.')
        else:
            controller.getTaxisByDate(analyzer, num, initialDate)

    elif option == 2:
        num = int(input("\nIngrese la cantidad de taxis: "))
        initialDate = input("\nIngrese la fecha inicial (YYYY-MM-DD): ")
        finalDate = input("\nIngrese la fecha final (YYYY-MM-DD): ")
        if om.contains(analyzer['dateIndex'], initialDate) == False or om.contains(analyzer['dateIndex'], finalDate) == False:
            print('\nPor favor ingrese fechas que se encuentren en el archivo.')
        else:
            controller.getTaxisByDateRange(analyzer, num, initialDate, finalDate)

    else:
        print("\nPor favor ingrese una opción válida.")

def optionFive():
    """
    Req C
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
        if not (lt.isEmpty(route)):
            for i in range(1, lt.size(route)+1):
                commArea = lt.getElement(route, i)
                print(f'\t{i}) De {commArea["vertexA"]} a {commArea["vertexB"]}')
        else:
            print('\tNo hay estaciones de por medio(B)')
    else:
        print('\tNo hay estaciones de por medio(A)')
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

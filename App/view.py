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
file2 = 'taxi-trips-wrvz-psew-subset-medium.csv'
file3 = 'taxi-trips-wrvz-psew-subset-large.csv'
filename = file1ssss
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
    controller.loadFile(citibike, filename)
    numedges = controller.totalConnections(citibike)
    numvertex = controller.totalStations(citibike)
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
    pass

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print('\nInicializando....')
        # cont es el controlador que se usará de acá en adelante
        citibike = controller.init()

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
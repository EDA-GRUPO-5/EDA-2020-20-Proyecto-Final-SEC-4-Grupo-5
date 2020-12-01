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
    print("3- <Req 1> ")
    print("4- <Req 2>")
    print("5- <Req 3>")
    print("0- Salir")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

def optionTwo():
    print("\nCargando información de bicicletas de Nueva York ....")
    controller.loadFile(citibike, filename)
    numedges = controller.totalConnections(citibike)
    numvertex = controller.totalStations(citibike)
    print('Numero de vértices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))

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

    if int(inputs) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        citibike = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))
    
    else:
        sys.exit(0)

sys.exit(0)
from datetime import datetime
import config as cf
from App import model
import csv
from DISClib.ADT import orderedmap as om

# ---------------------------------------------------
#  Inicializacion
# ---------------------------------------------------

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    citibike = model.newChicagoAnalyzer()
    return citibike

# ---------------------------------------------------
#  Funciones para la carga y almacenamiento 
#  de datos en los modelos
# ---------------------------------------------------

def loadFile(analyzer, tripfile):
    """

    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for line in input_file:
        model.loadChicagoAnalyzer(analyzer, line)
        analyzer['numServicios'] += 1
    
    return analyzer

# ---------------------------------------------------
#  Funciones para consultas
# ---------------------------------------------------

def totalStations(analyzer):
    """
    Total de estaciones de bicicleta
    """
    return model.totalStations(analyzer)

def totalConnections(analyzer):
    """
    Total de enlaces entre las estaciones
    """
    return model.totalConnections(analyzer)

# ---------------------------------------------------
#  Funciones para Reqs
# ---------------------------------------------------

def reporteInformacion(chicagoAnalyzer, m, n):
    """
    Req 1
    Reporte de Informacion Companias y Taxis
    """
    return model.reporteInformacion(chicagoAnalyzer, m, n)

def getTaxisByDate(chicagoAnalyzer, num, initialDate):
    """
    Req B Parte 1
    """
    model.getTaxisByDate(chicagoAnalyzer, num, initialDate)

def getTaxisByDateRange(chicagoAnalyzer, num, initialDate, finalDate):
    """
    Req B Parte 2
    """
    model.getTaxisByDateRange(chicagoAnalyzer, num, initialDate, finalDate)

def mejorHorario(chicagoAnalyzer, inferior, superior, idStart, idEnd):
    """
    Req C
    Returns:
    DateTime, Arraylist, float
    """
    inferior = datetime.strptime(inferior, '%H:%M')
    superior = datetime.strptime(superior, '%H:%M')
    
    rta = model.Req3MejorHorario(chicagoAnalyzer, inferior, superior, idStart, idEnd)

    if type(rta) == tuple: #La respuesta esperada
        return rta

    else:
        if rta == 0: #Vertice no contenido en el grafo
            print('Las community areas ingresadas no son validas')

        elif rta == 1: #El rango de fechas no retorno fechas(El rango de fechas es vacio)
            print('El rango de tiempo ingresado no contiene viajes')

        else: #Otro tipo de error
            print('Sucedio un error inesperado')

        return None, None, None

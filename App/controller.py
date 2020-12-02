from datetime import datetime
import config as cf
from App import model
import csv

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

def mejorHorario(chicagoAnalyzer, inferior, superior, idStart, idEnd):
    """
    Req 3\n
    Returns:
    DateTime, Arraylist, float
    """
    inferior = datetime.strptime(inferior, '%HH:%M')
    superior = datetime.strptime(superior, '%HH:%M')
    
    return model.mejorHorario(chicagoAnalyzer, inferior, superior, idStart, idEnd)
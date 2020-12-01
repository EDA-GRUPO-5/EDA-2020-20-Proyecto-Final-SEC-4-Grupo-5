from os import cpu_count
import config
from DISClib.ADT.graph import gr
from DISClib.DataStructures import listiterator as it
from DISClib.Utils import error as error

from datetime import date 

assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# =====================================================
#                       API
# =====================================================

# Funciones para agregar informacion al grafo

def newAnalyzer():
    return analyzer

def addToAnalyzer(analyzer, line):
    
    return analyzer

# ==============================
# Funciones de Load
# ==============================

def addStationToGraph(citibike, station):

    if not gr.containsVertex(citibike['connections'], station):
        gr.insertVertex(citibike['connections'], station)

    return citibike

def addStationToMap(citibike, trip):
    entry = m.get(citibike['stations'], trip['end station id'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, trip['start station id'])
        m.put(citibike['stations'], trip['end station id'], lstroutes)
    else:
        lstroutes = entry['value']
        info = trip['start station id']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return citibike

def addRoute(citibike, start, end, duration):

    edge = gr.getEdge(citibike['connections'], start, end)
    
    if edge is None:
        gr.addEdge(citibike['connections'], start, end, duration)

    else:
        gr.addEdgeCount(citibike['connections'], edge)
        #gr.promediateWeight(citibike['connections'], edge)

def addStationName(citibike, station):
    """
    Para el req 3
    """
    entry = citibike['name_IDstations']
    stationStart = station['start station id']
    stationEnd = station['end station id']
    if not m.contains(entry, stationStart):
            m.put(citibike['name_IDstations'], stationStart, station['start station name'])
    else:
        m.put(citibike['name_IDstations'], stationEnd, station['end station name'])
        
    if not m.contains(entry, stationEnd):
            m.put(citibike['name_IDstations'], stationEnd, station['end station name'])
    else:
        m.put(citibike['name_IDstations'], stationStart, station['start station name'])
    
    return citibike
    
def addStationCoords(citibike, trip):
    """
    Para el req 6
    """
    entry = citibike['coords']
    stationStart = (trip['start station latitude'], trip['start station longitude'], 0)
    stationEnd = (trip['end station latitude'], trip['end station longitude'], 1)

    e1 = m.get(entry, trip['start station id'])
    if e1 is None:
        m.put(entry, trip['start station id'], stationStart)

    e2 = m.get(entry, trip['end station id'])
    if e2 is None:
        m.put(entry, trip['end station id'], stationEnd)

    return citibike

def addBirthYear(citibike, trip):
    """
    Para los REQs {}
    """
    entry = citibike['components']
    year = trip['birth year']

    if not om.contains(entry, int(trip['start station id'])):
        om.put(entry, int(trip['start station id']), year)

    if not om.contains(entry, int(trip['end station id'])):
        om.put(entry, int(trip['end station id']), year)

    return citibike

def totalConnections(citibike):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(citibike['connections'])

def totalStations(citibike):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(citibike['connections'])

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(station, keyvaluestation):
    """
    Compara dos estaciones
    """
    stationid = keyvaluestation['key']
    if (station == stationid):
        return 0
    elif (station > stationid):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

# ==============================
# Funciones de Requerimientos
# ==============================

def Req3():
    pass

#=-=-=-=-=-=-=-=-=-=-=-=
#Funciones usadas
#=-=-=-=-=-=-=-=-=-=-=-=
def lessequal(k1,k2=None):
    if k2 == None:
        return True
    return k1 <= k2

def greatequal(k1,k2=None):
    return not(lessequal(k1,k2))

from os import cpu_count
import config
from DISClib.ADT import graph as gr
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from datetime import datetime as dt
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.Algorithms.Graphs import dijsktra as djk
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

def newChicagoAnalyzer():
    """
    Funcion para inicializar el analyzer
    """

    chicagoAnalyzer = {
        'taxi': None,
        'communityTrip': None,
        'company': None
    }

    chicagoAnalyzer['taxi'] = m.newMap  (
                                        numelements=1000,
                                        comparefunction=compareComm
                                        )

    chicagoAnalyzer['communityTrip'] = gr.newGraph  (
                                                    datastructure='ADJ_LIST',
                                                    directed=True,
                                                    size=1000,
                                                    comparefunction=compareComm
                                                    )

    chicagoAnalyzer['company'] = m.newMap   (
                                            numelements=1000,
                                            comparefunction=compareComm
                                            )

    chicagoAnalyzer['timeTrip'] = om.newMap (
                                            omaptype='BST',
                                            comparefunction=compareID
                                            )

    chicagoAnalyzer['tripID_edge'] = m.newMap   (
                                                numelements=100,
                                                comparefunction=compareComm
                                                )

    return chicagoAnalyzer

def loadChicagoAnalyzer(chicagoAnalyzer, infoline):
    """
    Cargar los datos en el Analyzer
    """
    #Clean Numeric
    cleanComArea(infoline)
    cleanTripMile(infoline)

    origin = str(infoline['pickup_community_area'])
    destiny = str(infoline['dropoff_community_area'])
    tripTime = infoline['trip_seconds']
    idTrip = infoline['trip_id']

    #Graph: Vertex and Edge
    addComArea(chicagoAnalyzer, origin)
    addComArea(chicagoAnalyzer, destiny)

    addTrip(chicagoAnalyzer, origin, destiny, tripTime, idTrip)

    #Map Taxi
    addTripToTaxi(chicagoAnalyzer, infoline)

    #Map Company
    addTaxiToCompany(chicagoAnalyzer, infoline)

    #Ordered Map Time
    addTimeToTaxi(chicagoAnalyzer, infoline)

    #Get edge by tripID
    addEdgeByTripID(chicagoAnalyzer, idTrip, origin, destiny)

    return chicagoAnalyzer

# ==============================
# Funciones de Load
# ==============================

def addTripToTaxi(chicagoAnalyzer, line):
    """
    Aniade al mapa de 'taxi' la informacion del mismo \n
    Key: Id del taxi; Value: {Tiempo de los recorridos total, Millas recorridas en total, Cantidad de Servicios dados, Dinero ganado}
    """

    entry = m.get(chicagoAnalyzer['taxi'], line['taxi_id'])

    if entry is None:
        info = m.newMap(numelements=7, comparefunction=compareComm)

        m.put(info, 'timeTotal', line['trip_seconds'])
        m.put(info, 'mileTotal', line['trip_miles'])
        m.put(info, 'numServices', 1)
        m.put(info, 'money', None)
        #m.put(info, '', lt.newList())

        m.put(chicagoAnalyzer['taxi'], line['taxi_id'], info)
    else:
        info = entry['value']
    
    return chicagoAnalyzer

def addComArea(chicagoAnalyzer, vertex):
    """
    Inserta el vertice que representa a un Community Area en el grafo
    """

    if not gr.containsVertex(chicagoAnalyzer['communityTrip'], vertex): gr.insertVertex(chicagoAnalyzer['communityTrip'], vertex)

    return chicagoAnalyzer

def addTrip(chicagoAnalyzer, origin, destiny, tripTime, idTrip):
    """
    Crea el arco(camino) entre los dos vertices(el de origen y el de destino)
    """
    
    edge = gr.getEdge(chicagoAnalyzer['communityTrip'], origin, destiny)

    if edge is None:
        gr.addEdge(chicagoAnalyzer['communityTrip'], origin, destiny, tripTime)
        edge = gr.getEdge(chicagoAnalyzer['communityTrip'], origin, destiny)
        edge['name'] = lt.newList()
    
    lt.addLast(edge['name'], idTrip)

    return chicagoAnalyzer

def addTaxiToCompany(chicagoAnalyzer, line):
    """
    Aniade la id del taxi a la compania a la que pertenece
    """

    entry = m.get(chicagoAnalyzer['company'], line['company'])

    if entry is None:
        taxis = lt.newList()
        lt.addLast(taxis, line['taxi_id'])
        m.put(chicagoAnalyzer['company'], line['company'], taxis)

    else:
        lt.addLast(entry['value'], line['taxi_id'])
    
    return chicagoAnalyzer

def addTimeToTaxi(chicagoAnalyzer, line):
    """
    Para el Req 3\n
    Key: Fecha; Value: lista de taxis que estan en esa hora
    """
    tripStart = line['trip_start_timestamp']
    taxiTrip = dt.strptime(tripStart, '%Y-%m-%dT%H:%M:%S.%f')
    time = taxiTrip.strftime('%H:%M')
    entry = om.get(chicagoAnalyzer['timeTrip'], time)

    if entry is None:
        taxiLt = lt.newList(cmpfunction=compareID)
        om.put(chicagoAnalyzer['timeTrip'], time, taxiLt)

    else:
        lt.addLast(entry['value'], line['trip_id'])

    return chicagoAnalyzer

def addEdgeByTripID(chicagoAnalyzer, trip_id, origin, destiny):
    """
    Funcion para conseguir origen y destino teniendo el id del viaje
    """
    entry = m.get(chicagoAnalyzer['tripID_edge'], trip_id)

    if entry is None:
        edge = gr.getEdge(chicagoAnalyzer['communityTrip'], origin, destiny)
        m.put(chicagoAnalyzer['tripID_edge'], trip_id, edge)

    return chicagoAnalyzer
# ==============================
# Funciones de Comparacion/Limpieza
# ==============================

def compareID(id1, id2):
    """
    Compara dos numeros
    """
    if (id1 == id2):
        return 0
    elif (id1 > id2):
        return 1
    else:
        return -1

def compareComm(station, keyvaluestation):
    """
    Compara dos valores, str y dict
    """
    stationid = keyvaluestation['key']
    if (station == stationid):
        return 0
    elif (station > stationid):
        return 1
    else:
        return -1

def cleanComArea(line):

    if line['dropoff_community_area'] == '': line['dropoff_community_area'] = '-1'

    if line['pickup_community_area'] == '': line['pickup_community_area'] = '-1'

    return line

def cleanTripMile(line):

    if line['trip_miles'] == '': line['trip_miles'] = 0

    return line

def totalConnections(chicagoAnalyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(chicagoAnalyzer['communityTrip'])

def totalStations(chicagoAnalyzer):
    """
    Retorna el total de vertices del grafo
    """
    return gr.numVertices(chicagoAnalyzer['communityTrip'])

# ==============================
# Funciones de Requerimientos
# ==============================

def Req3MejorHorario(chicagoAnalyzer, inferior, superior, idStart, idEnd):

    commArea = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareID)

    structure = djk.Dijkstra(chicagoAnalyzer['communityTrip'], idStart)
    time = djk.distTo(structure, idEnd)
    path = djk.pathTo(structure, idEnd)

    for i in range(st.size(path)):
        lt.addLast(commArea, st.pop(path))

    return startTime, commArea, time

# =-=-=-=-=-=-=-=-=-=-=-=
# Funciones usadas
# =-=-=-=-=-=-=-=-=-=-=-=
def lessequal(k1,k2=None):
    if k2 == None:
        return True
    return k1 <= k2

def greatequal(k1,k2=None):
    return not(lessequal(k1,k2))

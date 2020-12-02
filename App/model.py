from DISClib.ADT.graph import vertices
from DISClib.ADT.orderedmap import keys
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
                                        numelements=100,
                                        comparefunction=compareComm
                                        )

    chicagoAnalyzer['communityTrip'] = gr.newGraph  (
                                                    datastructure='ADJ_LIST',
                                                    directed=True,
                                                    size=2000,
                                                    comparefunction=compareComm
                                                    )

    chicagoAnalyzer['company'] = m.newMap   (
                                            numelements=50,
                                            comparefunction=compareComm
                                            )

    chicagoAnalyzer['timeTrip'] = om.newMap (
                                            omaptype='BST',
                                            comparefunction=compareID
                                            )

    chicagoAnalyzer['tripID_edge'] = m.newMap   (
                                                numelements=2000,
                                                comparefunction=compareComm
                                                )

    return chicagoAnalyzer

def loadChicagoAnalyzer(chicagoAnalyzer, infoline):
    """
    Cargar los datos en el Analyzer
    """
    #Clean Numeric
    cleanComArea(infoline)
    cleanTripMileSeconds(infoline)

    origin = str(infoline['pickup_community_area'])
    destiny = str(infoline['dropoff_community_area'])
    tripTime = float(infoline['trip_seconds'])
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
    
    m.put(chicagoAnalyzer['tripID_edge'], idTrip, edge)

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
    timeB = taxiTrip.strftime('%H:%M')
    time = dt.strptime(timeB, '%H:%M')
    entry = om.get(chicagoAnalyzer['timeTrip'], time)

    if entry is None:
        taxiLt = lt.newList(cmpfunction=compareID)
        om.put(chicagoAnalyzer['timeTrip'], time, taxiLt)

    else:
        lt.addLast(entry['value'], line['trip_id'])

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

    if line['dropoff_community_area'] in {'', None}: line['dropoff_community_area'] = '0'

    if line['pickup_community_area'] in {'', None}: line['pickup_community_area'] = '0'

    return line

def cleanTripMileSeconds(line):

    if line['trip_miles'] in {'', None}: line['trip_miles'] = '0'
    if line['trip_seconds'] in {'', None}: line['trip_seconds'] = 0

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

    commArea = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareComm)

    keysInRange = om.keys(chicagoAnalyzer['timeTrip'], inferior, superior)

    structure = djk.Dijkstra(chicagoAnalyzer['communityTrip'], idStart)
    timeTrip = djk.distTo(structure, idEnd)
    path = djk.pathTo(structure, idEnd)

    for _ in range(st.size(path)):
        lt.addLast(commArea, st.pop(path))

    for time in range(lt.size(keysInRange)):
        temp = lt.getElement(keysInRange, time)
        route = om.get(chicagoAnalyzer['timeTrip'], temp)['value']
        for timeID in range(lt.size(route)):
            start, end = getEdgebyTripID(chicagoAnalyzer, lt.getElement(route, timeID))
            try:
                if start == idStart and lt.isPresent(commArea, end):
                    print('ou yeah')
                    return temp, commArea, timeTrip
            except:
                print(end)
                print(commArea)

    
    return None, commArea, timeTrip

# =-=-=-=-=-=-=-=-=-=-=-=
# Funciones usadas
# =-=-=-=-=-=-=-=-=-=-=-=
def lessequal(k1,k2=None):
    if k2 == None:
        return True
    return k1 <= k2

def greatequal(k1,k2=None):
    return not(lessequal(k1,k2))

def getEdgebyTripID(chicagoAnalyzer, tripID):

    entry = m.get(chicagoAnalyzer['tripID_edge'], tripID)['value']

    if entry is not None:
        return (entry['vertexA'], entry['vertexB'])
    return None

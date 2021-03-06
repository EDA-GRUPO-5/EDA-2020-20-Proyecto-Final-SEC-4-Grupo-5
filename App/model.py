from DISClib.ADT.stack import newStack
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
from DISClib.Algorithms.Sorting import insertionsort as insor
from DISClib.Algorithms.Sorting import mergesort as ms

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

    chicagoAnalyzer['dateIndex'] = om.newMap (omaptype='BST',
                                              comparefunction=compareDates
                                              )

    chicagoAnalyzer['numServicios'] = 0

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

    #Ordered Date Map
    addDateToTaxi(chicagoAnalyzer, infoline)

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

        m.put(chicagoAnalyzer['taxi'], line['taxi_id'], info)
    else:
        info = entry['value']
        num = m.get(info, 'numServices')['value']+1
        m.put(info, 'numServices', num)
        m.put(chicagoAnalyzer['taxi'], line['taxi_id'], info)
    
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

def addDateToTaxi(chicagoAnalyzer, line):
    tripStart = line['trip_start_timestamp']
    taxiTrip = dt.strptime(tripStart, '%Y-%m-%dT%H:%M:%S.%f')
    date = taxiTrip.strftime('%Y-%m-%d')
    entry = om.get(chicagoAnalyzer['dateIndex'], date)
    if entry is None:
        taxiLt = lt.newList(cmpfunction=compareID)
        om.put(chicagoAnalyzer['dateIndex'], date, taxiLt)

    else:
        if float(line['trip_miles']) > 0.0 and float(line['trip_total']) > 0.0:
            puntos = (float(line['trip_miles'])/float(line['trip_total']))
            lt.addLast(entry['value'], (line['trip_id'], puntos))

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

def compareDict(id1, dic2):
    """
    Compara dos numeros
    """
    if (id1 in {dic2['vertexA'], dic2['vertexB']}):
        return 0
    elif (id1 > dic2['vertexA'] or id1> dic2['vertexB']):
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

def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def comparePoints(element1, element2):
    if float(element1[1]) > float(element2[1]):
        return True
    return False

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
def Req1RepInfo(chicagoAnalyzer, mTop, nTop):
    if 0 in {mTop, nTop}: return 0

    totalTaxi = m.size(chicagoAnalyzer['taxi'])
    totalCompany = m.size(chicagoAnalyzer['company'])
    topMCompanyTaxi = lt.newList(datastructure='ARRAY_LIST')
    topNCompanyService = lt.newList(datastructure='ARRAY_LIST')

    #Obtener taxis por compania
    ltCompany = m.keySet(chicagoAnalyzer['company'])
    for company in range(lt.size(ltCompany)):
        size = m.get(chicagoAnalyzer['company'], lt.getElement(ltCompany, company))['value']
        lt.addLast(topMCompanyTaxi, (lt.getElement(ltCompany, company),lt.size(size)))
        count = 0
        for idTaxi in range(lt.size(size)):
            infoT = m.get(chicagoAnalyzer['taxi'], lt.getElement(size, idTaxi))['value']
            count += m.get(infoT, 'numServices')['value']
        lt.addLast(topNCompanyService, (lt.getElement(ltCompany, company),count))

    ms.mergesort(topMCompanyTaxi, comparePoints)
    ms.mergesort(topNCompanyService, comparePoints)

    return totalTaxi, totalCompany, lt.subList(topMCompanyTaxi, 1, mTop)['elements'], lt.subList(topNCompanyService, 1, nTop)['elements']

def reporteInformacion(chicagoAnalyzer, m, n):
    """
    Req 1
    Return: # Total Taxis, # Total Compañias, Top M de compañias con más taxis afiliados, 
    Top N de compañias con más servicios prestados
    """
    
    reporteCompleto = lt.newList(datastructure='ARRAY_LIST')

    taxis = chicagoAnalyzer['taxi']['size'] #NUMERO TOTAL DE TAXIS
    companias = chicagoAnalyzer['company']['size'] #NUMERO TOTAL DE COMPANIAS

    #TOP M DE COMPANIAS POR CANTIDAD DE TAXIS AFILIADOS 
    taxisAfiliados = chicagoAnalyzer['company']['table']
    topTaxisAfiliados = lt.newList(datastructure='ARRAY_LIST')

    for value in taxisAfiliados.values():
        cantidadTaxisAfiliados = lt.newList(datastructure='ARRAY_LIST')
        for i in value:
            x = i.get('first')
            if x != None:
                y = x.get('info')
                key = y.get('key')
                value = y.get('value')
                size = value.get('size') #Obtener el tamaño de cada compania (cantidad de taxis afiliados)
                lt.addLast(cantidadTaxisAfiliados, (key, size))
        cantidadTaxisAfiliados['elements'].sort(key=lambda taxis: taxis[1]) #Ordenar de mayor a menor
        cantidadTaxisAfiliados['elements'].reverse()
        topTaxisAfiliados = lt.newList(datastructure='ARRAY_LIST')
        for i in range(1, m+1): #Top M
            resultado = lt.getElement(cantidadTaxisAfiliados, i)
            lt.addLast(topTaxisAfiliados, resultado)
        print('Top de compañias con más taxis afiliados: ', topTaxisAfiliados['elements'])

    #TOP N DE COMPANIAS CON MAS SERVICIOS PRESTADOS
    #topServiciosPrestados = lt.newList(datastructure='ARRAY_LIST')

    lt.addLast(reporteCompleto, taxis)
    lt.addLast(reporteCompleto, companias)
    #lt.addLast(reporteCompleto, topTaxisAfiliados['elements'])
    #lt.addLast(reporteCompleto, topServiciosPrestados['elements'])

    return reporteCompleto['elements']

def getTaxisByDate(chicagoAnalyzer, num, initialDate):
    """
    Req B Parte 1
    """
    
    lstIdsPoints = om.get(chicagoAnalyzer['dateIndex'], initialDate)['value']
    insor.insertionSort1(lstIdsPoints, comparePoints)
    
    print("\nLos Ids de los " + str(num) + " taxis con más puntos son: ")
    count = 1
    print("\n")
    for pos in range(1, num+1):
        taxi = lt.getElement(lstIdsPoints, pos)
        print(str(count) + ". " + str(taxi[0]) + " con " + str(taxi[1]*chicagoAnalyzer['numServicios']) + " puntos")
        count += 1
        num -= 1

def getTaxisByDateRange(chicagoAnalyzer, num, initialDate, finalDate):
    """
    Req B Parte 2
    """
    lstValues = om.values(chicagoAnalyzer['dateIndex'], initialDate, finalDate)
    lstIdsPoints = lt.newList(datastructure='ARRAY_LIST')

    for pos in range(1, lt.size(lstValues)+1):
        date = lt.getElement(lstValues, pos)
        for pos1 in range(1, lt.size(date)+1):
            taxi= lt.getElement(date, pos1)
            lt.addLast(lstIdsPoints, (taxi[0], taxi[1]))
    
    insor.insertionSort1(lstIdsPoints, comparePoints)
    
    print("\nLos Ids de los " + str(num) + " taxis con más puntos son: ")
    count = 1
    print("\n")
    for pos2 in range(1, num+1):
        taxi = lt.getElement(lstIdsPoints, pos2)
        print(str(count) + ". " + str(taxi[0]) + " con " + str(taxi[1]*chicagoAnalyzer['numServicios']) + " puntos")
        count += 1
        num -= 1         

def Req3MejorHorario(chicagoAnalyzer, inferior, superior, idStart, idEnd):
    """
    Req C\n
    Returns: Tiempo de inicio del trayecto, las community areas en medio del trayecto, la duracion del trayecto
    """
    #Si no contiene el vertice el proceso se corta de raiz y no hace mas operaciones innecesarias DE MORGAN
    if not(gr.containsVertex(chicagoAnalyzer['communityTrip'], idStart) and gr.containsVertex(chicagoAnalyzer['communityTrip'], idStart)): return 0

    #Lista con las community areas, se entregara como parte de la respuesta
    comRoute = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareDict)

    #Conseguir los viajes que sucedieron en el rango de hora especificado
    keysInRange = om.keys(chicagoAnalyzer['timeTrip'], inferior, superior)

    #Si el rango de horas no contiene alguna hora de trayecto
    if (lt.isEmpty(keysInRange)): return 1

    #Dijkstra para conseguir la duracion y las comunnity areas para llegar al destino
    structure = djk.Dijkstra(chicagoAnalyzer['communityTrip'], idStart)
    tripDuration = djk.distTo(structure, idEnd)
    path = djk.pathTo(structure, idEnd) if djk.hasPathTo(structure, idEnd) else st.newStack()

    #Se usa _ porque la variable no importa en si, solo es necesario hacerle pop al stack
    for _ in range(st.size(path)):
        lt.addLast(comRoute, st.pop(path))
    #Para conseguir el tiempo en formato Hora:Minuto
    #Dado que hay dos for anidados, en comparacion a la complejidad del resto del algoritmo
    startTime = None
    for time in range(lt.size(keysInRange)):
        #starTime antes de hacerle format
        startTimeb4F = lt.getElement(keysInRange, time)
        route = om.get(chicagoAnalyzer['timeTrip'], startTimeb4F)['value']

        #Para conseguir la id del trayecto y con la funcion de getEdgebyTripID() se conseguir ambos vertices
        for timeID in range(lt.size(route)):
            start, end = getEdgebyTripID(chicagoAnalyzer, lt.getElement(route, timeID))
            #Verificar que sea el arco que buscamos
            if start == idStart and lt.isPresent(comRoute, end):
                startTime = f'{startTimeb4F.hour:02}:{startTimeb4F.minute:02}'
                return startTime, comRoute, tripDuration
    return startTime, comRoute, tripDuration

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

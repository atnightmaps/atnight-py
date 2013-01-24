# -*- coding: cp1252 -*-
'''
archivo que genera unico shape
'''

import datetime
import shapefile
import urllib2
import json
import time
import sched

getUrl= 'http://map.mytaxi.net/public/index.php/map_controller/retrieveMarkers/42/3/40/0'
print 'inicio taxi2shape'
print

# carga la posición de los taxis i lo convierte en un dic
def loadTaxis():
    request = urllib2.Request(getUrl)
    response = urllib2.urlopen(request)
    content = response.read()
    data = json.loads(content)
    return data


# incorpora cada taxi a su shape
def shapeTaxi(data):
    now = datetime.datetime.now()
    print now
    nowf = now.strftime("%Y/%m/%d %H:%M:%S")
    hour = now.strftime("%H:%M:%S")
    hourTs=int(time.time())
    for i in data:
        for e in data[i]:
            parse (str(data[i][e]['id']),float(data[i][e]['lat']), float(data[i][e]['lng']),nowf,hourTs)
    return

# parsea
def parse(tid,lat,lng,time,hour):
    now = datetime.datetime.now()
    nowf = now.strftime("%Y%m%d")
    try:
        e= shapefile.Editor(shapefile=nowf)
        e.point(lng,lat,0,0)
        e.record(tid,time,hour)
        e.save(nowf)
    
    except:
        w= shapefile.Writer(shapeType=1)
        w.autobalance=1
        w.point(lng,lat,0,0)
        w.field('tid','C','40',0)
        w.field('tTime','C','20',0)
        w.field('hour','C','10',0)
        w.record(tid,time,hour)
        w.save(nowf) 
    return

#run
if __name__ == '__main__':
    it=1
    while True:
        print 'inicio consulta numero ',it
        try:
            shapeTaxi(loadTaxis())            

        except:
            print '//////////////////try again'

        print 'fin    consulta numero ',it    
        print
        it+=1
        time.sleep(60)

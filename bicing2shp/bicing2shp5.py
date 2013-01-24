# -*- coding: cp1252 -*-

import shapefile
import urllib2
import json
import time
import datetime
import csv

getUrl= 'http://api.citybik.es/bicing.json'
files='b2s-05'

print 'inicio bicing2shape'

def setup():
    #crea el shapefile
    try:
        shapefile.Reader(files)
    except:
        w= shapefile.Writer(shapeType=1)
        w.autobalance=1

        w.point(0,0,0,0)
        w.field('bid','C','5',0)
        w.field('lng','C','20',10)
        w.field('lat','C','20',10)
        w.field('nombre','C','50',0)
        w.record(0,0,0,0)
        
        data = loadBicis()

        for i in data:
            name=i['name']
            
            if name != None:
               name=name.encode('cp1252',errors='ignore')
            else:
                print 'noooo'
                
            lat=float(i['lat']/1000000.0)
            lng=float(i['lng']/1000000.0)
            bid=i['number']
            w.point(lng,lat,0,0)
            w.record(bid,lat,lng,name)
            
        w.save(files)

        print('shp file created')

    # crea el csv
    
    try:
        f=file((files+'.csv'),'r')
    except:
        f= file((files+'.csv'), 'wb')
        csvFile=csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        l=['inicio de la consulta']
        csvFile.writerow(l)
        f.close
        print ('csv file created')
    print('setup done')
    return

def loadBicis():
    while True:
        try:
            request = urllib2.Request(getUrl)
            response = urllib2.urlopen(request)
            content = response.read()
            data = json.loads(content)
            return data
            break
        except:
            print 'problemas con loadBicis()'

def data2dic(data):
    l={}
    for i in data:
        l[i['number']]=i['bikes']
    return l
    

#actualiza cadena de bicis
def countBikes(bikes,newBikes):
    
    for i in newBikes:
        if bikes.get(i) != None:
            pass
        else:
            bikes[i]=0
            
        bikes[i]=(newBikes[i]-bikes[i])

    return bikes


#actualiza movimientos
def countMovs(movs,bikes):

    for i in bikes:
        if movs.get(i) != None:
            pass
        else:
            movs[i]=0       
        movs[i]+= abs(bikes[i])
    return movs

def parse(nowf,movs,bikes):
    for i in movs:
            row=(nowf, i ,bikes[i], movs[i])
            with open((files+'.csv'), 'ab') as f:
                csvFile = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                csvFile.writerow(row)     
    return


if __name__ == '__main__':
    setup()
    movs={}
    bikes={}
    it=0
    while True:  
        data=loadBicis()
        
        newBikes= data2dic(data)

        bikes=countBikes(bikes,newBikes)
        movs=countMovs(movs,bikes)
        it+=1
        now = datetime.datetime.now()
        nowf = now.strftime("%Y/%m/%d %H:%M:%S")
        print nowf
        print it,',', 
        if it > 10:
            now = datetime.datetime.now()
            nowf = now.strftime("%Y/%m/%d %H:%M:%S")
            print nowf
            parse(nowf,movs,bikes)
            print '/parsed data'
            movs={}
            bikes={}
            it=0
            print 'nuevo ciclo:',
            
           
        time.sleep(90)    
        

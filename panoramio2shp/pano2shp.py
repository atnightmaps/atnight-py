# -*- coding: utf-8 -*-
import urllib2
import json
import shapefile
import time

# http://www.panoramio.com/api/data/api.html

url = 'http://www.panoramio.com/map/get_panoramas.php'
inter= 400
k=inter
set2 = 'full'
from2 = k-inter
to = inter
minx = '2.087'
miny = '41.335'
maxx = '2.246'
maxy = '41.4674'
size = 'thumbnail'
mapfilter= 'false'

geturl = (url+'?'+'set'+'='+set2+'&'+'from'+'='+str(from2)+'&'+'to'+'='+str(to)+'&'+'minx'+'='+minx+'&'+'miny'+'='+miny+'&'+'maxx'+'='+maxx+'&'+'maxy'+'='+maxy+'&'+'size'+'='+size+'&'+'mapfilter'+'='+mapfilter)
geturl2 = (url+'?'+'set'+'='+set2+'&'+'from'+'=0&'+'to'+'='+'0'+'&'+'minx'+'='+minx+'&'+'miny'+'='+miny+'&'+'maxx'+'='+maxx+'&'+'maxy'+'='+maxy+'&'+'size'+'='+size+'&'+'mapfilter'+'='+mapfilter)
pano2shapeFile='pan2shp'

print geturl

try:
    shapefile.Reader(pano2shapeFile)

except:
    w= shapefile.Writer(shapeType=1)
    w.autobalance=1

    w.point(1,41,0,0)
    w.point(3,43,0,0)

    w.field('fid','C','20',5)
    w.field('source','C','100',5)
    w.field('title','C','100',5)
    w.field('desc','C','100',5)
    w.field('month','C','4',5)
    w.field('hour','C','10',5)

    w.record('nonull1','0','0','0','0','0')
    w.record('nonull2','0','0','0','0','0')

    w.save(pano2shapeFile)

def setData():
    data=getData(geturl2)
    k=data['count']
    return k


def parse(lng, lat, fid, src, tit):
    e= shapefile.Editor(shapefile=pano2shapeFile)
    e.point(lng,lat,0,0)
    e.record(fid, src, tit, 0, 0, 0)
    e.save(pano2shapeFile)
    return 

#lanza la consulta
def getData(url):
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        content = response.read()
        data = json.loads(content)
        return data
    except:
        print 'preparandose para otro intento'
        time.sleep(5)
        return getData(url)

def shapeData(data):
    if len(data['photos'])==0:
        k=-1
        return
    for f in range (len(data['photos'])):
        lat= data['photos'][f]['latitude']
        lng= data['photos'][f]['longitude']
        tit= data['photos'][f]['photo_title']
        tit=tit.encode(errors='ignore')
        src= data['photos'][f]['photo_file_url']
        src=src.encode(errors='ignore')
        fid= data['photos'][f]['photo_id']
        parse (float(lng), float(lat),fid, src, tit)
    return

#run
if __name__ == '__main__':
    
    k=setData()

    while k  > (0-inter):
        from2 = k-(inter-1)
        to = k  
        print 'lanzando consulta from ', from2,'to ',to
        data=getData(geturl)
        shapeData(data)
        k= k-inter
    print 'happy end!'

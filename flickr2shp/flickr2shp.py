# -*- coding: cp1252 -*-
import shapefile
import flickrapi
import time

print 'iniciando flikcrAPI'

#introducir datos de la APIFLICKR
api_key = ''
api_secret = ''

#llamada a la api
flickr = flickrapi.FlickrAPI(api_key, api_secret)
(token, frob) = flickr.get_token_part_one(perms='read')
if not token: raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

print 'iniciando shapes'
flickr2shapeFile='flck2shp'

#verificar que hay un shp listo para escribir
try:
  shapefile.Reader(flickr2shapeFile)

except:
  w= shapefile.Writer(shapeType=1)
  w.autobalance=1
  
  w.point(1,41,0,0)
  w.point(3,43,0,0)

  w.field('fid','C','20',0)
  w.field('source','C','100',0)
  w.field('title','C','100',0)
  w.field('desc','C','200',0)
  w.field('month','C','4',0)
  w.field('hour','C','10',0)
  w.field('tags','C','200',0)
  
  w.record('nonull1','0','0','0','0','0','0')
  w.record('nonull2','0','0','0','0','0','0')

  w.save(flickr2shapeFile)

print 'ok, all running...'

def parse(lng, lat, fid, src, tit, desc, month, hour, tags):
  print (lng, lat, fid, src, tit, desc, month, hour, tags)
  
  e= shapefile.Editor(shapefile=flickr2shapeFile)
  e.point(lng,lat,0,0)
  e.record(fid, src, tit, desc, month, hour, tags)
  e.save(flickr2shapeFile)
  return 

  
        
#obtención de la primera estimación
def status():
  photos = flickr.photos_search(lat='41.40348', lon='2.18687', radius='15', license='1,2,3,4,5,6,7', per_page='500')
  print 'total fotos = ' + photos[0].attrib['total']
  print 'total_paginas = ' + photos[0].attrib['pages']
  print 'go! go! go!'
  print
  return

# inicio de timestamp en 1334552400 / 1352160000
#por qué fecha vamos p = open('fecha', 'r+')
def setData():
  p = open('fecha', 'r+')
  j = p.readline()
  p.close
  k = int(j)
  print 'leyendo desde la fecha '+ str(j)
  return k

def updateData(k):
  p = open('fecha', 'w')
  k = k - 21600
  p.write( str(k))
  p.close
  return k

#cojemos las fotos en paquetes de 12 horas 43200 s.
def takeFotos(k):
  i= k - 21599
  photos = flickr.photos_search(min_upload_date=i, max_upload_date=k, lat='41.40348', lon='2.18687', radius='15', license='1,2,3,4,5,6,7', per_page='500')
  for photo in photos[0]:
    #get lat lon
    photoLoc = flickr.photos_geo_getLocation(photo_id=photo.attrib['id'])
    #get url
    photoSizes = flickr.photos_getSizes(photo_id=photo.attrib['id'])
    #get dates
    photoInf = flickr.photos_getInfo(photo_id=photo.attrib['id'])
    

    lng= photoLoc[0][0].attrib['longitude']
    lat= photoLoc[0][0].attrib['latitude']
    
    fid= photo.attrib['id']
    
    tit= photo.attrib['title']
    tit = tit.encode(errors='replace')
    src= photoSizes[0][1].attrib['source']

    #try:
    des= photoInf[0][2].text
    if des==None:
      desc = 0
    else:
      desc=des.encode('ascii', 'xmlcharrefreplace')
      
    month= photoInf[0][4].attrib['taken'][5:7]
    hour= photoInf[0][4].attrib['taken'][11:]
    print 'pora ahora bien'
    #tags
    tags=[]
    for tag in photoInf[0][11]:
      tags.append(tag.attrib['raw'])
    print tags

    parse (float(lng), float(lat), fid, src, tit, desc, month, hour, tags)
    
  return

#run
if __name__ == '__main__':
  status()
  k=setData()
  while k  > 0:
    try:
      takeFotos(k)    
      k=updateData(k)
      print 'solicitando :',k
    except:
      print 'try again... ... ...'
  print 'happy end!'


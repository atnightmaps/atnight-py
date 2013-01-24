# -*- coding: cp1252 -*-

import datetime
import shapefile
import urllib2
import json
import time

files='insta_hist02'

currentT=int(time.time())

print currentT
lapsus=3600
punts2=[('41.40402','2.18804'),('41.39133','2.16313')]
punts=[('41.320767', '2.101864'), ('41.320951', '2.125758'),
       ('41.32113', '2.149653'), ('41.33878', '2.101617'), ('41.338964', '2.125517'),
       ('41.339144', '2.149418'), ('41.339318', '2.173319'), ('41.356977', '2.125276'),
       ('41.357157', '2.149184'), ('41.357331', '2.173091'), ('41.3575', '2.196999'),
       ('41.374806', '2.101121'), ('41.374991', '2.125035'), ('41.37517', '2.148949'),
       ('41.375344', '2.172863'), ('41.375514', '2.196777'), ('41.392819', '2.100873'),
       ('41.393004', '2.124793'), ('41.393183', '2.148714'), ('41.393358', '2.172635'),
       ('41.393527', '2.196556'), ('41.410642', '2.076698'), ('41.410832', '2.100625'),
       ('41.411016', '2.124552'), ('41.411196', '2.148479'), ('41.411371', '2.172406'),
       ('41.41154', '2.196334'), ('41.428845', '2.100376'), ('41.429029', '2.12431'),
       ('41.429209', '2.148243'), ('41.429384', '2.172177'), ('41.429554', '2.196112'),
       ('41.428648', '2.075624'), ('41.447042', '2.124067'), ('41.447222', '2.148008'),
       ('41.447397', '2.171948'), ('41.447567', '2.195889'), ('41.46541', '2.171719'),
       ('41.46558', '2.195667'), ('41.410642', '2.076698'), ('41.320767', '2.101864'),
       ('41.33878', '2.101617'), ('41.374806', '2.101121'), ('41.392819', '2.100873'),
       ('41.410832', '2.100625'), ('41.428845', '2.100376'), ('41.42873', '2.100378'),
       ('41.320951', '2.125758'), ('41.338964', '2.125517'), ('41.356977', '2.125276'),
       ('41.374991', '2.125035'), ('41.393004', '2.124793'), ('41.411016', '2.124552'),
       ('41.429029', '2.12431'), ('41.447042', '2.124067'), ('41.32113', '2.149653'),
       ('41.339144', '2.149418'), ('41.357157', '2.149184'), ('41.37517', '2.148949'),
       ('41.393183', '2.148714'), ('41.411196', '2.148479'), ('41.429209', '2.148243'),
       ('41.447222', '2.148008'), ('41.339318', '2.173319'), ('41.357331', '2.173091'),
       ('41.375344', '2.172863'), ('41.393358', '2.172635'), ('41.411371', '2.172406'),
       ('41.429384', '2.172177'), ('41.447397', '2.171948'), ('41.3575', '2.196999'),
       ('41.375514', '2.196777'), ('41.393527', '2.196556'), ('41.41154', '2.196334'),
       ('41.429554', '2.196112'), ('41.447567', '2.195889'), ('41.393692', '2.220477'),
       ('41.411705', '2.220261'), ('41.429718', '2.220046')]

global nFotos
nFotos=0

##lat= '41.393'
##lng= '2.161'

def getUrl(lat,lng):
    
    maxT= str(currentT)
    minT= str(currentT-lapsus+1)
    dist= '1500'
    token= ''

    url3= 'https://api.instagram.com/v1/media/search?lat='+lat+'&lng='+lng+'&max_timestamp='+maxT+'&min_timestamp='+minT+'&distance='+dist+'&access_token='+token
    getUrl=url3

    return getUrl

def updateDate():
    return (currentT-lapsus)

def instagram_call(consulta):
    while True:
        try:
            request = urllib2.Request(consulta)
            response = urllib2.urlopen(request)
            content = response.read()
            data = json.loads(content)
            fotos=data['data']
            #print fotos
            return fotos
        except:
            print '/////'

def setup():
    try:
        shapefile.Reader(files)
        print('shp file ready')
    except:
        w= shapefile.Writer(shapeType=1)
        w.autobalance=1

        w.point(0,0,0,0)
        w.field('foto_id','C','30',0)
        w.field('foto_text','C','100',0)
        w.field('foto_time','C','40',0)
        w.field('foto_latitude','C','20',0)
        w.field('foto_longitude','C','20',0)
        w.field('foto_link','C','100',0)
        w.record(0,0,0,0,0,0)
        w.save(files)
        
        print('shp file created')
        
    return

def parse(lng, lat, fid, source, title, time):
    global nFotos
    nFotos+=1
    e= shapefile.Editor(shapefile=files)
    e.point(lng,lat,0,0)
    e.record(fid,title,time,lat,lng,source) 
    e.save(files)
    #print (fid,title,time,lat,lng,source)
    return
    
def insta2shp(fotos):
    for foto in fotos:
        try:
            tit=foto['caption']['text']
            title=tit.encode('ascii', 'xmlcharrefreplace')
        except:
            title='none'
            
        fid=foto['id']
        source=foto['images']['standard_resolution']['url']
        lat=foto['location']['latitude']
        lng=foto['location']['longitude']
        time=foto['created_time']
        
        parse (lng, lat, fid, source, title, time)
    return

if __name__ == '__main__':
    print 'inicio tests instagram'
    setup()
    it=0

    while True:
        try:
            it+=1
            print it,
            for i in punts:
                consulta = getUrl(i[0],i[1])
                fotos = instagram_call(consulta)
                insta2shp(fotos)
                print nFotos,'/',
                #print i , '//' ,nFotos, '//',currentT,'//' ,getUrl(i[0],i[1])[42:127]
                #print getUrl(i[0],i[1])
            currentT = updateDate()
            time.sleep(1)
        except:
            print 'try again... ... ...'
            
    print 'fin    tests instagram'
        

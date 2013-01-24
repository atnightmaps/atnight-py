# -*- coding: cp1252 -*-
import urllib2
import json
import time
import shapefile
import punts_data
import config

#enuncia variable global contador de llamadas
global requestN
requestN=0

placesParsed=0

##files='glocal_01'
##
##lat='41.40402'
##lon='2.18804'

radius='177'

key1=''
key2=''
key3=''
key4=''
key5=''
key6=''
key7=''
key8=''
key9=''
key10=''
key11=''
key12=''
key13=''
key14=''
key15=''
key16=''
key17=''
key18=''
key19=''
key20=''

query=''
sensor='false'
types='restaurant'
pagetoken=''



listTypes=['bar','bank','accounting', 'store', 'church','shopping_mall', 'night_club',
           'clothing_store', 'liquor_store',
           'airport', 'amusement_park', 'aquarium', 'art_gallery', 'atm',
           'bakery',   'beauty_salon', 'bicycle_store', 'book_store',
           'bowling_alley',
           'cafe','restaurant','food', 'school','parking', 'pharmacy','police','post_office',
           'convenience_store','museum', 'gym', 'grocery_or_supermarket', 'florist',
           'health', 'hindu_temple', 'bus_station',  
           'campground', 'car_dealer', 'car_rental',
           'car_repair', 'car_wash', 'casino', 'cemetery', 'city_hall', 
           'courthouse', 'dentist', 'department_store', 'doctor', 'electrician',
           'electronics_store', 'embassy', 'establishment', 'finance', 'fire_station', 
           'funeral_home', 'furniture_store', 'gas_station', 'general_contractor',
           'hair_care', 'hardware_store', 
           'home_goods_store', 'hospital', 'insurance_agency', 'jewelry_store', 'laundry', 'lawyer',
           'library',  'local_government_office', 'locksmith', 'lodging', 'meal_delivery',
           'meal_takeaway', 'mosque', 'movie_rental', 'movie_theater', 'moving_company', 
           'painter', 'park',  'pet_store', 'physiotherapist',
           'place_of_worship', 'plumber',   'real_estate_agency', 
           'roofing_contractor', 'rv_park',  'shoe_store',  'spa', 'stadium',
           'storage',  'subway_station', 'synagogue', 'taxi_stand', 'train_station', 'travel_agency',
           'university', 'veterinary_care', 'zoo']

def changeKey():
    keys=[key1,key2,key3,key4,key5,key6,key7,key8,key9,key10,key11,key12,key13,key14, key15,key16,key17,key18,key19,key20]
    i=0
    global key
    while True:
        for i in keys:
            key=i
            yield key

ck=changeKey()
key=ck.next()

def getUrl(lat, lon, radius,types,sensor,key, query='',pagetoken=''):
    url= 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+lat+','+lon \
    +'&radius='+radius \
    +'&query='+query \
    +'&types='+types \
    +'&sensor='+sensor \
    +'&pagetoken='+pagetoken \
    +'&key='+key
    #print url
    return url

# ver que pasa cuando repetimos mas de veinte preguntas u ocho
def glocal_call(url):
    global requestN
    while True:
        it=0
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            content = response.read()
            data = json.loads(content)
            places=data['results']
            requestN += 1   
            print (requestN),
            return data
        except:
            print 'error en glocal_call()'
        #print 'call: '+it
                    
# toma puntos   
def getPoint(n):
    return punts_data.punts[n]

def lenPoint():
    return len(punts_data.punts)

#toma types
def getType(n):
    return listTypes[n]

def lenTypes():
    return len(listTypes)
    
def parse(data, types):
    places=data['results']
    global placesParsed
    for place in places:
        lat=place['geometry']['location']['lat']
        lng=place['geometry']['location']['lng']
        name=place['name']
        name=name.encode('ascii', 'xmlcharrefreplace')
        idp=place.get('id')
        rating=place.get('rating')
        ref=place.get('reference')
        
        e= shapefile.Editor(shapefile=types)
        e.point(lng,lat,0,0)
        e.record(idp, name, rating, types, lat, lng, ref)
        e.save(types)

        placesParsed+=1
        print placesParsed,
    return

def setupShape(types):
    try:
        shapefile.Reader(types)
        print 'ya existe un shape'
    except:
        w= shapefile.Writer(shapeType=1)
        w.autobalance=1

        w.point(0,0,0,0)

        w.field('idp','C','50',0)
        w.field('name','C','100',0)
        w.field('rating','C','10',0)
        w.field('types','C','50',0)
        w.field('lat','C','20',10)
        w.field('lng','C','20',10)
        w.field('ref','C','255',0)
        
        w.record('0','0','0',types,'0','0','0')
           
        w.save(types)

        print('shp file created')
    return

def getToken(data):
    token=data.get('next_page_token')
    print '/////////////////////////////////////////////// ',token
    if token == None:
        token=''
        print '/////////////////// no mas consultas sobre este punto'
    return token

def getStatus(data):
    status = data.get('status')
    return status

def searchPlaces(point, types, pagetoken):
    lat=point[0]
    lon=point[1]
    url = getUrl(lat, lon, radius,types,sensor,key, query='',pagetoken=pagetoken)
    places = glocal_call(url)
    #print places
    ## verifica si ha ido todo ok
    #print places
    status=getStatus(places)
    print 'status is : ', status
    if status == u'OVER_QUERY_LIMIT':
        ck.next()
        print 'key changed : ',key
        return 'problems'
    parse(places,types)
    pagetoken=getToken(places)
    print ' +1 ',
    if pagetoken!= '':
        time.sleep(10) 
        searchPlaces(point, types, pagetoken)
    return

def saveConfig(tId, pId):
    config=('tId, pId =' + str(tId) + ', '+ str(pId))
    with open(('config.py'), 'w') as f:
        f.write(config)   
    return
    
def runSearch():
    tId=config.tId
    pId=config.pId    
    while tId < (lenTypes()):
        pagetoken=''
        types = getType(tId)
        setupShape(types)
        while pId <(lenPoint()):
            print pId, lenPoint(), types
            point = getPoint(pId)
            saveConfig(tId, pId)
            search=searchPlaces(point, types, pagetoken)
            if search=='problems':
                pId-=1
            pId += 1
        else:
            pId = 0
            tId = tId + 1
        
        print tId, pId
        
    print 'glocal is finished'
    return

if __name__ == '__main__':
    runSearch()

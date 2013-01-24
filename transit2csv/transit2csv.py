import urllib2
import csv
import datetime
import time

getUrl= 'http://www.bcn.cat/transit/dades/dadestrams.dat'
files='transit.csv'
def loadTransit():
    while True:
        try:
            request = urllib2.Request(getUrl)
            response = urllib2.urlopen(request)
            content = response.read()
            return content
        except:
            print 'problemas con loadTransit()'
            
def parse(row):
    with open((files+'.csv'), 'ab') as f:
        csvFile = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        csvFile.writerow(row)     
    return

# todo se desarrolla aqui
def prepareData():
    data = loadTransit()
    lista = data.split('\n')
    lista.pop()
    now = datetime.datetime.now()
    nowf = now.strftime("%Y/%m/%d %H:%M:%S")
    print nowf
    for i in range(len(lista)):
        tram=lista[i].split('#')
        row=(nowf,(tram[1][0:4]+'/'+tram[1][4:6]+'/'+tram[1][6:8]+' '+tram[1][8:10]+':'+tram[1][10:12]+':'+tram[1][12:14]),tram[0],tram[2])
        parse (row)

if __name__ == '__main__':
    
    while True:
        prepareData()
        time.sleep(1800)   

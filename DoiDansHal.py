'''Programme qui prend en entré une liste de DOIs et récupère via l'API de Hal les valeurs des champs suivants :
 halId_s,fileType_s,linkExtId_s
ML 2019 07 
copyleft'''

import urllib.request, urllib.parse, urllib.error
import json, csv
import ssl

prehal = 'https://api.archives-ouvertes.fr/search/?wt=json&fq=doiId_s:'
posthal = '&fl=halId_s,fileType_s,linkExtId_s'
dois = open('allDois.txt')
output = open('export.txt', 'w')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open('output-table.csv', mode='w', newline='') as table:
    writer = csv.writer(table, delimiter=',')
    writer.writerow(['doi', 'hal', 'halid', 'haldepot', 'oaext'])

    count = 0
    remoDouble = list()
    for doi in dois:
        doi = doi.strip()
        if doi in remoDouble: continue

        remoDouble.append(doi)
        doilk = '=LIEN.HYPERTEXTE(\"http://doi.org/'+doi+'\";\"'+doi+'\")'
        req = prehal + doi + posthal
        #output.write(req +'\n')

        uh = urllib.request.urlopen(req, context=ctx)
        data = uh.read().decode()
        js = json.loads(data)

        halbool = js['response']['numFound']
        if halbool == 0:
            print(count, halbool)
            writer.writerow([doilk, halbool, 0, 0, 0])
            count +=1
            continue

        halid = js['response']['docs'][0]['halId_s']

        try:
            haldepot = js['response']['docs'][0]['fileType_s'][0]
        except:
            haldepot = '0'

        try:
            oaext = js['response']['docs'][0]['linkExtId_s']
        except:
            oaext = '0'

        #output.write(doi+' , '+halbool+' , '+halid+' , '+haldepot+' , '+oaext+'\n')
        print(count, halbool, halid, haldepot, oaext)
        halid =  '=LIEN.HYPERTEXTE(\"http://hal.archives-ouvertes.fr/'+halid+'\";\"'+halid+'\")'

        writer.writerow([doilk,halbool, halid, haldepot, oaext])

        count +=1
        #if count > 5: break

output.close()

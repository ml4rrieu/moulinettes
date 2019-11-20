import requests

#un fichier texte de sortie pour coller la réponse de sword
out = open('04-zconsol.txt', 'w') 

url = 'https://api-preprod.archives-ouvertes.fr/sword/hal'
service = 'https://api.archives-ouvertes.fr/sword/servicedocument'

headers = {
    'Packaging': 'http://purl.org/net/sword-types/AOfr',
    'Content-Type': 'text/xml', #ou application/zip pour charger les fichiers
}

#data = open('./TEI/source/art2.xml')
data = open('ART.xml', encoding='UTF-8')
print('TEI has been loaded')

response = requests.post(url, headers=headers, data=data, auth=('urLogin', 'urpass'))


out.write(response.text) #coller la réponse de SWORD dans fichier texte
data.close()
out.close()
print("done")




'''
documentation SWORD HAL : https://api.archives-ouvertes.fr/docs/sword
fichier TEI pour TEST : https://api.archives-ouvertes.fr/documents/art.xml

la méthode CURL présente dans la docs
curl -X POST -d @meta.xml -v -u 
login:password https://api.archives-ouvertes.fr/sword/hal/ 
-H "Packaging:http://purl.org/net/sword-types/AOfr" 
-H "Content-Type:text/xml" -H "On-Behalf-Of: login|marvin;idhal|arthur-dent;ORCID|0000-0002-9079-593X"
'''

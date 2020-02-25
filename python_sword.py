import requests

#txt file to write the requests answer
out = open('feedback.txt', 'w') 

url = 'https://api-preprod.archives-ouvertes.fr/sword/hal'
# do it manually, service is 'https://api.archives-ouvertes.fr/sword/servicedocument' 
	
#or Content-Type : application/zip to upload pdf file
headers = {
    'Packaging': 'http://purl.org/net/sword-types/AOfr',
    'Content-Type': 'text/xml',
}

xmlfile = open('./TEI/ART.xml', encoding='utf-8')
print(xmlfile)
print('TEI has been loaded')

response = requests.post(url, headers=headers, data=xmlfile, auth=('user', 'pass'))

out.write(response.text)# parse answer to the txt file

print("done")
xmlfile.close()
out.close()



'''
SWORD HAL documentation : https://api.archives-ouvertes.fr/docs/sword
fichier TEI pour TEST : https://api.archives-ouvertes.fr/documents/art.xml

la méthode CURL présente dans la doc
curl -X POST -d @meta.xml -v -u 
login:password https://api.archives-ouvertes.fr/sword/hal/ 
-H "Packaging:http://purl.org/net/sword-types/AOfr" 
-H "Content-Type:text/xml" -H "On-Behalf-Of: login|marvin;idhal|arthur-dent;ORCID|0000-0002-9079-593X"
'''

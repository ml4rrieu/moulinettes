'''
Retrouver ses projets ANR dans la liste nationale des projets financés
Données ANR : https://www.data.gouv.fr/fr/datasets/projets-finances-hors-pia-2005-2019-partenaires/
1. Depuis Hal, charge le nom et le rnsr de vos structures
2. Scanne ensuite des données anr afin d'identifier les projets liés à votre institution
'''
import requests, json, csv

structId = '81173'
def reqHal():
	url = 'https://api.archives-ouvertes.fr/ref/structure/?rows=100&q=parentDocid_i:'+structId+'&fl=name_s,rnsr_s'
	print(url)
	req= requests.get(url)
	req = req.json()
	namelist = req['response']['docs']
	return namelist
	

def loadThisRow(row):
	temp = []
	for f in fields : 
		temp.append(row[f])
	writer.writerow(temp)

d = reqHal()
loadTitles = []
loadRnsr = []
for item in d : 
	loadTitles.append(item['name_s'].lower())
	try : 
		item['rnsr_s']
	except : pass
	else :
		for r in item['rnsr_s'] : loadRnsr.append(r)	
		
print("nb of lab titles", len(loadTitles))
print("nb of rnsr", len(loadRnsr))


nameFile = '00anr-horspia-2005-19-projets-finances-partenaires-20200423.csv'
uvsqAnr = open("uvsqAnr.csv", 'w', newline='')
writer = csv.writer(uvsqAnr)
fields = ['Code Décision Projet', 'Acronyme Projet', 'Code Décision Partenaire', 'Coordinateur (Oui/Non)', 'Nom Partenaire', 'Catégorie du Partenaire', 'Numéro RNSR', 'Nom du responsable scientifique', 'Prénom du responsable scientifique', 'Ville de réalisation des travaux', 'Région de réalisation des travaux', 'Pays de réalisation des travaux']
writer.writerow(fields)

with open(nameFile, 'r', newline='', encoding='utf-8' ) as fh : 
	reader = csv.DictReader(fh)
	match = 0 
	for row in reader : 
		lab = row['Nom Partenaire'].lower()
		if 'uvsq' in lab or \
		('univ' in lab and 'versailles' in lab) or \
		('univ' in lab and 'quentin'in lab) or \
		row['Numéro RNSR'] in loadRnsr :
			loadThisRow(row)
			match +=1
			continue

		for title in loadTitles : 
			if title in lab : 
				loadThisRow(row)
				match +=1
			
			

print('nb of project finded', match)
uvsqAnr.close()





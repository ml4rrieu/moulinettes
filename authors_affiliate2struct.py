'''
Contexte : identifier les auteurs qui possèdent des publications affiliées à une structure Hal, 
et déduire le nombre d'article de revues par auteur qui pourraient être déposés en pdf.
Dans le but de les solliciter par mail

en entrée : identifiant hal structure
en sortie : table et json avec les champs suivants : 'name', 'id', 'idHal', 'hasCV','orcid', 'docsDejaDeposees','pdfADeposer','uris'
ML
2020-03
'''
import requests, json, csv

def reqHal(suffix):
	url = 'https://api.archives-ouvertes.fr/'
	r = requests.get(url+suffix)
	r = r.json()
	# print(json.dumps(r, indent=4))
	num = r['response']['numFound']
	docs = r['response']['docs']
	return [num, docs]


labId = '140307'

# __00__ get authors affiliated to structure

authData = {}
param = 'search/?rows=100&fq=docType_s:ART&fq=submitType_s:notice&fq=producedDate_tdate:[1900-01-01T00:00:00Z TO NOW-1YEARS/DAY]&fq=authStructId_i:'+labId+'&fl=structHasAuthId_fs,uri_s'
docs = reqHal(param)

for doc in docs[1]:
	# print('\n',doc['uri_s'])
	for auth in doc['structHasAuthId_fs'] : 
		if auth.startswith(labId+'_Facet') : 
			# auth is from LAB
			lIdx = auth.index("JoinSep") + len("JoinSep_")
			rIdx = auth.rindex("_FacetSep")
			name =auth[rIdx+len("_FacetSep_"):]
			authId = auth[ lIdx : rIdx ]
			
			if name not in authData.keys() : 
				# print('\t new auth', authId)
				authData[name] = {
				'id':[authId], 
				'nb':1 ,
				'uris':[doc['uri_s']]
				}

			else :
				# print('\t add this uris to', authId)
				if authId not in authData[name]['id'] : authData[name]['id'].append(authId)
				authData[name]['nb'] += 1
				authData[name]['uris'].append(doc['uri_s'])
	

print('nb of doc : ', docs[0])
print('nb of authors : ', len(authData))
# print(json.dumps(authData, indent=2))


# __01__ enrich authors data with authors referentiel

fields = ['idHal_s', 'hasCV_bool', 'orcid_id']

for name in authData : 
	params = 'ref/author/?q=fullName_s:"'+name+'"&fl=fullName_s,idHal_s,hasCV_bool,orcid_id'

	authForms = reqHal(params)
	for i in authForms[1] : 
		for f in fields : 
			if f in i.keys() :
				# print(auth, 'has', f)
				authData[name][f] = i[f]
			else : 
				authData[name][f] = ''

	## auth has already deposit a file ? 
	contrib = reqHal('search/?q=contributorFullName_s:"'+name+'"')
	authData[name]['nbOfDeposit']= contrib[0]


# print(json.dumps(authData, indent=1))


# __0Z__ export data json & CSV

jsonfh = open('cemotev-auth.json', 'w')
json.dump(authData, jsonfh)

header = ['name', 'id', 'idHal', 'hasCV','orcid', 'docsDejaDeposees','pdfADeposer','uris']

csvfh = open('cemotev-auth.csv', 'w', newline='', encoding="utf-8")
writecsv = csv.writer(csvfh, delimiter =',')
writecsv.writerow(header)

for name in authData : 
	auth = authData[name]
	if 'idHal_s' not in auth.keys(): #si auteur pas trouvé dans le ref auth de Hal
		print('auth not finded in ref auth : ', auth)
		continue

	row = [name, ','.join(auth['id']), auth['idHal_s'], auth['hasCV_bool'], auth['orcid_id'], auth['nbOfDeposit'], auth['nb']]
	for i in auth['uris'] : row.append(i)
	
	writecsv.writerow(row)
	print(name, 'exported')
	
csvfh.close()

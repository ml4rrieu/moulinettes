# codes et méthodes réalisées dans le cadre du projet IPERU
[2020 à l'UVSQ](#iperu-2020-%C3%A0-luvsq--retour-sur-le-rep%C3%A9rage-effectu%C3%A9-dans-le-cadre-diperu)

[2016 à l'UPEM](#iperu-2016-%C3%A0-lupem--m%C3%A9thode-et-code)

# IPERU 2020 à l'UVSQ : retour sur le repérage effectué dans le cadre d'IPERU

Objectif : a partir d'une liste d'affiliation identifier celles qui relèvent du périmètre de l'UVSQ. Particularité :  le travail se fait au niveau des affiliations et non des publications. Aussi les noms d'auteur ne sont pas disponibles : l'identification doit se faire à partir de la lecture de l'affiliation.

Exemple d'affiliation `Univ Paris Saclay, INRA, Mol Virol & Immunol Unit VIM, F-78350 Jouy En Josas, France`


## Mémo
format d'encodage des caractères : windows-1252/WinLatin1. Separateur : `; `

Colonne **statut** correspond au statut avant repérage. Valeurs possibles : 
``` C : nouvelles adresses pré cochées par l'OST 
NC : nouvelles adresses non pré cochées           
NR : anciennes adresses marqués laissés non repéré par l'établissement                
O : anciennes adresses repérées à oui
N : anciennes adresses repérées à Non              
```

Colonne **Reperage** correspond au statut en cours de repérage. Valeurs possibles : 
```O (oui)
N (non)
NR (non repéré
```


## Méthodes appliquées
Conception de trois filtres, permettant de déduire l'appartenance d'une affiliation ("aff" par la suite) :
* filtre sur l'université : l'aff contient-elle des infos sur l'université (eg. uvsq, univ. versailles, univ st quentin)
* filtre sur les laboratoires : l'aff contient-elle des infos sur les laboratoires (présence de deux niveaux d'info : un premier sur le laboratoire (sigle ou forme longue ou numéro d'unité) et un second sur les tutelles (présence d'au moins une tutelle) ) 
* filtre sur les hopitaux : l'aff contient-elle des informations sur les hopitaux avec lesquels l'univ. est en lien ?

**Étape 1** verification automatique

Exécutez le code _a_filter_all_aff.py_, qui produit la table _all_aff_automat_deduction.csv_

**Étape 2** verif. manuelle

2a. Vérifier manuellement ce qui a été filtré, ce qui a été identifié automatiquement et qui n'a pas été pré-coché par l'OST

2b. Vérifier le résidu :  ce qui n'a pas été identifié automatiquement mais qui a été précoché par l'OST

**Étape 3** consolider les données

avec le code _b_deduce_reperage_and_conforme_data.py_ déduire la table _aff_uvsq_auto.csv_ : les affiliations identifiées automatiquement;

Modifier cette dernière selon les résultats de létape 2a. ;

Ajouter les résultats de l'étape 2b.

Enregistrer la table _aff_uvsq_auto_plus_manuel.csv_

**Étape 4**

Exécutez le script "conform data" du code _b_deduce_reperage_and_conforme_data.py_ (si l'affiliation n'est pas de l'uvsq (Reperage = N) il retire les valeurs de la colonne   `intra_inst3` ); 

table de sortie  _aff_uvsq_for_ost.csv_ (sep ; & windows-1252/WinLatin1 )

**Étape 5**

Charger _aff_uvsq_for_ost.csv_ dans l'interface de l'OST

## Statistiques pour 2019

nb d'affiliations :  93182

nb d'affiliations à traiter (nouvelles et anciennes non repérées) : 93179

nb d'affiliations validées : 2757

nb de publication correspondant : 2235

nb de publication trouvées dans le cadre du [Baromètre sicence ouverte uvsq en 2019](https://github.com/ml4rrieu/barometre_science_ouverte_uvsq) : 2869

<br /><br />
Donc l'OST calcul des indicateurs sur maximum 78 % des publications de l'université.
(en réalité c'est moins car le périmètre de l'OST inclut les publications des hopitaux seuls, ce qui n'est pas inclus dans le baromètre de la science ouverte).

## Codes
##### _a_filter_all_aff_
```python
import csv, re, pandas as pd
lines_to_del = []


## __0__ load data
#df = pd.read_csv("./data_source/test_affil.csv", sep = ";", encoding = "windows-1252", index_col="adrCleost")
df = pd.read_csv("./data_source/VERSAILLES_reperage_2013.csv", sep = ";", encoding = "windows-1252", index_col="adrCleost")
print("nb of affil", len(df.index))

# load laboratory information (sigle, code, tutelles)
with open("../00 data/labData.csv", newline='', encoding='utf8') as fh : 
	reader = csv.DictReader(fh)
	# coller les données des laboratoires dans un dict
	## ATTENTION il faut exclure les labos pour lesquels l'uvsq n'est pas tutelle pour l'année de traitement
	## 2020 :  vima & breed
	## 2016 :  liparad
	## 2015 2i, b2phi, cesdip, david, endicap, gemac, ilv, latmos, lmv, lsce, printemps, vima

	labData = {row["sigle"]: row for row in reader if row["sigle"] not in ["liparad", "vima", "breed"]}
	

#selection des affils à traiter (les nouvelles et les non traitées)
aff2treat = df[ (df["Statut"] == "C") | (df["Statut"] == "NC") | (df["Statut"] == "NR") ].copy()
print("nb adresse à traiter", len(aff2treat))


#____1_______________________________________
## search univ presence in affiliation
def deduce_uvsq_presence(row) : 
	"""recherche de l'université dans l'affiliation"""
	aff = row["adresse"].lower()
	
	is_uvsq = False
	## si l'affiliation contient uvsq : c'est valide
	if "uvsq" in aff : 
		is_uvsq = True

	# trouver la forme univ st quentin en yvelines
	if "univ" in aff and "quentin" in aff and "yvelin" in aff: 
		is_uvsq = True

	## si on a univ et versailles s'assrer que le versailles correspond à l'univ et non à la ville
	if not is_uvsq and "univ" in aff and "versaill" in aff : 
		cut = re.split("\W+", aff)
		#récupérer les index où versailles est présent
		indexList = []
		[indexList.append(i) for i in range(len(cut)-1) if "versailles" == cut[i]]

		#si on a plusieurs fois versailles, alors c'est valide
		if len(indexList)>1 : 
			is_uvsq =  True
		
		#si une seule occurence s'assurer que ce n'est pas la ville
		if len(indexList) == 1 : 
			is_uvsq = True
			versaillesIdx = indexList[0]

			#exclure les cas où versailles est mentionné comme ville
			if (versaillesIdx > 0 and cut[versaillesIdx-1] == "78000") or \
			(versaillesIdx < len(cut)-1 and cut[versaillesIdx+1] == "france") : 
				is_uvsq = False

	return is_uvsq


aff2treat["uvsq_inside"] = aff2treat.apply(lambda row : deduce_uvsq_presence(row), axis = 1)
print("nb of uvsq finded", len(aff2treat[ aff2treat["uvsq_inside"] == True]) )


#____2_______________________________________
## search lab presense in affilition

def searchFormeLg(data, fromcsv):
	"""utilisé dans verif_lab_presence """	
	cut = fromcsv.split(',')
	regtotal = len(cut)
	regcount = 0
	for i in cut:
		i = i.strip()
		if re.search(i, data): regcount +=1
	
	return 1 if regcount == regtotal else 0
	
def deduce_lab_presence(row) : 
	"""recherche des labos dans l'affiliation"""
	aff = row["adresse"].lower()
	affsplit = re.split("\W+", aff)

	labFinded = False
	for lab in labData :
		sigle = code = lablg = tutelles = 0

		#__a. search for lab element
		if lab in affsplit : sigle = 1
		if labData[lab]["code1"] in affsplit and labData[lab]["code2"] in affsplit : code = 1
		lablg = searchFormeLg(aff, labData[lab]["regexp"])

		#__b. search for tutelle element
		labTutelles = ['uvsq', 'versaill', 'saclay']
		ext_tut = labData[lab].get("tutelle suppl")
		if ext_tut :
			[labTutelles.append(tut.strip().lower()) for tut in ext_tut.split(",")]
		for tut in labTutelles : 
			if tut in aff : 
				tutelles = 1

		#__c. deduce if lab in aff
		if sigle + code + lablg > 0 and tutelles > 0 : 
			#print(sigle, code, lablg, tutelles)
			labFinded = True
			break

	return labFinded


aff2treat["lab_inside"] = aff2treat.apply(lambda row : deduce_lab_presence(row), axis = 1)
print("nb of labo finded", len(aff2treat[ aff2treat["lab_inside"] ]) )

#____3_______________________________________
## add hospital affiliations
hosp = {
"ambroise pare" : ["boulogne", "billancourt"],
"chi poissy" : ["possy"], 
"raymond poincare" : ["garche", "aphp", "ap hp"],
"andre mignot" : ["versailles", "chesnay", "chv"], 
}
	
def deduce_hospital(row) : 
	aff = row["adresse"].lower()
	hosp_inside = False
	
	for k, v in hosp.items() : 
		if k in aff : 
			for extra in hosp[k] : 
				if extra in aff : 
					hosp_inside = True
					break		

	return hosp_inside

aff2treat["hospital_inside"] = aff2treat.apply(lambda row : deduce_hospital(row), axis = 1)


#____4_______________________________________
## gather all 3 precedent filters in is_uvsq column

aff2treat["is_uvsq"] = (aff2treat["uvsq_inside"]) | (aff2treat["lab_inside"]) #| (aff2treat["hospital_inside"])
print("nb of aff finded", len(aff2treat[ aff2treat["is_uvsq"]].index) )

aff2treat.to_csv("./data_out/all_aff_automat_deduction.csv")

#____Z_______________________________________
## outputs extract of result for verifications

# verif 1. extraire les affils non identifiés par l'OST mais identifiés par nous
perso_yes_ost_no = aff2treat[ (aff2treat["Statut"] == "NC") & (aff2treat["is_uvsq"]) ]
if len(perso_yes_ost_no.index) > 0 : 
	perso_yes_ost_no.to_csv("./verif/perso_yes_ost_no.csv")



# verif 2. extraire les affils pré cochés par l'OST mais pas par nous
ost_yes_perso_no = aff2treat[ (aff2treat["Statut"] == "C") & (aff2treat["is_uvsq"] == False) ]
if len(ost_yes_perso_no.index) > 0 : 
	ost_yes_perso_no.to_csv("./verif/ost_yes_perso_no.csv")

```

##### _b_deduce_reperage_and_conforme_data.py_
```python
import pandas as pd

#__________________________________ REDUIRE LES DONNES A CELLES RELEVANT BIEN DE L'UVSQ
df = pd.read_csv("./data_out/all_aff_automat_deduction.csv")

df = df[ df["is_uvsq"]].copy()
df["Reperage"] = "O"
df.drop(columns=["is_uvsq"], inplace = True)
df.to_csv("./data_out/aff_uvsq_auto.csv", index=False)

exit()


#___________________________________ DERNIERE ETAPE : SI CE N EST PAS DE L UVSQ EFFACER LES CHAMPS Intra_inst_3 et 4

df = pd.read_csv("./data_out/aff_uvsq_auto_plus_manuel.csv", index_col=False)
print("longueur de table importées", len(df.index))

df_no_uvsq = df.loc[ df["Reperage"] == "N", :].copy()
df_no_uvsq["Intra_inst_3"] = ""
df_no_uvsq["Intra_inst_4"] = ""


df_is_uvsq = df.loc[ df["Reperage"] == "O", :]
lastdf = pd.concat([df_no_uvsq, df_is_uvsq])
print("longueur table après traitement", len(lastdf.index))

lastdf.drop(columns=["uvsq_inside", "lab_inside", "hospital_inside"], inplace = True)
lastdf.to_csv("./data_out/aff_uvsq_auto_plus_manuel_for_ost.csv", sep=";", encoding="windows-1252", index= False)
```





<br /><br />
# IPERU 2016 à l'UPEM : méthode et code

### Introduction
L’OST (Observatoire des sciences et techniques) dirige un projet nommé IPERU (Indicateurs de Production des Établissements de Recherche Universitaire) qui a pour fin d’établir des indicateurs de productions sur les publications publiées annuellement par les établissements de la recherche. 
Selon le positionnement géographique de l’établissement, l’OST sélectionne une quantité importante de références présents dans le WOS. Ensuite l’OST contacte les établissements et demande aux documentalistes de repérer, via une interface web dédiée, les références qui correspondent bien à leur établissement.

Dans notre contexte, il s’agit donc d’identifier les références qui appartiennent à un laboratoire dont l’UPEM est la tutelle. Ce travail doit faire face à deux difficultés :
- les laboratoires peuvent avoir plusieurs tutelles ;
- aucune norme n’existe pour structurer ces références, tant au niveau des tutelles, que des revues ou encore des bases de données.

En conséquence, il existe tout un ensemble de signatures pour se référer à un même laboratoire. Par exemple pour le LAMA, en juin 2016, plus de 300 variantes d’affiliations ont été trouvées dans des articles publiés entre 2010-15.

Deux exemples de variantes d’affiliations :
-Univ Francaise, Lab Anal & Math Appl, CNRS, UMR 8050, F-77454 Marne La Vallee 2, France
-Lab. Anal. Math. Appl. (UMR CNRS 8050), Université Paris-Est, 61 Av. du Gé de Gaulle, F-94010 Créteil de Gaulle, France

Pour l’année 2015 la pré-sélection géographique de l’OST concerne 58 709 références : il nous faut parmi celles-ci faire le tri.

### Méthodologie

Nous avons travaillé sur les références de 2015. Afin de repérer celles de l’UPEM, nous avons utilisé différentes méthodes, parfois automatiques parfois semi-automatiques. Le passage d’une méthode à l’autre se fait en retirant les références qui ont été validées précédemment (la méthode 2 est appliquée sur toutes les références moins celles qui ont été validées par la méthode 1, etc.)

Une méthode se déroule en trois temps :
        extraire les références de l’interface de l’OST
        effectuer les identifications
        importer les références validées dans l’interface de l’OST

### METHODE UNE : correspondance d’ affiliations
Un avantage d’Opalia est de retenir les correspondances (matching) faites manuellement par les documentalistes, entre les affiliations présentes sur les articles et le nom des laboratoires. À l’issue des travaux réalisés sur Opalia il résulte donc, pour chaque laboratoire, des dictionnaires : des fichiers textes qui regroupent ces différentes affiliations.
Le dictionnaire global de la tutelle UPEM, regroupant tous les dictionnaires de ses laboratoires, totalise 1 552 affiliations.

Cette première méthode consiste à trouver dans les affiliations pré-sélectionnées par l’OST (58 709) celles qui correspondent aux affiliations présentes dans le dictionnaire global de l’UPEM.

Résultat : 133 références repérées


code processing
```processing
ML 2016-05-30

Table input ; 
StringList affil;
String[] labos = {"ACP", "DICEN", "ERUDITE", "ESYCOM", "IRG", "LABURBA", "LAMA", "LATTS", "LGE", "LIGM", "LIPHA", 
  "LISAA", "LISIS", "LVMT", "MSME"};

void setup() {
  input = loadTable("../table/in2015noSemi.csv", "header");
  //input.addColumn("autoReperage");
  affil = new StringList();
  println("nb OST ref " + input.getRowCount());

  //load all affiliations from dico into StringList affil
  for (int i=0; i< labos.length; i++) {
    String[] affilTemp = loadStrings("../"+labos[i]+".txt");
    for (int j=0; j<affilTemp.length; j++) affil.append(trim(affilTemp[j]));
  }
  println("nb opalia affil "+affil.size()+'\n' );

  //iterate throw ref and tchek if it is an affil
  for (int i=0; i<input.getRowCount(); i++) { //
    String addr = input.getString(i, "adresse");
    if (affil.hasValue(trim(addr))) input.setString(i, "Reperage", "O");
  }

  saveTable(input, "../out2015dico.csv");
  exit();
}

```

### METHODE DEUX correspondance laboratoire ET tutelle

Cette méthode recherche pour chaque affiliation (i) un sigle ou numéro d’un laboratoire de l’UPEM et (ii) un sigle d’une tutelle attachée à l’UPEM : si ces deux informations sont présentes alors celle-ci appartient à l’UPEM.

Résultat : 219 affiliations repérées

Remarque : Une vérification manuelle à été nécessaire car un laboratoire est un faux ami : LISIS fait tantôt référence à un laboratoire de l’UPEM (Laboratoire Interdisciplinaire Sciences Innovations Sociétés) tantôt à un laboratoire de l’IFFSTAR (Laboratoire Instrumentation, Simulation et Informatique scientifique).

*code processing*
```processing
 ML 2016-05-30
Table input ; 
String[] labo = {"ACP", "3350", "DICEN", "4420", "ERUDITE", "437", "3435", 
  "ESYCOM", "2552", "IRG", "2354", "LABURBA", "3482", "LAMA", "8050", "LATTS", "8134", 
  "LIGE", "4508", "LIGM", "4089", "LIPHA", "4118", "LISAA", "4120", "LISIS", "1326", "LVMT", "T9403", "MSME", "8208"};

String[] tutelle = {"CNAM", "UPEC", "CRETEIL", "crÃ©teil", "ESIEE", "CNRS", "ENPC", "Ecole des Ponts", "paristech", 
  "IFSTARR", "UPEM", "UPEMLV"};

void setup() {
  StringList result =new StringList(); // a buffer to save catched ref
  input = loadTable("../table/in2015moinsDico.csv", "header");
  input.addColumn("autoReperage");
  println("nb OST ref " + input.getRowCount());

  //iterate throw all ref 
  for (int i=0; i<input.getRowCount(); i++) { //
    String addr = input.getString(i, "adresse");
    switch (isItAnUpemRef(addr)) {
    case "allMatch" :
      input.setString(i, "Reperage", "O");
      break;
    case "laboMatch" :
      input.setString(i, "autoReperage", "laboMatch");
      //result.append(addr);
      break;
    }
  }

  saveTable(input, "../table/out2015Methode2.csv");
  printArray(result.array());
  exit();
}

String isItAnUpemRef(String in) {
  String [] cut = splitTokens(in, ", -");
  trim(cut);
  boolean laboMatch = false;
  boolean tutelleMatch = false;
  String answer="";

  for (int i=0; i<cut.length; i++) {
    for (int j=0; j<labo.length; j++) {
      if (cut[i].equalsIgnoreCase(labo[j])) laboMatch = true;  // match labo
    }
  }
  if (laboMatch) {
    for (int i=0; i<cut.length; i++) {
      for (int j=0; j<tutelle.length; j++) {
        if (cut[i].equalsIgnoreCase(tutelle[j])) tutelleMatch = true;
      }
    }
  }
  if (laboMatch && tutelleMatch) answer ="allMatch";
  if (laboMatch && !tutelleMatch) answer = "laboMatch";
  return answer;
}

```



# méthodologie et code réalisé pour IPERU 2016 à l'UPEM

#Introduction
L’OST (Observatoire des sciences et techniques) dirige un projet nommé IPERU (Indicateurs de Production des Établissements de Recherche Universitaire) qui a pour fin d’établir des indicateurs de productions sur les articles publiés annuellement par les établissements de la recherche. 
Selon le positionnement géographique de l’établissement, l’OST sélectionne une quantité importante de références d’articles présents dans le WOS. Ensuite l’OST contacte les établissements et demande aux documentalistes de repérer, via une interface web dédiée, les références qui correspondent bien à leur établissement.

Dans notre contexte, il s’agit donc d’identifier les références qui appartiennent à un laboratoire dont l’UPEM est la tutelle. Ce travail doit faire face à deux difficultés :
- les laboratoires peuvent avoir plusieurs tutelles ;
- aucune norme n’existe pour structurer ces références, tant au niveau des tutelles, que des revues ou encore des bases de données.

En conséquence, il existe tout un ensemble de signatures pour se référer à un même laboratoire. Par exemple pour le LAMA, en juin 2016, plus de 300 variantes d’affiliations ont été trouvées dans des articles publiés entre 2010-15.

Deux exemples de variantes d’affiliations :
-Univ Francaise, Lab Anal & Math Appl, CNRS, UMR 8050, F-77454 Marne La Vallee 2, France
-Lab. Anal. Math. Appl. (UMR CNRS 8050), Université Paris-Est, 61 Av. du Gé de Gaulle, F-94010 Créteil de Gaulle, France

Pour l’année 2015 la pré-sélection géographique de l’OST concerne 58 709 références : il nous faut parmi celles-ci faire le tri.

#Méthodologie

Nous avons travaillé sur les références de 2015. Afin de repérer celles de l’UPEM, nous avons utilisé différentes méthodes, parfois automatiques parfois semi-automatiques. Le passage d’une méthode à l’autre se fait en retirant les références qui ont été validées précédemment : la méthode 2 est appliquée sur toutes les références moins celles qui ont été validées par la méthode 1, etc.
Enfin, une méthode se fait en trois temps :
        extraire les références de l’interface de l’OST
        effectuer les identifications
        importer les références validées dans l’interface de l’OST

METHODE UNE : correspondance d’ affiliations
-------------------------------------------------
Un avantage d’Opalia est de retenir les correspondances (matching), faites manuellement par les documentalistes, entre les affiliations présentes sur les articles et le nom des laboratoires. À l’issue des travaux réalisés sur Opalia il résulte donc, pour chaque laboratoire, des dictionnaires : des fichiers textes qui regroupent ces différentes affiliations.
Le dictionnaire global de la tutelle UPEM, regroupant tous les dictionnaires de ses laboratoires, totalise 1 552 affiliations.

Cette première méthode consiste à trouver dans les affiliations pré-sélectionnées par l’OST (58 709) celles qui correspondent aux affiliations présentes dans le dictionnaire global de l’UPEM.

Résultat : 133 références repérées

Remarque : il serait fort souhaitable dans Opalia que les données des dictionnaires soient structurées (sigle, numéro de laboratoire, type, nom, abréviation, tutelles). 

ML 2016-05-30
 */

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

/*
METHODE DEUX correspondance laboratoire ET tutelle
-------------------------------------------------
Cette méthode recherche pour chaque affiliation (i) un sigle ou numéro d’un laboratoire de l’UPEM et (ii) un sigle d’une tutelle attachée à l’UPEM : si ces deux informations sont présentes dans une affiliation alors celle-ci appartient à l’UPEM.

Résultat : 219 affiliations repérées

Remarque : Une vérification manuelle à été nécessaire car un laboratoire est un faux ami : LISIS fait tantôt référence à un laboratoire de l’UPEM (Laboratoire Interdisciplinaire Sciences Innovations Sociétés) tantôt à un laboratoire de l’IFFSTAR (Laboratoire Instrumentation, Simulation et Informatique scientifique).


 ML 2016-05-30
 */

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


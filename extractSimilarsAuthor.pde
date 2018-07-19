/**
Ce programme permet d'extraire, à partir d'une liste d'auteurs, les formes auteurs similaires.
La comparaison entre auteurs est simple : suppression de la casse, des espaces et des signes de ponctuation suivant : '-.
En entrée le programme charge une table qui doit avoir les trois colonnes suivantes id, nom, prenom
en sortie le programme exporte une table où les auteurs identifiés comme similaires sont placés à la suite des autres.

extract dupicate authors

can be improved
ML 2018
CC-BY
*/

Table input = new Table();
Table output = new Table();
StringDict buffer = new StringDict();

void setup() {
  input = loadTable("leNomDeVotrefichier.csv", "header"); //!\\ indiquer le nom de votre fichier tableur
  output.setColumnTitles(new String[]{"id", "nom", "prenom", "bib-id", "labo"  });
  buffer = new StringDict();
  println("nb of autors", input.getRowCount());

  // 1. past all convert names in StringDict
  for (int i=0; i<input.getRowCount(); i++) { 
    int tempId = input.getInt(i, 0);
    String tempName = convertName(input.getString(i, 1), input.getString(i, 2));
    buffer.set(str(tempId), tempName);
  }
  println("size of buffers", buffer.size());

  //2. check similarity
  IntList duplicateIds = new IntList(); 
  int duplicateNb = 0;
  for (int i=0; i<input.getRowCount(); i++) {
    duplicateIds.clear();
    int id = input.getInt(i, 0);
    String name = convertName(input.getString(i, 1), input.getString(i, 2));
    buffer.remove(str(id));
    for (String idB : buffer.keys()) {
      // si cela match et que ce n'est pas la mm row
      if (name.equals( buffer.get(idB)) && id != int(idB) ) {  
        duplicateIds.append(int(idB));
        buffer.remove(idB);
      }
    }

    //3 export duplicate authors in table
    if (duplicateIds.size() >0) {
      copyThisRow(id, duplicateIds);       
      duplicateNb += 1;
    }
  }

  println("nb of duplicate", duplicateNb);
  saveTable(output, "doublonsAuteurs.csv");
  exit();
}

void copyThisRow(int id, IntList ids ) {

  // a. copy original row
  output.addRow();
  int cellNb = input.findRowIndex(str(id), 0);
  for (int i=0; i< input.getColumnCount(); i++) {
    String data = input.getString(cellNb, i);
    output.setString( output.lastRowIndex(), i, data);
  }

  //b. add all duplicated rows
  for (int i=0; i<ids.size(); i++) {
    output.addRow();
    int cellNb2 = input.findRowIndex(str(ids.get(i)), 0);
    for (int j=0; j< input.getColumnCount(); j++) {
      String data = input.getString(cellNb2, j);
      output.setString( output.lastRowIndex(), j, data);
    }
  }
}


String convertName(String a, String b) {
  String lastName = a.toLowerCase();
  String firstName = b.toLowerCase();
  String name = lastName.concat(firstName);
  String[] shineName = splitTokens(name, " '-.");
  name = join(shineName, "");
  name.trim();
  return(name);
}

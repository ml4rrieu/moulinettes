/**
 ce code  permet d'extraire les IdHals des auteurs d'une structure , 
 les noms complets des auteurs plus leur idHals sont placés dans une table au chemin du code, 
 le numéro de votre structure est à indiquer dans la variable codeLab (ligne 13).
 
 ML 
 CC BY
 2018
 */

void setup() {

  String codeLab ="15218"; 
  
  String url = "https://api.archives-ouvertes.fr/search/?q=*:*&rows=0&facet=true&facet.field=structHasAuthIdHal_fs&facet.prefix="+codeLab+"_&wt=json&facet.limit=5000";
  JSONObject json = loadJSONObject(url);
  JSONObject child = json.getJSONObject("facet_counts").getJSONObject("facet_fields");
  JSONArray arr = child.getJSONArray("structHasAuthIdHal_fs");

  Table authIds = new Table();
  authIds.setColumnCount(2);
  authIds.setColumnTitles(new String[] {"idHal", "name"});
  println("nb of authors", arr.size());

  for (int i=0; i< arr.size(); i+=2) {

    String [] cut = split(arr.getString(i), "JoinSep_");
    if ( ! cut[1].startsWith("_FacetSep")) {
      String [] cutBis = split(cut[1], "_FacetSep_");

      TableRow row = authIds.addRow();
      row.setString(0, cutBis[0]);
      row.setString(1, cutBis[1]);
    }
  }
  println("nb of authors with IdHal", authIds.getRowCount());
  saveTable(authIds, "authIds.csv");
  exit();
}

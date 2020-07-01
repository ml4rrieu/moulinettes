'''
Script pour faire du mailing aux auteurs correspondants dont les publications ne sont pas en accès ouvert

un extrait du fichier csv entrant 'Hal Uvsq Imports - juin.csv' : 
index,state,type,lien hal,open access,qui traite,traité ?,commentaire,mail correspondant,mail envoyé
78,new,ART,https://hal.archives-ouvertes.fr/hal-02876608,closed,pesronneA,ok ,,aziz.zaanan@aphp.fr,
85,new,ART,https://hal.archives-ouvertes.fr/hal-02876615,closed,pesronneA,ok,,caroline.moine@uvsq.fr,
86,new,ART,https://hal.archives-ouvertes.fr/hal-02876616,closed,pesronneB,ok,,caroline.moine@uvsq.fr,
94,new,ART,https://hal.archives-ouvertes.fr/

'''

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import defaultdict
from string import Template 
import pandas as pd
import smtplib, json, requests
private = ['login', 'password']


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def reqHal(halId):
	base = "https://api.archives-ouvertes.fr/search/?q=halId_s:"
	req = requests.get(base+halId+"&fl=title_s")
	req = req.json()
	try : 
		return req['response']['docs'][0]['title_s'][0]
	except : 
		print(f"\n\n\nerror API HAL\n{halId}\n{base}+{halId}")
		quit()


# ____ configure SMTP server
s = smtplib.SMTP_SSL(host='smtps.uvsq.fr', port=465)
s.login(private[0], private[1])


# ____ load csv file
data = pd.read_csv('Hal Uvsq Imports - juin.csv')
sel = data.loc[(data.type =='ART') &\
(data['open access'].isin(['closed','open from publisher : no licence'])) & \
(data['mail correspondant'] !='pass')]


# ____ construct dict {email : uris}
mailNuris = defaultdict(list)
{r['mail correspondant']:mailNuris[r['mail correspondant']].append(r['lien hal']) for i,r in sel.iterrows()}
print(f"nb auteur a contacter : {len(mailNuris)}")

for mail, uris in mailNuris.items():
	#if len(uris) == 1 : continue

	title = ['- '+reqHal(link[link.find('/',8)+1:]) for link in uris]
	title_and_link = [j for i in zip(title, uris) for j in i]
	title_and_link = "\n".join(title_and_link)
		
	# ____ load message template
	message_template = (read_template("message.txt") if len(title) == 1 else read_template("message_pluriel.txt"))
	
	# ____ create message
	msg = MIMEMultipart()
	message = message_template.substitute( TITLE= title_and_link )

	msg['From']="hal.bib@uvsq.fr"
	msg['To']="m@larri.eu"
	msg['Subject']="Pensez à partager votre article dans HAL "+title[0]	

	# ____ add body to msg
	msg.attach(MIMEText(message, 'plain'))
	s.send_message(msg)

	print(f"\n{mail}\n{len(mailNuris[mail])} article\nmail sent")
	del msg
	

	break

s.quit()



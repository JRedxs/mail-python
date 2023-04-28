import smtplib
import imaplib
from email.message import EmailMessage

# On demande les informations d'identification à l'utilisateur
mon_email = input("Entrez votre adresse e-mail : ")
mon_mot_de_passe = input("Entrez votre mot de passe : ")
serveur_imap = input("Entrez le serveur IMAP de votre boîte mail : ")

# Connexion au serveur IMAP
imap = imaplib.IMAP4_SSL(serveur_imap)

# Identification de l'utilisateur
imap.login(mon_email, mon_mot_de_passe)

# Sélection de la boîte mail
imap.select("inbox")

# Recherche des 10 premiers e-mails
result, data = imap.uid("search", None, "ALL")
email_uids = data[0].split()[-10:]
toSendSubject = ""

# Récupération des informations sur les 10 e-mails
for uid in reversed(email_uids):
    result, data = imap.uid("fetch", uid, "(RFC822)")
    raw_email = data[0][1]

    # Décodage de chaque e-mail
    email_message = raw_email.decode('ISO-8859-1')

    # Extraction du sujet de chaque e-mail
    subject = email_message.split("Subject: ", 1)[1].split("\r\n", 1)[0]
    if len(toSendSubject) == 0:
        toSendSubject = email_message.split("Subject: ", 1)[1].split("\r\n", 1)[0]

    # Impression du sujet de chaque e-mail
    print(subject)
    
send_choice = input("Souhaitez-vous envoyer un email avec le même sujet que le premier email ?\n")

if send_choice == 'oui':
    # Demande de l'adresse e-mail du destinataire
    to_email = input("Entrez l'adresse e-mail du destinataire : ")

    # Création du message
    msg = EmailMessage()
    msg['Subject'] = toSendSubject
    msg['From'] = mon_email
    msg['To'] = to_email
    
    # Envoi du message
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(mon_email, mon_mot_de_passe)
    smtp_server.send_message(msg)
    smtp_server.quit()

# Fermeture de la connexion IMAP
imap.close()
imap.logout()

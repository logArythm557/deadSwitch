import imaplib
import smtplib
import email
import time
import platform
import os

#constants
MAIL_DOMAIN = "@gmail.com"
FROM_EMAIL = {USERNAME} + MAIL_DOMAIN
FROM_PWD = {PASSWORD}
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993
KILLSWITCH = "shut it down"
STAYALIVE = "I'm Alive"
OS = platform.system()
PATH = ""



#mail reading function stolen from the internet
def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])


        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(latest_email_id, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print 'From : ' + email_from + '\n'
                    print 'Subject : ' + email_subject + '\n'
		    return email_subject

    except Exception, e:
        print str(e)


SUBJECT = read_email_from_gmail()
if SUBJECT == KILLSWITCH:
	if OS == "Linux":
		PATH = "~/.mozilla/firefox/"
		os.system("rm -r "+PATH+"*")
	elif OS == "Darwin":
		PATH = ["~/Library/Application Support/Firefox/Profiles/","~/Library/Mozilla/Firefox/Profiles/"]
		i = 0
		while i <= 1:
			print "Deleting Firefox profile at "+PATH[i]
			os.system("rm -r " +PATH[i]+"*")
			i = i+1
	elif OS == "Windows":
		PATH = '"%APPDATA%/Mozilla/"'
		print("Deleting firefox profile at "+PATH)
		os.system("rd /s /q "+PATH)
elif SUBJECT == STAYALIVE:
	print 'stay alive'
else:
	print "INVALID SUBJECT"


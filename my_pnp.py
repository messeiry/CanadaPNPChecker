# -*- coding: utf-8 -*-
import json, smtplib
#from pysnmp.hlapi.asyncore import *
from tornado.httpclient import HTTPClient




immigration_sites = json.dumps(
        {
        'novascotia': ['https://novascotiaimmigration.com/move-here/nova-scotia-demand-express-entry/','Category B is now closed'], 
        'saskatchewan': ['https://www.saskatchewan.ca/residents/moving-to-saskatchewan/immigrating-to-saskatchewan/saskatchewan-immigrant-nominee-program/applicants-international-skilled-workers/international-skilled-worker-saskatchewan-express-entry','Saskatchewan Express Entry sub-category is closed to applications at this time'],
        'newbrunswick': ['http://www.welcomenb.ca/content/wel-bien/en/immigrating/content/HowToImmigrate/NBProvincialNomineeProgram.html','Please note that New Brunswick is only accepting Expressions of Interest (EOIs) for the PNP Express Entry Labour Market Stream from individuals currently employed in New Brunswick and from potential applicants who demonstrate French as a first language']
        })

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body

def emailStatus(msg):
    msg = "From: PNP Tracking App\n\nSubject: Province PNP Status\n\n" + msg 
    gmail_user  = 'xyz@gmail.com';
    gmail_pwd   = 'xyzpassword'
    
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo() # optional, called by login()
    server_ssl.login(gmail_user, gmail_pwd)  

    server_ssl.sendmail(gmail_user, 'm.messeiry@gmail.com', msg)
    server_ssl.close()
    print 'successfully sent the mail'

novasCheck = "Category B is now closed"
sasCheck = "Saskatchewan Express Entry sub-category is closed to applications at this time"

if __name__ == '__main__':
    data = json.loads(immigration_sites)
    status = ""  
    
    for k,v in data.items():
        print "Checking The PNP Availability for %s" %k
        province = k
        provincePNPLink = str(v[0])
        provinceCheck = str(v[1])
  
        response = str(synchronous_fetch(provincePNPLink))
    
        if (response.find(provinceCheck) != -1):
            status += str(province)+" ==> Closed\n\n"
        else:
            status += province + " ==> Opened, Please check the following link \n\n"+provincePNPLink+ "\n\nGood Luck\n\n"
    
    emailStatus(status)



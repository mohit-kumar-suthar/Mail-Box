from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders 
import smtplib


def send_smtp(form_email,password,to_email,cc_email,bcc_email,subject,my_file,message):
    try:
        obj = MIMEMultipart()
        obj['From'] = form_email
        obj['To'] = to_email
        obj['cc']= cc_email
        obj['Subject'] = subject
        body = message
        obj.attach(MIMEText(body, 'plain'))

        if my_file:
            filename = my_file.name
            f= MIMEBase('application', 'octet-stream')
            f.set_payload( my_file.read() )
            encoders.encode_base64(f) 
            f.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            obj.attach(f) 

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(form_email,password)
        to=[to_email]+[cc_email]+[bcc_email]
        server.sendmail(obj['From'],to, obj.as_string())
        server.quit() 
    except:
        msg_error='Check your internet connection and less secure app access'
        return msg_error
    
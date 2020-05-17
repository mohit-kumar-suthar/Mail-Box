import poplib
from email.parser import Parser

def mail_login(user,password):
    server='pop.gmail.com'
    login= poplib.POP3_SSL(server,'995')
    login.user(user)
    login.pass_(password)

    return login


def print_info(msg):
    if(msg.is_multipart()):
        parts= msg.get_payload()
        for part in parts:
            return print_info(part)
        
    else:
        content_type=msg.get_content_type().lower()
        if content_type=='text/plain'or content_type=='text/html':
            content = msg.get_payload(decode=True)
            body=content.decode("utf-8") 
            return body
        
            
def receive_pop(user,password,num_msg):
    try:
        login=mail_login(user,password)        
        lines=login.retr(num_msg)[1]
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        email_from = msg.get('From')
        email_to = msg.get('To')
        email_cc = msg.get('Cc')
        email_subject = msg.get('Subject')
        body=print_info(msg)
        return email_from,email_to,email_cc,email_subject,body
    except:
        pass


def delete_msg(user,password,num_msg):
    try:
        login=mail_login(user,password)
        login.dele(num_msg)
        login.quit()
    except:
        pass


def num_mail(user,password):
    try:
        login=mail_login(user,password)
        return login.stat()[0]
    except:
        pass


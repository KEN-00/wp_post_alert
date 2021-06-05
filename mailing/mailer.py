import smtplib
from . import mail_content

def send(mailConfig, mailContentData, jinja2MailTemplateString):
    server = get_smtp_server(mailConfig)
    fromAddr = mailConfig['userName']
    recipients = mailConfig['recipients']
    subject = mailConfig['subject']

    emailMsg = mail_content.create_email_message(
        subject=subject, 
        fromAddr=fromAddr, 
        toAddrs=recipients, 
        mailContentData=mailContentData, 
        jinja2MailTemplateString=jinja2MailTemplateString
    )

    # TODO: send email
    # print(content)
    server.send_message(
        from_addr=fromAddr,
        to_addrs = recipients,
        msg=emailMsg
    )

    server.close()
    pass

def get_smtp_server(mailConfig):
    userName = mailConfig['userName']
    password = mailConfig['password']
    server = mailConfig['server']
    port = mailConfig['port']

    try:
        server = smtplib.SMTP_SSL(server, port)
        server.ehlo()
        server.login(userName, password)

    except Exception as e:
        print(e)
        exit()

    return server

def validate_mail_config(mailConfig):
    try:
        mailConfig['userName']
        mailConfig['password']
        mailConfig['server']
        mailConfig['port']
        mailConfig['recipients']
        mailConfig['subject']
    except KeyError as k:
        print ('mail config {} is missing, please set {} in config'.format(k, k))
        exit()
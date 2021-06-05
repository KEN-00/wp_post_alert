import smtplib
from . import mail_content

def send(mailConfig, mailContentData, jinja2MailTemplateString):
    server = get_smtp_server(mailConfig)
    recipients = mailConfig['recipients']

    template = mail_content.create_jinja2_mail_template(jinja2MailTemplateString)
    content = mail_content.create_mail_content(
        mailContentData,
        template
    )

    # TODO: send email
    # print(content)

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
    except KeyError as k:
        print ('mail config {} is missing, please set {} in config'.format(k, k))
        exit()
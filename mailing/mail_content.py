from jinja2 import Environment, BaseLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

MIME_SUBTYPE_ALTERNATIVE = 'alternative'
MIME_TEXT_SUBTYPE_HTML = 'html'

MIME_SUBJECT = 'Subject'
MIME_FROM = 'From'
MIME_TO = 'To'

SUBJECT_TEMPLATE = '{} {}'

def create_mail_html_content(mailContentData, jinja2MailTemplate):
    return jinja2MailTemplate.render(mailContentData=mailContentData)

def create_jinja2_mail_template(jinja2MailTemplateString):
    jinja2PostTemplate = Environment(loader=BaseLoader()).from_string(jinja2MailTemplateString)
    return jinja2PostTemplate

def create_email_message(subject, fromAddr, toAddrs, mailContentData, jinja2MailTemplateString):
    template = create_jinja2_mail_template(jinja2MailTemplateString)
    htmlContent = create_mail_html_content(
        mailContentData,
        template,
    )

    message = MIMEMultipart(MIME_SUBTYPE_ALTERNATIVE)

    ## message header
    message[MIME_SUBJECT] = create_subject(subject)
    message[MIME_FROM] = fromAddr
    message[MIME_TO] = ','.join(toAddrs)

    htmlMimeText = MIMEText(htmlContent, MIME_TEXT_SUBTYPE_HTML)
    message.attach(htmlMimeText)

    return message

def create_subject(subject):
    ## TODO generate subject
    dateStr = str(datetime.now())

    return SUBJECT_TEMPLATE.format(subject, dateStr)
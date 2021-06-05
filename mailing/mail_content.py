from jinja2 import Environment, BaseLoader

def create_mail_content(mailContentData, jinja2MailTemplate):
    return jinja2MailTemplate.render(mailContentData=mailContentData)

def create_jinja2_mail_template(jinja2MailTemplateString):
    jinja2PostTemplate = Environment(loader=BaseLoader()).from_string(jinja2MailTemplateString)
    return jinja2PostTemplate
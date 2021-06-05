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
import mysql.connector


def validate_wp_db_config(wpDbConfig):
    try:
        wpDbConfig['userName']
        wpDbConfig['password']
        wpDbConfig['host']
        wpDbConfig['port']
        wpDbConfig['database']
        wpDbConfig['targetCategories']
        wpDbConfig['targetPostStatuses']
    except KeyError as k:
        print ('MySQL DB config {} is missing, please set {} in config'.format(k, k))
        exit()

def get_wp_db(wpDbConfig):
    userName = wpDbConfig['userName']
    password = wpDbConfig['password']
    host = wpDbConfig['host']
    port = wpDbConfig['port']
    database = wpDbConfig['database']

    db = mysql.connector.connect(
        host=host,
        port=port,
        user=userName,
        password=password,
        database=database
    )

    return db
import os
import json
import io
from wp import wp_database, wp_post_query
from mailing import mailer

WP_DB_CONFIG_FILE_PATH_VAR_KEY = "WP_DB_CONFIG_FILE_PATH"
DEFAULT_WP_DB_CONFIG_FILE_PATH = "resource/wp_db_config.json"

MAIL_CONFIG_FILE_PATH_VAR_KEY = "MAIL_CONFIG_FILE_PATH"
DEFAULT_MAIL_CONFIG_FILE_PATH = "resource/mail_config.json"

JINJA2_MAIL_TEMPLATE_FILE_PATH_VAR_KEY ='JINJA2_MAIL_TEMPLATE_FILE_PATH'
DEFAULT_JINJA2_MAIL_TEMPLATE_FILE_PATH = 'resource/mail_template.jinja2'

# WordPress
def get_wp_db_config():
    wpDbConfigFilePath = get_wp_db_config_file_path()
    wpDbConfig = get_json_data(wpDbConfigFilePath)
    wp_database.validate_wp_db_config(wpDbConfig)
    return wpDbConfig

def get_wp_db_config_file_path():
    return get_env_config(WP_DB_CONFIG_FILE_PATH_VAR_KEY, DEFAULT_WP_DB_CONFIG_FILE_PATH)

# Mail
def get_mail_config():
    mailConfigFilePath = get_mail_config_file_path()
    mailConfig = get_json_data(mailConfigFilePath)
    mailer.validate_mail_config(mailConfig)
    return mailConfig

def get_mail_config_file_path():
    return get_env_config(MAIL_CONFIG_FILE_PATH_VAR_KEY, DEFAULT_MAIL_CONFIG_FILE_PATH)

# Jinja 2 Template
def get_jinja2_mail_template_string():
    filePath = get_jinja2_mail_template_file_path()
    with io.open(filePath, "r") as jinja2_file:
        return jinja2_file.read()

def get_jinja2_mail_template_file_path():
    return get_env_config(JINJA2_MAIL_TEMPLATE_FILE_PATH_VAR_KEY, DEFAULT_JINJA2_MAIL_TEMPLATE_FILE_PATH)

# Config
def get_env_config(key, default):
    return default if not os.environ.get(key) else os.environ.get(key)

def get_json_data(filename): 
    with io.open(filename, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data      

# Main
def main():
    wpDbConfig  = get_wp_db_config()
    mailConfig = get_mail_config()
    jinja2MailTemplateString = get_jinja2_mail_template_string()

    db = wp_database.get_wp_db(wpDbConfig)

    queryResult = wp_post_query.get_pending_posts(
        db=db, 
        targetCategories=wpDbConfig['targetCategories'], 
        targetPostStatuses=wpDbConfig['targetPostStatuses']
    )

    print(queryResult)

    mailer.send(mailConfig, queryResult, jinja2MailTemplateString)




if __name__ == '__main__':
    main()

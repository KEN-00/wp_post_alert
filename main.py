import os
import json
import io
from wp import wp_database, wp_post_query
from mailing import mailer

WP_DB_CONFIG_FILE_PATH_VAR_KEY = "WP_DB_CONFIG_FILE_PATH"
DEFAULT_WP_DB_CONFIG_FILE_PATH = "resource/wp_db_config.json"

MAIL_CONFIG_FILE_PATH_VAR_KEY = "MAIL_CONFIG_FILE_PATH"
DEFAULT_MAIL_CONFIG_FILE_PATH = "resource/mail_config.json"

def get_wp_db_config():
    wpDbConfigFilePath = get_wp_db_config_file_path()
    wpDbConfig = get_json_data(wpDbConfigFilePath)
    wp_database.validate_wp_db_config(wpDbConfig)
    return wpDbConfig

def get_wp_db_config_file_path():
    return get_env_config(WP_DB_CONFIG_FILE_PATH_VAR_KEY, DEFAULT_WP_DB_CONFIG_FILE_PATH)

def get_mail_config():
    mailConfigFilePath = get_mail_config_file_path()
    mailConfig = get_json_data(mailConfigFilePath)
    mailer.validate_mail_config(mailConfig)
    return mailConfig

def get_mail_config_file_path():
    return get_env_config(MAIL_CONFIG_FILE_PATH_VAR_KEY, DEFAULT_MAIL_CONFIG_FILE_PATH)

def get_env_config(key, default):
    return default if not os.environ.get(key) else os.environ.get(key)

def get_json_data(filename): 
    with io.open(filename, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data      

def main():
    wpDbConfig  = get_wp_db_config()
    mailConfig = get_mail_config()

    db = wp_database.get_wp_db(wpDbConfig)

    queryResult = wp_post_query.get_pending_posts(
        db=db, 
        targetCategories=wpDbConfig['targetCategories'], 
        targetPostStatuses=wpDbConfig['targetPostStatuses']
    )

    print(queryResult)

    for(post_title, post_date, post_id, post_url) in queryResult:
        pass


if __name__ == '__main__':
    main()

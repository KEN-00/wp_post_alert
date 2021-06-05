

# wp_post_alert
Python Alert for new WordPress posts created pending for administrator's approval

## Setup
To install dependencies:
`pip install -r requirements.txt`

  ### Environment Variables
A set of environment variables define the file paths of the configuration files required by the system:
| Environment Variable| Default Value   | 
| ------------ | ------------ | 
| WP_DB_CONFIG_FILE_PATH |  resource/wp_db_config.json |
| MAIL_CONFIG_FILE_PATH|  resource/mail_config.json |    
| JINJA2_MAIL_TEMPLATE_FILE_PATH|  resource/mail_template.jinja2 |  

### WordPress Database Config
`wp_db_config.json`:
`````json
{
    "userName": "bn_wordpress",
    "password": "password",
    "host": "127.0.0.1",
    "port": "3306",
    "database": "bitnami_wordpress",
    "targetCategories":[1],
    "targetPostStatuses":["pending"]	
}
`````

| Key| Value   | 
| ------------ | ------------ | 
| userName|  MySQL user name|
| password|  MySQL password |    
| host|  MySQL host |  
| port|  MySQL port |  
| database|  MySQL database name |  
| targetCategories|  IDs of WordPress post categories to be quried (list of int) |  
| targetPostStatuses|  [statuses](https://wordpress.org/support/article/post-status/) of WordPress posts to be quried (list of string) |  

Default post_status values in WordPress database [wp_posts](https://codex.wordpress.org/Database_Description#Table:_wp_posts) table: `publish`, `future`, `draft`, `pending`, `private`.
### Mail Config
`mail_config.json`:
`````json
{
    "server":"smtp.gmail.com",
    "port":465,
    "userName":"",
    "password":"",
    "recipients":[]
}
`````
| Key| Value   | 
| ------------ | ------------ | 
| server|  mail server name|
| port|  mail server port|
| userName|  email address of mail account |
| password|  email password of mail account|
| recipients|  target email recipients (list of email addresses)|

### Jinja2 Template
Create a Jinja2 template file `mail_template.jinja2` for creating WordPress post with content, which can be string template or HTML template.

Sample `mail_template.jinja2`:
```html
{% macro renderValue(value) -%}
    {{ value|default('') }}
{%- endmacro %}

{% if mailContentData %}
    <div class="table-container">
        <table class="table">
            <tr>
                <td>Post ID</td>
                <td>Title</td>
                <td>Date</td>
                <td>Post URL</td>
            </tr>

        {% for data in mailContentData %}
            <tr>
                <td>{{ renderValue(data.post_id) }}</td>
                <td>{{ renderValue(data.post_title) }}</td>
                <td>{{ renderValue(data.post_date) }}</td>
                <td>
                    {% if data.post_url %}
                        <a href="{{ data.post_url }}">{{ data.post_url }}</a>
                    {% endif %}
                </td>
            </tr>
        {% endfor %}
        </table>
    </div>
{% else %}
    no data
{% endif %}
```
Jinja2 will render the HTML mail content with the template and the database query results.

For details, please read [Jinja official documentaion](https://jinja.palletsprojects.com/en/3.0.x/).

### Execution
`python ./main.py`

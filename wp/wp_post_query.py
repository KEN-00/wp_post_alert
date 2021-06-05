COMMA = ','
SINGLE_QUOTE = '\''

PENDING_POSTS_QUERY_TEMPLATE = """
    SELECT 
    wpp.post_title AS post_title,
    wpp.post_date AS post_date,
    wpp.ID AS post_id,
    CONCAT(
        wopts.option_value, 
        'wp-admin/post.php?post=', 
        wpp.ID, 
        '&action=edit'
    ) AS post_url

    FROM
        wp_posts as wpp
        
        JOIN wp_term_relationships AS wtr
            ON wpp.ID = wtr.object_id
        
        JOIN wp_term_taxonomy AS wtx
            ON (
                wtr.term_taxonomy_id = wtx.term_taxonomy_id
                AND wtx.taxonomy = 'category'
            )
        JOIN wp_terms as wt
            ON wt.term_id = wtx.term_id
        JOIN  wp_options as wopts
            ON (
                1 = 1
                AND wopts.option_name = 'siteurl'
            )
            
    WHERE wt.term_id IN ({})
    AND wpp.post_status IN ({})
"""

def get_pending_posts(db, targetCategories, targetPostStatuses):
    #concat target categories into comma separated int list of category IDs
    targetCategoriesListStr =  COMMA.join(str(category) for category in targetCategories)
    
    #concat target statuses into comma separated string list of statuses
    targetPostStatusesListStr = COMMA.join(SINGLE_QUOTE + str(status) + SINGLE_QUOTE for status in targetPostStatuses)
    
    query = PENDING_POSTS_QUERY_TEMPLATE.format(targetCategoriesListStr, targetPostStatusesListStr)

    cursor = db.cursor(dictionary=True)
    cursor.execute(query)

    return cursor.fetchall()
    
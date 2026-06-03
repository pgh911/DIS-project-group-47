from database import db_connection

class CategoryType:
    def __init__(self, type_id, type_name):
        self.type_id = type_id
        self.type_name = type_name

class Category:
    def __init__(self, cid, category_name, category_type, created, lid):
        self.cid = cid
        self.category_name = category_name
        self.category_type = category_type
        self.created = created
        self.lid = lid


def find_category_type(type_id, category_type_list:list[CategoryType]):
    for CT in category_type_list:
        if CT.type_id == type_id:
            return CT.type_name
    return type_id
    

def list_category_types():
    conn = db_connection()

    db_category_types = conn.execute(
        "SELECT * FROM category_types",
    ).fetchall()
    
    conn.close()

    categories = []
    for category_type in db_category_types:
        categories.append(CategoryType(
            category_type['type_id'], category_type['type_name']
        ))
    return categories


def list_categories(lid):
    conn = db_connection()
    db_categories:list[Category] = conn.execute(
        "SELECT * FROM categories WHERE lid = ?",
        (lid,)
    ).fetchall()

    conn.close()

    category_types = list_category_types()

    categories = []
    for category in db_categories:
        category_type = find_category_type(category['type_id'], category_types)

        categories.append(Category(
            cid=category['cid'], 
            lid=category['lid'], 
            category_name=category['category_name'],
            category_type=category_type, 
            created=category['created']
        ))
    return categories

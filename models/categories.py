from database import db_connection


class CategoryType:
    def __init__(self, type_id: int, type_name: str) -> None:
        self.type_id: int = type_id
        self.type_name: str = type_name


class Category:
    def __init__(self, cid: int, category_name: str, category_type: str | None, created: str, lid: int, type_id: int) -> None:
        self.cid: int = cid
        self.lid: int = lid
        self.created: str = created
        self.type_id: int = type_id
        self.category_name: str = category_name
        self.category_type: str | None = category_type


def find_category_type(type_id: int) -> str | None:
    conn = db_connection()
    db_type = conn.execute(
        "SELECT type_name FROM category_types WHERE type_id = ?",
        (type_id,)
    ).fetchone()
    conn.close()

    if db_type:
        return db_type['type_name']
    return None


def list_category_types() -> list[CategoryType]:
    conn = db_connection()
    db_category_types = conn.execute(
        "SELECT * FROM category_types"
    ).fetchall()
    conn.close()

    category_types: list[CategoryType] = []
    for db_ct in db_category_types:
        category_types.append(CategoryType(
            type_id=db_ct['type_id'],
            type_name=db_ct['type_name']
        ))
    return category_types


def list_categories(lid: int) -> list[Category]:
    conn = db_connection()
    db_categories = conn.execute(
        "SELECT * FROM categories WHERE lid = ? ORDER BY cid",
        (lid,)
    ).fetchall()
    conn.close()

    categories: list[Category] = []
    for db_category in db_categories:
        category_type = find_category_type(db_category['type_id'])

        categories.append(Category(
            cid=db_category['cid'],
            category_name=db_category['category_name'],
            category_type=category_type,
            type_id=db_category['type_id'],
            created=db_category['created'],
            lid=db_category['lid']
        ))
    return categories


def get_category(cid: int) -> Category | None:
    conn = db_connection()
    db_category = conn.execute(
        "SELECT * FROM categories WHERE cid = ?",
        (cid,)
    ).fetchone()
    conn.close()

    if db_category:
        category_type = find_category_type(db_category['type_id'])

        return Category(
            cid=db_category['cid'],
            category_name=db_category['category_name'],
            category_type=category_type,
            created=db_category['created'],
            type_id=db_category['type_id'],
            lid=db_category['lid']
        )
    return None


def insert_category(category_name: str, type_id: int, lid: int) -> int | None:
    conn = db_connection()
    cur = conn.execute(
        "INSERT OR IGNORE INTO categories (category_name, type_id, lid) VALUES (?, ?, ?)",
        (category_name, type_id, lid)
    )
    conn.commit()
    category_id = cur.lastrowid
    conn.close()
    return category_id


def update_category(cid: int, category_name: str, type_id: int) -> None:
    conn = db_connection()
    conn.execute(
        "UPDATE categories SET category_name = ?, type_id = ? WHERE cid = ?",
        (category_name, type_id, cid)
    )
    conn.commit()
    conn.close()


def delete_category(cid: int) -> None:
    conn = db_connection()
    conn.execute("DELETE FROM categories WHERE cid = ?", (cid,))
    conn.commit()
    conn.close()

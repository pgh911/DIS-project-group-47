CREATE TRIGGER create_default_categories
AFTER INSERT ON ledgers
BEGIN
    INSERT INTO categories (category_name, type_id, lid)
    VALUES ('Income', 3, NEW.lid);

    INSERT INTO categories (category_name, type_id, lid)
    VALUES ('Food', 1, NEW.lid);

    INSERT INTO categories (category_name, type_id, lid)
    VALUES ('Rent', 1, NEW.lid);

    
    INSERT INTO categories (category_name, type_id, lid)
    VALUES ('Stocks', 2, NEW.lid);
END;
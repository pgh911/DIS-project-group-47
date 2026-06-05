CREATE TRIGGER create_default_categories AFTER INSERT ON ledgers BEGIN
INSERT INTO
    categories (category_name, type_id, lid)
VALUES
    ('Income', 3, NEW.lid);

INSERT INTO
    categories (category_name, type_id, lid)
VALUES
    ('Food', 1, NEW.lid);

INSERT INTO
    categories (category_name, type_id, lid)
VALUES
    ('Rent', 1, NEW.lid);

INSERT INTO
    categories (category_name, type_id, lid)
VALUES
    ('Stocks', 2, NEW.lid);

END;

-- when a year is added, budget entries are added in the ledger, for each 
-- year, month, category
CREATE TRIGGER create_budget_entries_on_year_added AFTER INSERT ON ledger_years BEGIN
INSERT INTO
    budget_entries (year_id, amount, cid, lid, type_id, MONTH)
SELECT
    NEW.year_id,
    1, -- amount
    c.cid,
    c.lid,
    c.type_id,
    m.month
FROM
    categories c
    CROSS JOIN (
        SELECT 1 AS month UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
        SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
        SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL
        SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12
    ) m
WHERE
    c.lid = NEW.lid;
END;

-- when a category is added, budget entries are added in the ledger, for each 
-- year, month
CREATE TRIGGER create_budget_entries_on_category_added
AFTER INSERT ON categories
BEGIN
INSERT INTO budget_entries (
    year_id,
    amount,
    cid,
    lid,
    type_id,
    month
)
SELECT
    y.year_id,
    1,
    NEW.cid,
    NEW.lid,
    NEW.type_id,
    m.month
FROM ledger_years y
CROSS JOIN (
    SELECT 1 AS month UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
    SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL
    SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12
) m
WHERE y.lid = NEW.lid;
END;
DROP VIEW IF EXISTS posting_details;

DROP VIEW IF EXISTS posting_sum;

DROP VIEW IF EXISTS categories_totals;
DROP VIEW IF EXISTS category_details;

DROP VIEW IF EXISTS budget_details;

CREATE VIEW
    posting_details AS
SELECT
    p.pid,
    p.lid,
    l.ledger_name,
    p.cid,
    c.category_name,
    ct.type_name,
    p.amount,
    p.description,
    p.posting_date,
    CAST(strftime('%m', p.posting_date) AS INTEGER) AS posting_month,
    CAST(strftime('%Y', p.posting_date) AS INTEGER) AS posting_year
FROM
    postings p
    JOIN categories c ON p.cid = c.cid
    JOIN category_types ct ON c.type_id = ct.type_id
    JOIN ledgers l ON p.lid = l.lid;

CREATE VIEW category_details AS 
SELECT 
    ca.*,
    ct.type_name as type_name
FROM categories ca
INNER JOIN category_types ct
ON ca.type_id = ct.type_id;


CREATE VIEW
    posting_sum AS
SELECT
    ca.lid,
    ca.category_name,
    ca.type_name,
    pd.posting_month,
    pd.posting_year,
    COALESCE(
        CASE
            WHEN ca.type_name = 'expense' THEN SUM(ABS(pd.amount) * -1)
            WHEN ca.type_name = 'saving' THEN SUM(ABS(pd.amount))
            WHEN ca.type_name = 'income' THEN SUM(ABS(pd.amount))
            ELSE SUM(pd.amount)
        END,
        0
    ) AS total_amount
FROM
    category_details ca
    LEFT JOIN posting_details pd ON pd.cid = ca.cid
GROUP BY
    ca.lid,
    ca.category_name,
    ca.type_name,
    pd.posting_month,
    pd.posting_year;


CREATE VIEW budget_details AS
SELECT
    be.*,
    CASE
        WHEN cd.type_name = 'expense' THEN ABS(be.amount) * -1
        WHEN cd.type_name = 'saving' THEN ABS(be.amount)
        WHEN cd.type_name = 'income' THEN ABS(be.amount)
        ELSE be.amount
    END AS total_amount,
    cd.type_name,
    cd.category_name,
    ly.ledger_year
FROM budget_entries be
LEFT JOIN ledger_years ly
    ON be.year_id = ly.year_id
LEFT JOIN category_details cd
    ON be.cid = cd.cid;

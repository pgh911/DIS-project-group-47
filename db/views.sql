DROP VIEW IF EXISTS posting_details;
DROP VIEW IF EXISTS posting_sum;
DROP VIEW IF EXISTS categories_totals;


CREATE VIEW 
    categories_totals AS
SELECT
    lid, sum(amount) as total
FROM postings
GROUP BY lid;

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
    p.created
FROM
    postings p
    JOIN categories c ON p.cid = c.cid
    JOIN category_types ct ON c.type_id = ct.type_id
    JOIN ledgers l ON p.lid = l.lid;

CREATE VIEW
    posting_sum AS 
SELECT 
    CASE
        WHEN pd.type_name = 'expense' THEN SUM(ABS(pd.amount) * -1)
        WHEN pd.type_name = 'saving' THEN SUM(ABS(pd.amount))
        WHEN pd.type_name = 'expense' THEN SUM(ABS(pd.amount))
    END AS total_amount,
    pd.lid
FROM posting_details pd
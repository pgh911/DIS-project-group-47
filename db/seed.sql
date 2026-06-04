INSERT INTO
    users (id, username, password)
VALUES
    (1, "user", "password");

INSERT INTO
    ledgers (ledger_name, user_id)
VALUES
    ('Bank Account', 1),
    ('Cash Wallet', 1);

INSERT INTO
    category_types (type_id, type_name)
VALUES
    (1, 'expense'),
    (2, 'saving'),
    (3, 'income');

INSERT INTO
    categories (category_name, type_id, lid)
VALUES
    ('Rent', 1, 1),
    ('Groceries', 1, 1),
    ('Transport', 1, 1),
    ('Entertainment', 1, 1),
    ('Stocks', 2, 1),
    ('Vacation Fund', 2, 1),
    ('Salary', 3, 1),
    ('Sidegigs', 3, 1),
    ('Investment Returns', 3, 1),
    ('Rent', 1, 2),
    ('Groceries', 1, 2),
    ('Transport', 1, 2),
    ('Entertainment', 1, 2),
    ('Stocks', 2, 2),
    ('Vacation Fund', 2, 2),
    ('Salary', 3, 2),
    ('Sidegigs', 3, 2),
    ('Investment Returns', 3, 2);

INSERT INTO
    postings (lid, cid, amount, description)
VALUES
    (1, 7, 3000.00, 'Monthly salary'),
    (1, 1, -1200.00, 'Rent payment'),
    (1, 2, -250.00, 'Groceries'),
    (2, 3, -40.00, 'Bus ticket'),
    (2, 8, 500.00, 'Freelance gig');


INSERT INTO 
    ledger_years (year_id, ledger_year, lid)
VALUES 
    (1, 2025, 1),
    (2, 2026, 1),
    (3, 2025, 2),
    (4, 2026, 2);

INSERT INTO 
    budget_entries (bid, year_id, amount, cid, lid, type_id)
VALUES 
    (1, 1, 500, 1, 1, 1),
    (2, 1, 1500.25, 1, 1, 2);
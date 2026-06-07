INSERT INTO
    users (id, username, password)
VALUES
    (1, "user", "password");

INSERT INTO
    ledgers (ledger_name, user_id)
VALUES
    ('Bank Account', 1),
    ('Cash Wallet', 1),
    ('Tokyo trip', 1),

INSERT INTO
    category_types (type_id, type_name)
VALUES
    (1, 'expense'),
    (2, 'saving'),
    (3, 'income');

INSERT OR IGNORE INTO
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
    postings (lid, cid, amount, description, posting_date)
VALUES
    (1, 7, 3000.00, 'Monthly salary', "2026-06-04"),
    (1, 1, -1200.00, 'Rent payment', "2026-06-04"),
    (1, 2, -250.00, 'Groceries', "2026-06-04"),
    (2, 3, -40.00, 'Bus ticket', "2026-06-04"),
    (2, 8, 500.00, 'Freelance gig', "2026-06-04"),
    (1, 7, 3000.00, 'Monthly salary', "2026-07-04"),
    (1, 1, -1200.00, 'Rent payment', "2026-07-04"),
    (1, 2, -250.00, 'Groceries', "2026-07-04"),
    (2, 3, -40.00, 'Bus ticket', "2026-07-04"),
    (2, 8, 500.00, 'Freelance gig', "2026-07-04");

INSERT INTO 
    ledger_years (year_id, ledger_year, lid)
VALUES 
    (1, 2025, 1),
    (4, 2026, 2);

-- Categories for ledger 3 (Tokyo trip)
INSERT OR IGNORE INTO
    categories (category_name, type_id, lid)
VALUES
    ('Accommodation', 1, 3),
    ('Dining', 1, 3),
    ('Transport', 1, 3),
    ('Sightseeing', 1, 3),
    ('Shopping', 1, 3),
    ('Travel Budget', 2, 3),
    ('Travel Allowance', 3, 3);


-- Categories for ledger 5 (Home Budget)
INSERT OR IGNORE INTO
    categories (category_name, type_id, lid)
VALUES
    ('Rent', 1, 5),
    ('Groceries', 1, 5),
    ('Utilities', 1, 5),
    ('Entertainment', 1, 5),
    ('Emergency Fund', 2, 5),
    ('Salary', 3, 5),
    ('Sidegigs', 3, 5);

-- Categories for ledger 6 (Travel Fund)
INSERT OR IGNORE INTO
    categories (category_name, type_id, lid)
VALUES
    ('Flights', 1, 6),
    ('Hotels', 1, 6),
    ('Activities', 1, 6),
    ('Travel Savings', 2, 6),
    ('Travel Allowance', 3, 6);

-- Categories for ledger 7 (Monthly Budget)
INSERT OR IGNORE INTO
    categories (category_name, type_id, lid)
VALUES
    ('Rent', 1, 7),
    ('Groceries', 1, 7),
    ('Transport', 1, 7),
    ('Subscriptions', 1, 7),
    ('Savings', 2, 7),
    ('Salary', 3, 7);

-- Postings for ledger 3 (Tokyo trip)
INSERT INTO
    postings (lid, cid, amount, description, posting_date)
VALUES
    (3, 20, 8000.00, 'Travel allowance saved up', '2026-03-01'),
    (3, 19, -1200.00, 'Flight to Tokyo', '2026-04-10'),
    (3, 18, -900.00, 'Hotel Shinjuku 6 nights', '2026-04-11'),
    (3, 21, -180.00, 'Shinkansen pass', '2026-04-12'),
    (3, 17, -320.00, 'Ramen, sushi, izakaya', '2026-04-13'),
    (3, 22, -250.00, 'Akihabara shopping', '2026-04-14'),
    (3, 16, -60.00, 'TeamLab Planets tickets', '2026-04-15');

-- Postings for ledger 5 (Home Budget, June + July)
INSERT INTO
    postings (lid, cid, amount, description, posting_date)
VALUES
    (5, 29, 3400.00, 'Monthly salary', '2026-06-01'),
    (5, 24, -1100.00, 'Rent payment', '2026-06-02'),
    (5, 25, -310.00, 'Weekly groceries', '2026-06-05'),
    (5, 26, -85.00, 'Electricity bill', '2026-06-06'),
    (5, 27, -60.00, 'Cinema and dinner', '2026-06-07'),
    (5, 28, 200.00, 'Emergency fund top-up', '2026-06-07'),
    (5, 29, 3400.00, 'Monthly salary', '2026-07-01'),
    (5, 24, -1100.00, 'Rent payment', '2026-07-02'),
    (5, 25, -280.00, 'Weekly groceries', '2026-07-04'),
    (5, 26, -90.00, 'Internet + electricity', '2026-07-05');

-- Postings for ledger 7 (Monthly Budget, June)
INSERT INTO
    postings (lid, cid, amount, description, posting_date)
VALUES
    (7, 41, 2800.00, 'Monthly salary', '2026-06-01'),
    (7, 35, -950.00, 'Rent payment', '2026-06-01'),
    (7, 36, -200.00, 'Groceries run', '2026-06-03'),
    (7, 37, -55.00, 'Monthly transit card', '2026-06-03'),
    (7, 38, -45.00, 'Streaming subscriptions', '2026-06-04'),
    (7, 39, 150.00, 'Savings transfer', '2026-06-05');

-- Ledger years for new ledgers
INSERT INTO
    ledger_years (year_id, ledger_year, lid)
VALUES
    (5, 2026, 3),
    (6, 2026, 4),
    (7, 2025, 5),
    (8, 2026, 5),
    (9, 2026, 6),
    (10, 2026, 7);
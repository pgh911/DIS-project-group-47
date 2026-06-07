INSERT INTO
    users (id, username, password)
VALUES
    (1, 'user', 'password');

INSERT INTO
    ledgers (ledger_name, user_id)
VALUES
    ('Bank Account', 1),
    ('Cash Wallet', 1),
    ('Tokyo Trip', 1);

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
    ('Investment Returns', 3, 2),
    -- Tokyo Trip categories (lid = 3)
    ('Flights', 1, 3),
    ('Accommodation', 1, 3),
    ('Transport', 1, 3),
    ('Food & Dining', 1, 3),
    ('Activities', 1, 3),
    ('Shopping', 1, 3),
    ('Travel Fund', 2, 3);

INSERT INTO
    postings (lid, cid, amount, description, posting_date)
VALUES
    (1, 7, 3000.00, 'Monthly salary', '2026-06-04'),
    (1, 1, -1200.00, 'Rent payment', '2026-06-04'),
    (1, 2, -250.00, 'Groceries', '2026-06-04'),
    (2, 3, -40.00, 'Bus ticket', '2026-06-04'),
    (2, 8, 500.00, 'Freelance gig', '2026-06-04'),
    
    (1, 7, 3000.00, 'Monthly salary', '2026-07-04'),
    (1, 1, -1200.00, 'Rent payment', '2026-07-04'),
    (1, 2, -250.00, 'Groceries', '2026-07-04'),
    
    (2, 3, -40.00, 'Bus ticket', '2026-07-04'),
    (2, 8, 500.00, 'Freelance gig', '2026-07-04'),
    
    (3, 20, -850.00, 'Return flights CPH-NRT', '2026-09-01'),
    (3, 26,  850.00, 'Travel fund contribution', '2026-08-01'),
    (3, 21, -120.00, 'Hotel Shinjuku night 1-3', '2026-09-10'),
    (3, 21, -95.00,  'Hostel Kyoto night 4-6', '2026-09-13'),
    (3, 22, -30.00,  'Suica card top-up', '2026-09-10'),
    (3, 22, -15.00,  'Shinkansen Kyoto-Tokyo', '2026-09-16'),
    (3, 23, -18.00,  'Ramen dinner Shinjuku', '2026-09-10'),
    (3, 23, -12.00,  'Sushi lunch Tsukiji', '2026-09-11'),
    (3, 23, -9.00,   'Convenience store meals', '2026-09-12'),
    (3, 24, -15.00,  'TeamLab Planets entry', '2026-09-11'),
    (3, 24, -8.00,   'Senso-ji area tour', '2026-09-12'),
    (3, 25, -60.00,  'Clothing Harajuku', '2026-09-14'),
    (3, 25, -40.00,  'Souvenirs Kyoto', '2026-09-15');

INSERT INTO
    ledger_years (year_id, ledger_year, lid)
VALUES
    (1, 2025, 1),
    (4, 2026, 2),
    (5, 2026, 3);
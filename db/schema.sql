DROP TABLE IF EXISTS postings;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS category_types;
DROP TABLE IF EXISTS ledgers;
DROP TABLE IF EXISTS users;

CREATE TABLE
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL, 
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    );

INSERT INTO
    users (id, username, password)
VALUES
    (1, "user", "password");

CREATE TABLE ledgers (
    lid INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ledger_name TEXT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO
    ledgers (ledger_name, user_id)
VALUES
    ('Bank Account', 1),
    ('Cash Wallet', 1);

CREATE TABLE
    category_types (
        type_id INTEGER PRIMARY KEY,
        type_name TEXT UNIQUE NOT NULL
    );

INSERT INTO
    category_types (type_id, type_name)
VALUES
    (1, 'expense'),
    (2, 'saving'),
    (3, 'income');

CREATE TABLE
    categories (
        cid INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL,
        type_id INTEGER NOT NULL,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (type_id) REFERENCES category_types (type_id)
    );

INSERT INTO
    categories (category_name, type_id)
VALUES
    ('Rent', 1),
    ('Groceries', 1),
    ('Transport', 1),
    ('Entertainment', 1),
    ('Emergency Fund', 2),
    ('Vacation Fund', 2),
    ('Salary', 3),
    ('Freelance', 3),
    ('Investment Returns', 3);

CREATE TABLE
    postings (
        pid INTEGER PRIMARY KEY AUTOINCREMENT,
        lid INTEGER NOT NULL,
        cid INTEGER NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (lid) REFERENCES ledgers (lid) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (cid) REFERENCES categories (cid) ON DELETE CASCADE ON UPDATE CASCADE
    );

INSERT INTO
    postings (lid, cid, amount, description)
VALUES
    (1, 7, 3000.00, 'Monthly salary'),
    (1, 1, -1200.00, 'Rent payment'),
    (1, 2, -250.00, 'Groceries'),
    (2, 3, -40.00, 'Bus ticket'),
    (2, 8, 500.00, 'Freelance gig');
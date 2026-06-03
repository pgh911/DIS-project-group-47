DROP TABLE IF EXISTS ledgers;
DROP TABLE IF EXISTS postings;
DROP TABLE IF EXISTS category_types;
DROP TABLE IF EXISTS categories;

CREATE TABLE ledgers (
    lid INTEGER PRIMARY KEY AUTOINCREMENT,
    ledger_name TEXT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE category_types (
    type_id INTEGER PRIMARY KEY,
    type_name TEXT UNIQUE NOT NULL
);

INSERT INTO category_types (type_name) VALUES
('expense'), ('saving'), ('income');

CREATE TABLE categories (
    cid INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL,
    type_id INTEGER NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (type_id) REFERENCES category_types(type_id)
);

CREATE TABLE postings (
    pid INTEGER PRIMARY KEY AUTOINCREMENT,
    lid INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (lid) REFERENCES ledgers(lid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    
    FOREIGN KEY (cid) REFERENCES categories(cid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT OR IGNORE INTO ledgers (ledger_name)
VALUES ('Bank Account');

INSERT INTO category_types (type_name) VALUES
('expense'),
('saving'),
('income');

INSERT INTO categories (category_name, type_id) VALUES
('Rent', 1),
('Groceries', 1),
('Transport', 1),
('Emergency Fund', 2),
('Vacation Fund', 2),
('Salary', 3),
('Freelance', 3),
('Investment Returns', 3);

INSERT OR IGNORE INTO categories (category_name)
VALUES ("Rent")

INSERT INTO postings (lid, amount, description)
VALUES (1, 100.00, 'Gig payment');

INSERT INTO postings (lid, amount, description)
VALUES (1, -20.00, 'Equipment rental');

INSERT INTO postings (lid, amount, description)
VALUES (2, 500.00, 'Deposit');
DROP TABLE IF EXISTS budget_entries;

DROP TABLE IF EXISTS ledger_years;

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

CREATE TABLE
    ledgers (
        lid INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        ledger_name TEXT NOT NULL,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
    );

CREATE TABLE
    category_types (
        type_id INTEGER PRIMARY KEY,
        type_name TEXT UNIQUE NOT NULL
    );

CREATE TABLE
    categories (
        cid INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL,
        type_id INTEGER NOT NULL,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        lid INTEGER NOT NULL,
        FOREIGN KEY (type_id) REFERENCES category_types (type_id),
        FOREIGN KEY (lid) REFERENCES ledgers (lid) ON DELETE CASCADE,
        UNIQUE (lid, category_name)
    );

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

CREATE TABLE
    ledger_years (
        year_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ledger_year INTEGER NOT NULL,
        lid INTEGER NOT NULL,
        FOREIGN KEY (lid) REFERENCES ledgers (lid) ON DELETE CASCADE ON UPDATE CASCADE
    );

CREATE TABLE
    budget_entries (
        bid INTEGER PRIMARY KEY AUTOINCREMENT,
        year_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        cid INTEGER NOT NULL,
        lid INTEGER NOT NULL,
        type_id INTEGER NOT NULL,
        FOREIGN KEY (lid) REFERENCES ledgers (lid) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (type_id) REFERENCES category_types (type_id),
        FOREIGN KEY (cid) REFERENCES categories (cid) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (year_id) REFERENCES ledger_years (year_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
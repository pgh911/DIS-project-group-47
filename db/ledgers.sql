DROP TABLE IF EXISTS ledgers;

CREATE TABLE ledgers (
    lid INTEGER PRIMARY KEY AUTOINCREMENT,
    ledger_name TEXT UNIQUE NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO ledgers (ledger_name)
VALUES ('Band ledger');

INSERT OR IGNORE INTO ledgers (ledger_name)
VALUES ('Bank Account');
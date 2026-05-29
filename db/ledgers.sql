DROP TABLE IF EXISTS Ledgers CASCADE;

CREATE TABLE
	IF NOT EXISTS Ledgers (
		lid serial NOT NULL PRIMARY KEY,
		ledger_name VARCHAR(50) UNIQUE,
		created INT
	);

INSERT
OR IGNORE INTO ledgers (ledger_name)
VALUES
	('Band ledger');

INSERT
OR IGNORE INTO ledgers (ledger_name)
VALUES
	('Bank Account');
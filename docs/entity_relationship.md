# ER Diagram using mermaid (https://github.com/mermaid-js/mermaid)

```mermaid
erDiagram
    users {
        INTEGER id PK
        TEXT username UK
        TEXT password
        DATETIME created
    }

    ledgers {
        INTEGER lid PK
        INTEGER user_id FK
        TEXT ledger_name
        DATETIME created
    }

    category_types {
        INTEGER type_id PK
        TEXT type_name UK
    }

    categories {
        INTEGER cid PK
        TEXT category_name
        INTEGER type_id FK
        INTEGER lid FK
        DATETIME created
    }

    postings {
        INTEGER pid PK
        INTEGER lid FK
        INTEGER cid FK
        REAL amount
        TEXT description
        DATETIME created
        DATE posting_date
    }

    ledger_years {
        INTEGER year_id PK
        INTEGER ledger_year
        INTEGER lid FK
    }

    budget_entries {
        INTEGER bid PK
        INTEGER year_id FK
        INTEGER cid FK
        INTEGER lid FK
        INTEGER type_id FK
        REAL amount
        INTEGER month
    }

    users ||--o{ ledgers : "user_id"
    ledgers ||--o{ categories : "lid"
    ledgers ||--o{ postings : "lid"
    ledgers ||--o{ ledger_years : "lid"
    ledgers ||--o{ budget_entries : "lid"
    category_types ||--o{ categories : "type_id"
    category_types ||--o{ budget_entries : "type_id"
    categories ||--o{ postings : "cid"
    categories ||--o{ budget_entries : "cid"
    ledger_years ||--o{ budget_entries : "year_id"
```

## Legend
PK = Primary Key
FK = Foreign Key
UK = Unique Key
Lines = relationships, all of relationsship type one to many. A straight end closest to the parent entity indicates an 'exactly one' relationsship. The forked end with a circle closest to the child entity indicates a 'zero or many' relationsship.

import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash
from config import Config

try:
    from challenge_seed import FLAG as SEED_FLAG
except ImportError:
    SEED_FLAG = Config.FLAG


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS restricted_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    classification TEXT NOT NULL DEFAULT 'RESTRICTED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

ORDINARY_RECORDS = [
    (1, "Network Diagram - HQ", "Internal network topology showing core switches, firewalls, and DMZ segmentation. VLANs: 10-mgmt, 20-servers, 30-users, 40-guest.", "Infrastructure"),
    (2, "Server Inventory Q3", "Asset list: web-01 (10.0.20.10), db-01 (10.0.20.20), app-01 (10.0.20.30), backup-01 (10.0.20.40). All running Ubuntu 22.04 LTS.", "Inventory"),
    (3, "Firewall Rule Audit", "Reviewed ingress rules: 80/443 from WAF, 22 from mgmt VLAN only, 3306 from app VLAN only. Removed legacy rule allowing 1433 from anywhere.", "Security"),
    (4, "VPN Access Policy", "Remote access via OpenVPN with MFA. Certificate rotation every 90 days. Split tunneling disabled. Client config pushed via MDM.", "Policy"),
    (5, "Incident Runbook - Phishing", "Step 1: Isolate endpoint. Step 2: Collect headers and payload. Step 3: Block sender domain at gateway. Step 4: Reset credentials. Step 5: User refresher.", "Operations"),
    (6, "Database Backup Schedule", "Full backup daily 02:00 UTC. Incremental every 4 hours. Retention: 30 days full, 90 days incremental. Test restore monthly.", "Operations"),
    (7, "Certificate Inventory", "Wildcard *.corp.example.com expires 2025-06-15. Internal CA root expires 2028-01-20. Monitoring via cert-exporter + Prometheus.", "Infrastructure"),
    (8, "Access Review Q3", "Quarterly review completed. 3 stale accounts disabled. 2 contractor accounts expired. 1 privilege escalation request approved with justification.", "Security"),
]

RESTRICTED_RECORD = (1, "Legacy System Credentials", SEED_FLAG, "TOP SECRET")


def get_db_path():
    return Config.DATABASE_PATH


def init_db(db_path=None, flag=None):
    if db_path is None:
        db_path = get_db_path()
    if flag is None:
        flag = SEED_FLAG

    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA_SQL)

    # Insert user
    pw_hash = generate_password_hash("trainee123")
    conn.execute(
        "INSERT OR IGNORE INTO users (id, username, password_hash) VALUES (1, 'trainee', ?)",
        (pw_hash,)
    )

    # Insert ordinary records
    for rec_id, title, content, category in ORDINARY_RECORDS:
        conn.execute(
            "INSERT OR IGNORE INTO records (id, title, content, category) VALUES (?, ?, ?, ?)",
            (rec_id, title, content, category)
        )

    # Insert restricted record
    restricted_title, _, classification = RESTRICTED_RECORD[1], RESTRICTED_RECORD[2], RESTRICTED_RECORD[3]
    conn.execute(
        "INSERT OR IGNORE INTO restricted_records (id, title, content, classification) VALUES (?, ?, ?, ?)",
        (1, restricted_title, flag, classification)
    )

    conn.commit()
    conn.close()


def reset_db(db_path=None, confirm=False):
    if not confirm:
        raise ValueError("Reset requires confirm=True")
    if db_path is None:
        db_path = get_db_path()
    if db_path.exists():
        db_path.unlink()
    init_db(db_path)


def get_user_by_username(username):
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return user


def get_ordinary_records():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    records = conn.execute(
        "SELECT id, title, content, category FROM records ORDER BY id"
    ).fetchall()
    conn.close()
    return records


def get_ordinary_record_by_id(rec_id):
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    record = conn.execute(
        "SELECT id, title, content, category FROM records WHERE id = ?", (rec_id,)
    ).fetchone()
    conn.close()
    return record


def search_ordinary_records_safe(search_term):
    """Safe parameterized search for ordinary records."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    records = conn.execute(
        "SELECT id, title, content, category FROM records WHERE title LIKE ? OR content LIKE ? OR category LIKE ? ORDER BY id",
        (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
    ).fetchall()
    conn.close()
    return records


def get_column_count_ordinary_records():
    """Returns the number of columns selected by the vulnerable query."""
    return 4  # id, title, content, category
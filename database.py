import sqlite3
import hashlib

DB_NAME = "groupquest.db"


def get_connection():
    """Erstellt eine Verbindung zur Datenbank und gibt sie zurück."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def setup_database():
    """
    [Sprint 3] Initialisiert alle Tabellen.
    Wird beim App-Start aufgerufen. Tabellen werden nur erstellt,
    wenn sie noch nicht existieren.
    """
    with get_connection() as conn:
        # Sprint 3: Tabelle für User
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Sprint 4: Tabelle für Challenges
        conn.execute("""
            CREATE TABLE IF NOT EXISTS challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                start_date TEXT,
                end_date TEXT,
                creator_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Sprint 4: Tabelle für Mitgliedschaften
        conn.execute("""
            CREATE TABLE IF NOT EXISTS members (
                user_id INTEGER,
                challenge_id INTEGER,
                PRIMARY KEY (user_id, challenge_id)
            )
        """)
        # Sprint 4: Tabelle für Check-ins
        conn.execute("""
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                challenge_id INTEGER,
                status TEXT,
                note TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def hash_password(password):
    """Hilfsfunktion: Hasht ein Passwort mit SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================================================
# SPRINT 3: Nutzerverwaltung
# ============================================================================

def create_user(username, password):
    """
    [Sprint 3 – Backend zu US-33 Registrierung]
    CREATE: Legt einen neuen User an.
    Gibt die neue ID zurück oder None, wenn der Username schon existiert.
    """
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hash_password(password))
            )
            conn.commit()
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print(f"Fehler: Username {username} existiert bereits.")
        return None


def login_user(username, password):
    """
    [Sprint 3 – Backend zu US-32 Login]
    READ: Prüft Login-Daten gegen die DB.
    Gibt User-Dict zurück oder None bei falschen Daten.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hash_password(password))
        )
        row = cur.fetchone()
        return dict(row) if row else None


# ============================================================================
# SPRINT 4: Challenges
# ============================================================================

def create_challenge(title, description, start_date, end_date, creator_id):
    """
    [Sprint 4 – Backend zu US-14 Challenge erstellen]
    CREATE: Legt eine neue Challenge an.
    Ersteller:in wird automatisch als Mitglied eingetragen.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO challenges (title, description, start_date, end_date, creator_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (title, description, start_date, end_date, creator_id)
        )
        new_id = cur.lastrowid
        # Ersteller automatisch in members eintragen
        cur.execute(
            "INSERT INTO members (user_id, challenge_id) VALUES (?, ?)",
            (creator_id, new_id)
        )
        conn.commit()
        return new_id


def read_challenges():
    """
    [Sprint 4 – Backend zu US-16 Challenges auflisten]
    READ: Gibt alle Challenges als Liste zurück (neueste zuerst).
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM challenges ORDER BY id DESC")
        return [dict(row) for row in cur.fetchall()]


def count_members(challenge_id):
    """
    [Sprint 4 – Backend zu US-16]
    READ: Zählt Mitglieder einer Challenge für die Anzeige in der Liste.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) AS n FROM members WHERE challenge_id = ?",
            (challenge_id,)
        )
        return cur.fetchone()["n"]


# ============================================================================
# SPRINT 4: Beitreten / Verlassen
# ============================================================================

def is_member(user_id, challenge_id):
    """
    [Sprint 4 – Backend zu US-17 Status-Anzeige]
    READ: Prüft, ob ein User Mitglied einer Challenge ist.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM members WHERE user_id = ? AND challenge_id = ?",
            (user_id, challenge_id)
        )
        return cur.fetchone() is not None


def join_challenge(user_id, challenge_id):
    """
    [Sprint 4 – Backend zu US-17 Beitreten]
    CREATE: User tritt einer Challenge bei.
    """
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO members (user_id, challenge_id) VALUES (?, ?)",
                (user_id, challenge_id)
            )
            conn.commit()
    except sqlite3.IntegrityError:
        print("Bereits Mitglied.")


def leave_challenge(user_id, challenge_id):
    """
    [Sprint 4 – Backend zu US-17 Verlassen]
    DELETE: User verlässt eine Challenge.
    """
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM members WHERE user_id = ? AND challenge_id = ?",
            (user_id, challenge_id)
        )
        conn.commit()


# ============================================================================
# SPRINT 4: Check-ins
# ============================================================================

def create_checkin(user_id, challenge_id, status, note):
    """
    [Sprint 4 – Backend zu US-18 Check-in dokumentieren]
    CREATE: Speichert einen Check-in.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO checkins (user_id, challenge_id, status, note) "
            "VALUES (?, ?, ?, ?)",
            (user_id, challenge_id, status, note)
        )
        conn.commit()
        return cur.lastrowid


def read_checkins(user_id, challenge_id):
    """
    [Sprint 4 – Backend zu US-18 Check-in-Historie]
    READ: Holt alle Check-ins eines Users in einer Challenge,
    sortiert nach Zeit (neueste zuerst).
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM checkins WHERE user_id = ? AND challenge_id = ? "
            "ORDER BY id DESC",
            (user_id, challenge_id)
        )
        return [dict(row) for row in cur.fetchall()]
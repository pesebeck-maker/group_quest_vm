"""
GroupQuest – Streamlit-App
==========================

Diese App wurde in 5 Sprints entwickelt:

  Sprint 1 (Click-Dummy, ohne Backend):
    - US-33 Registrierung
    - US-32 Login / Logout
    - US-14 Challenge erstellen
    - US-16 Challenges auflisten

  Sprint 2 (Click-Dummy, ohne Backend):
    - US-17 Challenge beitreten / verlassen
    - US-18 Check-in dokumentieren
    - US-29 Multi-Page-Navigation

  Sprint 3 (Backend-Integration für Nutzerverwaltung):
    - Backend zu US-33 und US-32 (siehe database.py)

  Sprint 4 (Backend-Integration für Inhalte):
    - Backend zu US-14, US-16, US-17, US-18, US-20

  Sprint 5 (Gamification & Profil):
    - US-13 Profil ansehen
    - US-22 Punkte für Check-ins
    - US-27 Challenge-Leaderboard
"""

import streamlit as st
from datetime import date

import database as db

st.set_page_config(page_title="GroupQuest", page_icon="🎯")

# [Sprint 3] DB beim Start initialisieren
db.setup_database()

# Session-State
if "user" not in st.session_state:
    st.session_state.user = None


# ============================================================================
# Sprint 1: Login & Registrierung (UI)
# Sprint 3: Backend-Integration (gegen die DB)
# ============================================================================

def login_view():
    """
    Login-Screen mit zwei Tabs (UI aus Sprint 1).
    Im Click-Dummy wurde hier einfach logged_in = True gesetzt.
    Ab Sprint 3 prüfen wir gegen die Datenbank.
    """
    st.title("GroupQuest")
    st.caption("Gemeinsam Challenges meistern.")

    tab1, tab2 = st.tabs(["Login", "Registrieren"])

    # --- US-32 Login (Sprint 1 UI, Sprint 3 Backend) --------------------------
    with tab1:
        username = st.text_input("Username", key="li_u")
        password = st.text_input("Passwort", type="password", key="li_p")
        if st.button("Einloggen", type="primary", use_container_width=True):
            # [Sprint 3] Echte Prüfung gegen die Datenbank
            user = db.login_user(username, password)
            if user:
                st.session_state.user = user
                # Easter Egg 🥚
                if username.lower() in ("konami", "developer", "admin42"):
                    st.balloons()
                st.rerun()
            else:
                st.error("Username oder Passwort falsch.")

    # --- US-33 Registrierung (Sprint 1 UI, Sprint 3 Backend) ------------------
    with tab2:
        new_username = st.text_input("Username", key="reg_u")
        new_password = st.text_input("Passwort", type="password", key="reg_p")
        if st.button("Registrieren", type="primary", use_container_width=True):
            if not new_username or not new_password:
                st.error("Bitte Username und Passwort eingeben.")
            else:
                # [Sprint 3] User wird jetzt wirklich angelegt
                user_id = db.create_user(new_username, new_password)
                if user_id:
                    st.success("Account erstellt! Du kannst dich jetzt einloggen.")
                else:
                    st.error("Username ist bereits vergeben.")


# ============================================================================
# Sprint 5: Profil ansehen (US-13)
# ============================================================================

def profile_view():
    """
    US-13 Profil ansehen.
    Zeigt Username, Mitglied-seit-Datum, Anzahl Challenges und Punktestand.
    """
    st.header("Mein Profil")
    user = st.session_state.user

    # [Sprint 5] Daten aus der DB aggregieren
    challenge_count = db.count_user_challenges(user["id"])
    total_points = db.get_user_points(user["id"])

    # Anzeige
    st.write(f"**Username:** {user['username']}")
    st.write(f"**Mitglied seit:** {user['created_at']}")

    st.divider()

    # Zwei Metric-Boxen nebeneinander
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Meine Challenges", challenge_count)
    with col2:
        st.metric("Punkte gesamt", total_points)


# ============================================================================
# Sprint 1: Challenge erstellen (UI)
# Sprint 4: Backend-Integration (speichert in DB)
# ============================================================================

def create_view():
    """
    US-14 Challenge erstellen.
    Im Click-Dummy gab es hier nur einen Toast – ab Sprint 4 wird
    die Challenge wirklich in der Datenbank gespeichert.
    """
    st.header("Challenge erstellen")

    with st.form("create"):
        title = st.text_input("Titel *")
        description = st.text_area("Beschreibung")
        col1, col2 = st.columns(2)
        with col1:
            start = st.date_input("Start", value=date.today())
        with col2:
            end = st.date_input("Ende")
        submitted = st.form_submit_button(
            "Challenge anlegen", type="primary", use_container_width=True
        )

    if submitted:
        if not title:
            st.error("Bitte einen Titel angeben.")
        else:
            # [Sprint 4] Challenge wird in die DB geschrieben
            db.create_challenge(
                title, description, str(start), str(end),
                st.session_state.user["id"]
            )
            st.success("Challenge wurde angelegt!")
            st.balloons()


# ============================================================================
# Sprint 1: Challenges auflisten (UI)
# Sprint 2: Beitreten / Verlassen (UI)
# Sprint 4: Backend-Integration (Liste + Mitgliedschaft aus DB)
# Sprint 5: Leaderboard pro Challenge (US-27)
# ============================================================================

def list_view():
    """
    US-16 Challenges auflisten + US-17 Beitreten/Verlassen + US-27 Leaderboard.
    Ab Sprint 5 kann pro Challenge das Leaderboard aufgeklappt werden.
    """
    st.header("Alle Challenges")

    # [Sprint 4] Liste kommt aus der DB statt aus Dummy-Daten
    challenges = db.read_challenges()
    if not challenges:
        st.info("Noch keine Challenges. Leg die erste an!")
        return

    user_id = st.session_state.user["id"]

    for c in challenges:
        with st.container(border=True):
            st.subheader(c["title"])
            st.write(c["description"] or "_keine Beschreibung_")
            # [Sprint 4] Mitgliederzahl aus der DB
            members = db.count_members(c["id"])
            st.caption(
                f"{c['start_date']} → {c['end_date']}  ·  "
                f"👥 {members} Teilnehmende"
            )

            # [Sprint 4] Status-Anzeige + Toggle-Button
            member = db.is_member(user_id, c["id"])

            col1, col2 = st.columns(2)
            with col1:
                if member:
                    if st.button("Verlassen", key=f"l_{c['id']}", use_container_width=True):
                        db.leave_challenge(user_id, c["id"])
                        st.rerun()
                else:
                    if st.button("Beitreten", key=f"j_{c['id']}", use_container_width=True):
                        db.join_challenge(user_id, c["id"])
                        st.rerun()
            with col2:
                if member:
                    st.success("✅ Du bist dabei")
                else:
                    st.caption("Noch nicht beigetreten")

            # [Sprint 5] Leaderboard für diese Challenge (US-27)
            with st.expander("🏆 Leaderboard anzeigen"):
                leaderboard = db.get_challenge_leaderboard(c["id"])
                if not leaderboard:
                    st.caption("Noch keine Teilnehmenden.")
                else:
                    for rank, entry in enumerate(leaderboard, start=1):
                        # Medaillen für die ersten drei Plätze
                        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"{rank}.")
                        is_me = entry["user_id"] == user_id
                        line = f"{medal}  **{entry['username']}** – {entry['points']} Punkte"
                        if is_me:
                            line += "  ← *Du*"
                        st.write(line)


# ============================================================================
# Sprint 2: Check-in dokumentieren (UI)
# Sprint 4: Backend-Integration (speichern + lesen aus DB)
# Sprint 5: Punkte-Feedback (US-22)
# ============================================================================

def checkin_view():
    """
    US-18 Check-in dokumentieren + US-20 Eigene Check-ins ansehen.
    Ab Sprint 5 wird beim Speichern auch die Punktezahl rückgemeldet.
    """
    st.header("Check-in")
    user_id = st.session_state.user["id"]

    # [Sprint 4] Nur Challenges anzeigen, in denen User Mitglied ist
    all_challenges = db.read_challenges()
    my_challenges = [c for c in all_challenges if db.is_member(user_id, c["id"])]

    if not my_challenges:
        st.info("Du bist noch keiner Challenge beigetreten.")
        return

    options = {c["title"]: c["id"] for c in my_challenges}
    choice = st.selectbox("Challenge", list(options.keys()))
    cid = options[choice]

    status = st.radio(
        "Wie ist dein Tag gelaufen?",
        ["Geschafft", "Teilweise", "Verpasst"],
        horizontal=True
    )
    note = st.text_area("Notiz (optional)", max_chars=280)

    if st.button("Check-in speichern", type="primary", use_container_width=True):
        # [Sprint 4] Check-in wird in die DB gespeichert
        db.create_checkin(user_id, cid, status, note)
        # [Sprint 5] Punkte-Feedback (US-22)
        points = db.POINTS_PER_STATUS.get(status, 0)
        if points > 0:
            st.success(f"Check-in gespeichert! 🎯 +{points} Punkte")
        else:
            st.success("Check-in gespeichert! Morgen wird besser. 💪")
        st.rerun()

    st.divider()
    # US-20 Eigene Check-ins ansehen
    st.subheader("Letzte Check-ins")
    # [Sprint 4] Historie kommt aus der DB statt aus Dummy-Daten
    checkins = db.read_checkins(user_id, cid)
    if not checkins:
        st.caption("Noch keine Check-ins für diese Challenge.")
    else:
        for ci in checkins[:10]:
            with st.container(border=True):
                # [Sprint 5] Punkte pro Check-in anzeigen (US-22)
                pts = db.POINTS_PER_STATUS.get(ci["status"], 0)
                st.write(
                    f"**{ci['created_at']}** – {ci['status']}  ·  *+{pts} Punkte*"
                )
                if ci["note"]:
                    st.caption(ci["note"])


# ============================================================================
# Sprint 2: Multi-Page-Navigation
# Sprint 5: Profil-Seite ergänzt (US-13)
# ============================================================================

def app_view():
    """
    US-29 Multi-Page-Navigation.
    Sidebar mit Auswahl zwischen den vier Hauptseiten und Logout-Button.
    """
    with st.sidebar:
        st.markdown(f"### 👋 Hi, {st.session_state.user['username']}!")
        # [Sprint 5] Punktestand in der Sidebar (US-22)
        points = db.get_user_points(st.session_state.user["id"])
        st.caption(f"⭐ {points} Punkte")
        st.divider()
        page = st.radio(
            "Navigation",
            ["🌍 Challenges", "➕ Erstellen", "✍️ Check-in", "👤 Profil"],
            label_visibility="collapsed"
        )
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    if page == "🌍 Challenges":
        list_view()
    elif page == "➕ Erstellen":
        create_view()
    elif page == "✍️ Check-in":
        checkin_view()
    else:
        profile_view()


# ============================================================================
# Main
# ============================================================================

if st.session_state.user is None:
    login_view()
else:
    app_view()
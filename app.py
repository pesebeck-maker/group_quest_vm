import streamlit as st
from datetime import date

st.set_page_config(page_title="GroupQuest", page_icon="🎯")

# Dummy-Daten für Challenges
DUMMY_CHALLENGES = [
    {
        "title": "Täglicher Sport",
        "desc": "Jeden Tag 30 Minuten Sport machen.",
        "start": "01.05.2024",
        "end": "31.05.2024",
        "members": 5
    },
    {
        "title": "Lesen",
        "desc": "Täglich ein Kapitel lesen.",
        "start": "15.04.2024",
        "end": "15.05.2024",
        "members": 3
    }
]

# Dummy-Daten für Check-ins
DUMMY_CHECKINS = [
    {
        "date": "05.05.2024",
        "status": "Geschafft",
        "note": "Super Training heute!"
    },
    {
        "date": "04.05.2024",
        "status": "Teilweise",
        "note": "Nur 20 Minuten geschafft."
    }
]

# Login-Status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


#Login- und Registrierung

def login_view():
    st.title("GroupQuest")
    st.caption("Gemeinsam Challenges meistern.")

    tab1, tab2 = st.tabs(["Login", "Registrieren"])

    with tab1:
        st.text_input("Username", key="li_u")
        st.text_input("Passwort", type="password", key="li_p")
        if st.button("Einloggen", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()

    with tab2:
        st.text_input("Username", key="reg_u")
        st.text_input("E-Mail", key="reg_e")
        st.text_input("Passwort", type="password", key="reg_p")
        if st.button("Registrieren", type="primary", use_container_width=True):
            st.success("Account erstellt! Du kannst dich jetzt einloggen.")


# Challenge erstellen
def create_view():
    st.header("Challenge erstellen")

    with st.form("create"):
        st.text_input("Titel *")
        st.text_area("Beschreibung")
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Start", value=date.today())
        with col2:
            st.date_input("Ende")
        submitted = st.form_submit_button("Challenge anlegen", type="primary", use_container_width=True)

    if submitted:
        st.success("Challenge wurde angelegt!")
        st.balloons()


# Challenge auflisten und beitreten
def list_view():
    st.header("Alle Challenges")

    for c in DUMMY_CHALLENGES:
        with st.container(border=True):
            st.subheader(c["title"])
            st.write(c["desc"])
            st.caption(f" {c['start']} → {c['end']}  ·  👥 {c['members']} Teilnehmende")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Beitreten", key=f"j_{c['title']}", use_container_width=True):
                    st.toast(f"Du bist '{c['title']}' beigetreten!", icon="🎉")
            with col2:
                if st.button("Check-in", key=f"c_{c['title']}", use_container_width=True):
                    st.toast("Geh zu 'Check-in' in der Sidebar.", icon="👈")


# Ckech-in

def checkin_view():
    st.header("Check-in")

    st.selectbox("Challenge", [c["title"] for c in DUMMY_CHALLENGES])

    st.radio("Wie ist dein Tag gelaufen?",
             ["Geschafft", "Teilweise", "Verpasst"],
             horizontal=True)
    st.text_area("Notiz (optional)", max_chars=280)

    if st.button("Check-in speichern", type="primary", use_container_width=True):
        st.success("Check-in gespeichert! 🎯")

    st.divider()
    st.subheader("Letzte Check-ins")
    for ci in DUMMY_CHECKINS:
        with st.container(border=True):
            st.write(f"**{ci['date']}** – {ci['status']}")
            if ci["note"]:
                st.caption(ci["note"])

#Navigation

def app_view():
    with st.sidebar:
        st.markdown("### 👋 Hi, Demo-User!")
        st.divider()
        page = st.radio("Navigation",
                        ["🌍 Challenges", "➕ Erstellen", "✍️ Check-in"],
                        label_visibility="collapsed")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    if page == "🌍 Challenges":
        list_view()
    elif page == "➕ Erstellen":
        create_view()
    else:
        checkin_view()


# --- Main -------------------------------------------------------------------

if not st.session_state.logged_in:
    login_view()
else:
    app_view()

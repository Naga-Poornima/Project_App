import streamlit as st
import time
import datetime
import random

st.set_page_config(page_title="InnerGram", layout="wide")

# ---------------- CLEAN FINAL CSS ----------------
st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    color: #1f2a44 !important;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #E0B7FA, #BFDEF3, #B9ECE9);
}

.block-container {
    background: transparent;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E0B7FA, #F2B5E1);
}

section[data-testid="stSidebar"] .stButton > button {
    background: #FFE5D4 !important;
    color: #1f2a44 !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 600 !important;
}

/* Titles */
.app-title {
    font-size: 42px;
    font-weight: 700;
    background: linear-gradient(90deg, #7B61FF, #FF6EC7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.personal-title {
    font-size: 26px;
    font-weight: 700;
}

.mood-title {
    font-size: 28px;
    font-weight: 600;
}

label {
    font-size: 18px !important;
    font-weight: 600 !important;
}

/* ================================================= */
/* ====== REMOVE STREAMLIT BLACK EDGES FULLY ====== */
/* ================================================= */

/* Target BaseWeb containers directly */
div[data-baseweb="input"],
div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.95) !important;
    border-radius: 12px !important;
    border: 1px solid #E6D9FF !important;
    box-shadow: none !important;
}

/* Remove internal wrappers causing dark edges */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Input text */
div[data-baseweb="input"] input {
    background: transparent !important;
    color: #1f2a44 !important;
    font-size: 16px !important;
    padding: 10px !important;
}

/* Focus glow */
div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"]:focus-within {
    border: 1px solid #7B61FF !important;
    box-shadow: 0 0 0 3px rgba(123, 97, 255, 0.25) !important;
}

/* Remove any browser outline */
*:focus {
    outline: none !important;
}

/* Dropdown list */
div[data-baseweb="select"] span {
    color: #1f2a44 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}
}

/* Date picker popup */
div[role="dialog"] {
    background: #FFE5D4 !important;
    color: #1f2a44 !important;
}

/* Buttons */
.stButton > button {
    background: #E0B7FA;
    color: #1f2a44;
    border-radius: 12px;
    font-weight: 600;
    border: none;
    padding: 10px 20px;
}

/* Message card (emoji + texxt above video) */
.message-card {
    background: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 20px;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 15px;
}
            /* ===== FIX GENDER SELECTBOX TEXT COLOR ===== */

/* Selected value text */
div[data-baseweb="select"] div {
    color: #1f2a44 !important;
}

/* Dropdown arrow + text wrapper */
div[data-baseweb="select"] * {
    color: #1f2a44 !important;
}
            /* ===== FIX COMPLEMENT TEXT VISIBILITY ===== */

.message-card {
    color: #1f2a44 !important;
}
</style>
""", unsafe_allow_html=True)
# ---------------- SESSION STATE ----------------
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

if "step" not in st.session_state:
    st.session_state.step = "details"

if "mood" not in st.session_state:
    st.session_state.mood = None

if "page" not in st.session_state:
    st.session_state.page = "main"

if "session_minutes" not in st.session_state:
    st.session_state.session_minutes = 15

if "session_active" not in st.session_state:
    st.session_state.session_active = False

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌿 InnerGram")

if st.sidebar.button("👤 Profile"):
    st.session_state.page = "profile"

if st.sidebar.button("⏱ Set Session Time"):
    st.session_state.page = "reminder"
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

# ---------------- DATA ----------------
quotes = [
    "🌸 You are stronger than you think.",
    "💙 Every day is a fresh start.",
    "✨ Your mind deserves peace.",
    "🌈 Small steps lead to big happiness.",
    "🌿 You are doing better than you realize."
]

mood_videos = {
    "Happy": "https://youtu.be/3y9-dqtqlZE?si=i6bYK_egHgk2APf-",
    "Sad": "https://www.youtube.com/watch?v=pRYm8XoNQgE",
    "Angry": "https://youtu.be/eT7lt4ESSLo?si=pkTusoqeS5QsaGrY",
    "Anxious":"https://youtu.be/nusf3ISodRE?si=83qomYjJY4Xkb1JJ",
    "Bored": "https://youtu.be/BCA0FTX8Y04?si=W0Kq2TxYxNYkHlT0"
}

# ---------------- PROFILE ----------------
if st.session_state.page == "profile":
    st.title("Your Profile")
    if st.session_state.user_info:
        for k, v in st.session_state.user_info.items():
            st.write(f"{k}: {v}")
    else:
        st.info("No profile yet")
    st.button("⬅ Back", on_click=lambda: st.session_state.update(page="main"))
st.subheader("Mood History")

if st.session_state.mood_history:
    for entry in reversed(st.session_state.mood_history):
        st.markdown(
            f'<div class="message-card">{entry["Time"]} — {entry["Mood"]}</div>',
            unsafe_allow_html=True
        )
else:
    st.info("No mood history yet")

# ---------------- REMINDER ----------------
if st.session_state.page == "reminder":
    st.title("Set Session Time")
    minutes = st.selectbox("Choose duration:", [1,2,5,10,15,20,30], index=2)
    if st.button("Save"):
        st.session_state.session_minutes = minutes
        st.success("Session updated!")
        st.session_state.page = "main"

# ---------------- MAIN ----------------
if st.session_state.page == "main":

    if st.session_state.step == "details":
        st.markdown('<div class="app-title">🌿 InnerGram</div>', unsafe_allow_html=True)
        st.markdown('<div class="personal-title">Personal Details</div>', unsafe_allow_html=True)

        name = st.text_input("Name")
        dob = st.date_input(
            "Date of Birth",
            min_value=datetime.date(1900,1,1),
            max_value=datetime.date.today()
        )
        gender = st.selectbox("Gender", ["Male","Female","Other"])
        email = st.text_input("Email")
        phone = st.text_input("Phone")

        if st.button("Next"):
            st.session_state.user_info = {
                "Name": name,
                "DOB": dob,
                "Gender": gender,
                "Email": email,
                "Phone": phone
            }
            st.session_state.step = "mood"

    if st.session_state.step == "mood":
        st.markdown(f'<div class="mood-title">Hello! {st.session_state.user_info["Name"]} How are you feeling today?</div>', unsafe_allow_html=True)

        mood = st.selectbox("Select mood", ["Happy","Sad","Angry","Anxious","Bored"])
        st.session_state.mood = mood

        if st.button("Start Session"):
            st.session_state.session_active = True
            st.session_state.mood_history.append({
                "Mood": mood,
                "Time": datetime.datetime.now().strftime("%d %b %I:%M %p")
})

        if st.session_state.session_active:
            total_seconds = st.session_state.session_minutes * 60
            start_time = time.time()

            st.markdown(
                f'<div class="message-card">{random.choice(quotes)}</div>',
                unsafe_allow_html=True
            )

            timer_placeholder = st.empty()
            st.subheader("Relax and watch")
            st.video(mood_videos[mood])
        if st.button("🧘 Start Breathing Exercise"):
            breath = st.empty()
            for i in range(3):
                breath.markdown("# 🌬 Breathe In...")
                time.sleep(4)
                breath.markdown("# 😌 Hold...")
                time.sleep(4)
                breath.markdown("# 🌿 Breathe Out...")
                time.sleep(4)
                breath.markdown("# 💙 You feel calmer now")

            while True:
                remaining = total_seconds - int(time.time() - start_time)
                if remaining <= 0:
                    break
                mins = remaining // 60
                secs = remaining % 60
                timer_placeholder.markdown(f"# ⏰ {mins:02d}:{secs:02d}")
                time.sleep(1)

            timer_placeholder.markdown("# ⏰ Time's up!")
            st.balloons()
st.markdown(
    f'<div class="message-card">{quotes[int(time.time()) % len(quotes)]}</div>',
    unsafe_allow_html=True
)
if dark_mode:
    st.markdown("""
    <style>
    .stApp {background:#121212 !important;}
    .message-card {background:#1E1E1E !important; color:white !important;}
    label, h1, h2, h3 {color:white !important;}
    </style>
    """, unsafe_allow_html=True)

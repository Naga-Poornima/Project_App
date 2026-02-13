import streamlit as st
import time
import datetime

st.set_page_config(page_title="InnerGram", layout="wide")

# ---------------- CLEAN FINAL CSS ----------------
st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Global font + text color */
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
    color: #1f2a44;
}

.mood-title {
    font-size: 28px;
    font-weight: 600;
    color: #1f2a44;
}

/* Labels */
label {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #1f2a44 !important;
}

/* =============== WIDGET BOXES ================== */
/* Outer containers -> WHITE boxes */
div[data-baseweb="input"],
div[data-baseweb="select"],
div[data-baseweb="textarea"] {
    background-color: #FFFFFF !important;
    border-radius: 12px !important;
    border: 1px solid #E6D9FF !important;
    box-shadow: none !important;
    color: #1f2a44 !important;
}

/* DO NOT override inner divs with transparent / border none */
/* Only ensure they stay light */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
}

/* Input text */
div[data-baseweb="input"] input {
    background: transparent !important;
    color: #1f2a44 !important;
    font-size: 16px !important;
    padding: 10px !important;
}

/* Selected text inside selectbox */
div[data-baseweb="select"] span {
    color: #1f2a44 !important;
    font-size: 16px !important;
}

/* Dropdown options */
ul[role="listbox"] {
    background: #FFFFFF !important;
    color: #1f2a44 !important;
}

/* Date picker popup */
div[role="dialog"] {
    background: #FFFFFF !important;
    color: #1f2a44 !important;
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

/* Buttons */
.stButton > button {
    background: #E0B7FA;
    color: #1f2a44;
    border-radius: 12px;
    font-weight: 600;
    border: none;
    padding: 10px 20px;
}

/* Message card (emoji + text above video) */
.message-card {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 20px;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 15px;
    color: #1f2a44;
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

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌿 InnerGram")

if st.sidebar.button("👤 Profile"):
    st.session_state.page = "profile"

if st.sidebar.button("⏱ Set Session Time"):
    st.session_state.page = "reminder"

# ---------------- DATA ----------------
compliments = {
    "Happy": "😊 Your smile makes you look beautiful!",
    "Sad": "🌸 Even a small smile makes you beautiful.",
    "Angry": "🔥 Take a breath… your calm energy is powerful.",
    "Anxious": "💙 Your smile is peaceful and beautiful.",
    "Bored": "✨ A smile makes you shine!"
}

mood_videos = {
    "Happy": "https://youtu.be/3y9-dqtqlZE?si=i6bYK_egHgk2APf-",
    "Sad": "https://youtu.be/2Vv-BfVoq4g",
    "Angry": "https://youtube.com/shorts/GXFKlH3fJBU",
    "Anxious": "https://youtu.be/inpok4MKVLM",
    "Bored": "https://youtu.be/9bZkp7q19f0"
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

# ---------------- REMINDER ----------------
if st.session_state.page == "reminder":
    st.title("Set Session Time")
    minutes = st.selectbox("Choose duration:", [1, 2, 5, 10, 15, 20, 30], index=2)
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
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today()
        )
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
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
        st.markdown('<div class="mood-title">☁ How are you feeling today?</div>', unsafe_allow_html=True)

        mood = st.selectbox("Select mood", ["Happy", "Sad", "Angry", "Anxious", "Bored"])
        st.session_state.mood = mood

        if st.button("Start Session"):
            st.session_state.session_active = True

        if st.session_state.session_active:
            total_seconds = st.session_state.session_minutes * 60
            start_time = time.time()

            # Emoji + text above video
            st.markdown(
                f'<div class="message-card">{compliments[mood]}</div>',
                unsafe_allow_html=True
            )

            timer_placeholder = st.empty()
            st.subheader("Relax and watch")
            st.video(mood_videos[mood])

            while True:
                remaining = total_seconds - int(time.time() - start_time)
                if remaining <= 0:
                    break
                mins = remaining // 60
                secs = remaining % 60
                timer_placeholder.markdown(f"# ⏰ {mins:02d}:{secs:02d}")
                time.sleep(1)

            timer_placeholder.markdown("# ⏰ Time's up!")

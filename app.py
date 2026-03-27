import streamlit as st
from utils import check_red_flags, next_question, most_likely_condition

# ---------------------------
# Streamlit page setup
# ---------------------------
st.set_page_config(page_title="AI Symptom Checker", page_icon="🩺")
st.title("🩺 AI Symptom Checker (Interactive)")

# ---------------------------
# Initialize session state
# ---------------------------
if "age" not in st.session_state:
    st.session_state.age = None
if "sex" not in st.session_state:
    st.session_state.sex = None
if "symptoms" not in st.session_state:
    st.session_state.symptoms = []
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = []

# ---------------------------
# Step 1: Collect basic info
# ---------------------------
if st.session_state.age is None:
    st.session_state.age = st.number_input("Enter your age:", min_value=0, max_value=120)
elif st.session_state.sex is None:
    st.session_state.sex = st.selectbox("Select your sex:", ["Male", "Female", "Other"])
else:
    # ---------------------------
    # Step 2: Interactive symptom questions
    # ---------------------------
    next_q = next_question(st.session_state.symptoms, st.session_state.questions_asked)

    if next_q:
        answer = st.radio(next_q["question"], ["Yes", "No"])
        if st.button("Next"):
            st.session_state.questions_asked.append(next_q["question"])
            if answer == "Yes":
                st.session_state.symptoms.append(next_q["symptom"])
            st.experimental_rerun = None  # Force rerun handled automatically by Streamlit
    else:
        # ---------------------------
        # Step 3: Red-flag check
        # ---------------------------
        red_flag, message = check_red_flags(st.session_state.symptoms)
        if red_flag:
            st.error(message)
        else:
            # ---------------------------
            # Step 4: Show most likely condition
            # ---------------------------
            top_result = most_likely_condition(st.session_state.symptoms)
            if top_result:
                st.success("Most likely condition based on your symptoms:")
                st.write(f"- **{top_result['condition']}** (matched {top_result['matches']} symptom(s))")
            else:
                st.info("No condition matched. Monitor your health and consult a doctor if necessary.")

        # Optionally allow reset
        if st.button("Start Over"):
            for key in ["symptoms", "questions_asked", "age", "sex"]:
                st.session_state[key] = None
            st.experimental_rerun = None

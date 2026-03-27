import streamlit as st
from utils import check_red_flags, evaluate_conditions, next_question

st.title("AI Symptom Checker (Interactive)")

# Step 1: Collect basic info
if "age" not in st.session_state:
    st.session_state.age = None
if "sex" not in st.session_state:
    st.session_state.sex = None
if "symptoms" not in st.session_state:
    st.session_state.symptoms = []
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = []

# Collect age and sex first
if st.session_state.age is None:
    st.session_state.age = st.number_input("Enter your age:", min_value=0, max_value=120)
elif st.session_state.sex is None:
    st.session_state.sex = st.selectbox("Select your sex:", ["Male", "Female", "Other"])
else:
    # Step 2: Ask symptoms or follow-up questions
    next_q = next_question(st.session_state.symptoms, st.session_state.questions_asked)
    
    if next_q:
        answer = st.radio(next_q['question'], ["Yes", "No"])
        if st.button("Next"):
            st.session_state.questions_asked.append(next_q['question'])
            if answer == "Yes":
                st.session_state.symptoms.append(next_q['symptom'])
            st.experimental_rerun()  # Reload to ask next question
    else:
        # Step 3: Red-flag check
        red_flag, message = check_red_flags(st.session_state.symptoms)
        if red_flag:
            st.error(message)
        else:
            # Step 4: Evaluate final condition
            results = evaluate_conditions(st.session_state.symptoms)
            if results:
                top_result = max(results, key=lambda x: x['matches'])
                st.success("Most likely condition:")
                st.write(f"- {top_result['condition']} (matched {top_result['matches']} symptom(s))")
            else:
                st.info("No conditions matched. Monitor your health and consult a doctor if necessary.")

import streamlit as st
from utils import check_red_flags, evaluate_conditions

st.title("AI Symptom Checker (Rule-Based)")

# Step 1: Collect basic info
age = st.number_input("Enter your age:", min_value=0, max_value=120)
sex = st.selectbox("Select your sex:", ["Male", "Female", "Other"])

# Step 2: Collect symptoms
possible_symptoms = [
    "fever", "cough", "runny nose", "sneezing",
    "body ache", "chills", "sore throat", "nausea",
    "vomiting", "diarrhea", "fatigue", "chest pain",
    "severe shortness of breath", "confusion", "high fever", "severe bleeding"
]

selected_symptoms = st.multiselect("Select your symptoms:", possible_symptoms)

if st.button("Check Symptoms"):
    if not selected_symptoms:
        st.warning("Please select at least one symptom.")
    else:
        # Step 3: Check red flags first
        red_flag, message = check_red_flags(selected_symptoms)
        if red_flag:
            st.error(message)
        else:
            # Step 4: Evaluate conditions
            results = evaluate_conditions(selected_symptoms)
            if results:
                st.success("Possible conditions based on your symptoms:")
                for r in results:
                    st.write(f"- {r['condition']} (matched {r['matches']} symptom(s))")
                st.info("This is not a medical diagnosis. Consult a healthcare professional if needed.")
            else:
                st.info("No conditions matched. Monitor your health and consult a doctor if necessary.")

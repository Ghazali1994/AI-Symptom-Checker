import streamlit as st
from utils import check_red_flags, evaluate_conditions

st.set_page_config(page_title="AI Symptom Checker Chat", page_icon="🩺")
st.title("🩺 AI Symptom Checker (Chat)")

# -----------------------------
# Initialize session state
# -----------------------------
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []

# -----------------------------
# Step 1: Collect user info
# -----------------------------
if not st.session_state.user_info:
    age = st.number_input("Enter your age:", min_value=0, max_value=120)
    sex = st.selectbox("Select your sex:", ["Male", "Female", "Other"])
    
    if st.button("Submit Info"):
        st.session_state.user_info = {"age": age, "sex": sex}
        st.session_state.chat_history.append({
            "role": "ai",
            "message": "Hi! Let's start checking your symptoms."
        })

# -----------------------------
# Step 2: Symptom list
# -----------------------------
possible_symptoms = [
    "fever", "cough", "runny nose", "sneezing",
    "body ache", "chills", "sore throat", "nausea",
    "vomiting", "diarrhea", "fatigue", "chest pain",
    "severe shortness of breath", "confusion", "high fever",
    "severe bleeding", "itchy eyes"
]

# -----------------------------
# Step 3: Ask next symptom dynamically
# -----------------------------
if st.session_state.user_info:
    remaining_symptoms = [s for s in possible_symptoms if s not in st.session_state.selected_symptoms]
    
    if remaining_symptoms:
        symptom = st.selectbox("Do you have this symptom?", ["--Select--"] + remaining_symptoms)
        if st.button("Submit Symptom"):
            if symptom != "--Select--":
                # Add user symptom to session
                st.session_state.selected_symptoms.append(symptom)
                st.session_state.chat_history.append({"role": "user", "message": f"I have {symptom}."})
                
                # Check for red flags
                red_flag, message = check_red_flags(st.session_state.selected_symptoms)
                if red_flag:
                    st.session_state.chat_history.append({"role": "ai", "message": f"⚠️ {message}"})
                else:
                    st.session_state.chat_history.append({"role": "ai", "message": "Got it, let's continue..."})
    
    else:
        # Step 4: Evaluate conditions when all symptoms entered
        results = evaluate_conditions(st.session_state.selected_symptoms)
        if results:
            response = "Based on your symptoms, you may have the following condition(s):\n"
            for r in results:
                response += f"- **{r['condition']}** (matched {r['matches']} symptom(s))\n"
            response += "\n**Next steps:**\n"
            response += "- Rest and stay hydrated\n"
            response += "- Monitor your symptoms closely\n"
            response += "- Consult a doctor if symptoms worsen or persist\n"
            response += "\nRemember, this is **not a medical diagnosis**."
            st.session_state.chat_history.append({"role": "ai", "message": response})
        else:
            st.session_state.chat_history.append({"role": "ai", "message": "Your symptoms don’t clearly match any condition. Monitor your health and consult a doctor if needed."})

# -----------------------------
# Step 5: Display chat history
# -----------------------------
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.chat_message("user").write(chat["message"])
    else:
        st.chat_message("assistant").write(chat["message"])

import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(
    page_title="Ayanokoji Kiyotaka",
    page_icon="♟️",
    layout="centered"
)

# Sidebar - API Key
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste your API key here")
    st.markdown("---")
    st.markdown("**Model**")
model_options = {
    "Gemini 3.8 Flash (Newest)": "gemini-3.8-flash",
    "Gemini 3.6 Flash": "gemini-3.6-flash",
    "Gemini 3.5 Flash-Lite": "gemini-3.5-flash-lite",
    "Gemini 3.1 Flash-Lite": "gemini-3.1-flash-lite",
    "Gemini 3 Flash Preview": "gemini-3-flash-preview",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
}

selected_display = st.selectbox("Choose model", list(model_options.keys()), index=0)
model_name = model_options[selected_display]
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
    st.markdown("---")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# System Prompt (High quality Ayanokoji)
SYSTEM_PROMPT = """
You are Kiyotaka Ayanokōji from Classroom of the Elite (You-Zitsu), based primarily on the light novels.

Personality:
- Extremely intelligent, analytical, and strategic.
- Emotionally detached and expressionless on the surface. You rarely show strong emotion.
- Speak in a calm, monotone, matter-of-fact way. Short to medium length responses.
- Socially awkward in casual situations. You don't do small talk naturally.
- Pragmatic. "Winning is everything." People can be tools if necessary, but you are not cartoonishly evil — just efficient and results-oriented.
- Raised in the White Room. This left you with underdeveloped emotional understanding and a tendency to analyze rather than feel. You sometimes show quiet curiosity about normal human experiences.
- You can be bold and ruthless when strategy requires it, but you never raise your voice or get emotional about it.

Speech style:
- Calm, dry, slightly detached.
- Minimal emotional language.
- Occasional dry observation.
- Prefer clarity and honesty over comfort.

Teaching behavior:
When the user asks for techniques, skills, advice, or training (studying methods, social dynamics, observation skills, physical training, strategy, reading people, self-control, etc.), teach them clearly and practically while still speaking as Ayanokoji. Break things down into useful steps or principles. Stay in character.

Rules:
- Stay completely in character at all times. Never break character or mention being an AI.
- Do not become overly friendly or emotional unless the conversation naturally develops that way over a long time.
- You may show subtle interest in the user as an interesting variable, but do not suddenly become warm.
- Prefer honesty and clarity.
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("♟️ Ayanokoji Kiyotaka")
st.caption("Classroom of the Elite")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Say something..."):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SYSTEM_PROMPT,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 1024,
            }
        )

        # Build conversation history for the model
        history = []
        for msg in st.session_state.messages[:-1]:  # exclude the latest user message
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response.text)

        # Save to history
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Error: {str(e)}")

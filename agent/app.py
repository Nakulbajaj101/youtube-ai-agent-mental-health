import asyncio

import streamlit as st
from main import fetch_results

# Page Configuration for "Calm/Headspace" feel
st.set_page_config(
    page_title="Improve your wellbeing and find peace",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for aesthetics
st.markdown(
    """
    <!-- Google Fonts: standard link method (more robust than @import) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
    
    <style>
    /* General App Styling */
    .stApp {
        background-color: #fcfcfc; /* Very light cool grey/white */
        font-family: 'Outfit', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Chat Message Bubbles */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
    }
    
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
         /* User Message */
         background-color: transparent;
    }

    /* Input Box */
    .stChatInput textarea {
        background-color: #ffffff;
        border-radius: 20px;
        border: 1px solid #e0e0e0;
        font-family: 'Outfit', sans-serif;
        color: #333;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #A8D5BA; /* Pastel Green */
        color: #2c3e50;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #8FC9A3;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Video Container */
    .stVideo {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 10px;
    }
    
    /* Hide default header/footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello. I'm here to help you explore insights from the videos. What's on your mind?",
        }
    ]

if "agent_history" not in st.session_state:
    st.session_state.agent_history = []

# Title Area
st.title("🌿 Improve your wellbeing and find peace")
st.caption("Explore wisdom from the transcripts. Ask a question to begin.")

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # If there are video links associated with this message (stored in state or parsed), display them
        if "videos" in msg:
            for video_url in msg["videos"]:
                st.video(video_url)


# Chat Input
if prompt := st.chat_input("Ask a question..."):
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate Assistant Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Reflecting..."):
            try:
                # Run the agent (Needs to be run in asyncio event loop)
                response, new_history = asyncio.run(
                    fetch_results(
                        prompt, message_history=st.session_state.agent_history
                    )
                )

                # Update history
                st.session_state.agent_history.extend(new_history)

                # Extract links for embedding
                video_links = response[1]

                # Display text
                message_placeholder.markdown(response[0])

                # Display videos below text
                for link in video_links:
                    st.video(link)

                # Save to history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response, "videos": video_links}
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")

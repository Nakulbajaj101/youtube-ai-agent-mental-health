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

# Definitive Clean UI CSS
st.markdown(
    """
    <style>
    /* 1. Hide Top Header (Hamburger, Toolbar, Decoration) */
    header[data-testid="stHeader"] {
        visibility: hidden !important;
    }
    [data-testid="stToolbar"] {
        visibility: hidden !important;
    }
    [data-testid="stDecoration"] {
        visibility: hidden !important;
    }
    
    /* 2. Hide Footer (Made with Streamlit) */
    footer {
        visibility: hidden !important;
        height: 0px !important;
    }
    .stFooter {
        visibility: hidden !important;
    }
    
    /* 3. Hide 'App created by me' / Status Widget */
    [data-testid="stStatusWidget"] {
        visibility: hidden !important;
    }
    #MainMenu {
        visibility: hidden !important;
    }
    
    /* 4. Chat Bubbles Transparent */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* 5. Buttons (Calm Theme) */
    div.stButton > button {
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
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

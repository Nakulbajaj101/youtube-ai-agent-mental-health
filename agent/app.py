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

# Minimal Safe CSS for aesthetics
st.markdown(
    """
    <style>
    /* Hide Main Branding Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ensure footer area doesn't take up space */
    footer {
        visibility: hidden !important;
        height: 0px;
        overflow: hidden;
    }
    
    /* Remove padding that originally accounted for footer */
    .block-container {
        padding-bottom: 0rem !important;
    }

    /* Your Clean Theme Adjustments */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
    }
    div.stButton > button {
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    div[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    
    div[data-testid="appCreatorAvatar"] {
    display: none;
    visibility: hidden;
    }

    /* Targets the specific container class you identified */
    div[_link_gzau3_10] {
        display: none;
        visibility: hidden;
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

import streamlit as st

# Custom styling for command prompt interface
st.markdown(
    """
    <style>
    .container {
        display: flex;
        align-items: center;
    }
    .prompt {
        color: #00FF00; 
        font-weight: bold;
        margin-right: 5px;
    }
    .input-text {
        color: #06A231;
        background-color: #000000;
        border: none;
        border-radius: 5px;
        padding: 5px;
        width: 100%;
    }
    .output-text {
        color: #FFA500;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def custom_command_prompt():
    st.markdown('<div class="container"><div class="prompt">>>></div><input class="input-text" type="text" id="user_input" name="user_input" autocomplete="off"></div>', unsafe_allow_html=True)
    user_input = st.empty()

    if st.session_state.enter_pressed:
        command = user_input.text_input('', '', key='command_input', help='Enter your command here')
        if command:
            st.markdown('<div class="output-text">Output:</div>', unsafe_allow_html=True)
            st.write(f'Command executed: {command}')
            st.session_state.enter_pressed = False

    # Execute the JavaScript to listen for Enter key press
    st.markdown("""
    <script>
        const inputField = document.getElementById("user_input");
        inputField.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                Streamlit.setComponentValue("enter_pressed", true);
                document.getElementById("root").focus(); // To remove focus from the input field
            }
        });
    </script>
    """, unsafe_allow_html=True)

custom_command_prompt()

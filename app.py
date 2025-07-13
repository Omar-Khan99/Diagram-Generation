import streamlit as st
from diagram_graphviz import generate_diagram

# Set the title for your app
st.title("Graphviz Diagram Generator Chat")

# Initialize the chat history in the session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_image"):
            st.image(message["content"])
        else:
            st.markdown(message["content"])



# Chat input for the user's topic
if prompt := st.chat_input("Enter a topic to generate a diagram"):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt, "is_image": False})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display the diagram
    with st.chat_message("assistant"):
        with st.spinner("Generating diagram..."):
            try:
                # Call your diagram generation function
                diagram_path = generate_diagram(prompt)

                if diagram_path:
                    # Display the generated image
                    st.image(diagram_path, caption=f"Diagram for '{prompt}'")
                    st.session_state.messages.append({"role": "assistant", "content": diagram_path, "is_image": True})
                else:
                    st.error("Could not generate the diagram after multiple attempts.")
                    st.session_state.messages.append({"role": "assistant", "content": "Failed to generate diagram.", "is_image": False})

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}", "is_image": False})
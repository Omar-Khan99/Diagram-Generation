# AI-Powered Diagram Generation Chat

This project provides an interactive chat application built with Streamlit that leverages large language models (LLMs) to generate explanatory diagrams. Users can input a topic into the chat, and the system will generate a structured explanation and then create a visual diagram using Graphviz. The application also supports uploading and displaying images directly in the chat.

## Features

-   **Interactive Chat Interface**: A user-friendly chat interface powered by Streamlit for a seamless experience.
-   **AI-Powered Explanations**: Leverages Google's Gemini model to generate detailed and structured explanations for any given topic.
-   **Automated Diagram Generation**: Converts the AI-generated explanations into visual diagrams using Graphviz, powered by Groq's Llama3 for code generation.
-   **Error Correction**: Includes a mechanism to attempt self-correction of the generated Graphviz code if the initial execution fails.

## Setup

To set up and run this project, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone <your-repository-url>
    cd <your-project-folder>
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4.  **Set up API Keys**:
    Create a file named `.env` in the root of your project and add your API keys:
    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    GROQ_API_KEY="YOUR_GROQ_API_KEY"
    ```
    Replace the placeholder values with your actual API keys from Google and Groq. The application will load these keys from the `.env` file.

5. **Install Graphviz**: 

   Graphviz is an open-source graph visualization software. You need to install it separately on your system. 

   - **Windows**: Download the installer from [Graphviz website](https://graphviz.org/download/).
   - **macOS**: `brew install graphviz`
   - **Linux (Debian/Ubuntu)**: `sudo apt-get install graphviz`

   After installation, ensure that the Graphviz `bin` directory is added to your system's PATH.

## Project Structure

Your project directory should look like this:

```
your-project-folder/
├── app.py                # The main Streamlit application
├── diagram_graphviz.py   # Core logic for diagram generation
├── prompts.py            # Prompts for the language models
└── .env                  # Your API keys (private)
```

## Usage

To run the chat application, navigate to your project directory in your terminal and use the following Streamlit command:

```bash
streamlit run app.py
```

This will launch the application in a new tab in your web browser.

**How to interact with the app:**

*   **Generate a Diagram**: Type a topic into the chat input box at the bottom of the screen and press Enter. The assistant will generate a diagram and display it in the chat.

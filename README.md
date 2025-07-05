# Diagram Generation Project

This project utilizes large language models (LLMs) from Google's Gemini and Groq's Llama3 to generate explanatory diagrams using Graphviz. Users can input a topic, and the system will generate a structured explanation and then create a visual diagram to represent it.

## Features

- **AI-Powered Explanations**: Leverages LLMs to generate detailed and structured explanations for any given topic.
- **Automated Diagram Generation**: Converts structured explanations into visual diagrams using Graphviz.
- **Error Correction**: Includes a mechanism to attempt self-correction of generated Graphviz code if initial execution fails.

## Setup

To set up and run this project, follow these steps:

1. **Clone the repository** (if you haven't already):

   ```bash
   git clone <your-repository-url>
   cd Diagram\ Generation
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   *Note: You will need to create a `requirements.txt` file if it doesn't exist, listing all Python packages used (e.g., `graphviz`, `langchain-groq`, `python-dotenv`, `google-generativeai`).*

4. **Set up API Keys**:

   Create a file named `API.env` in the root of your project and add your API keys:

   ```
   GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
   GROQ_API_KEY="YOUR_GROQ_API_KEY"
   ```

   Replace `"YOUR_GEMINI_API_KEY"` with your actual Google Gemini API key and `"YOUR_GROQ_API_KEY"` with your Groq API key.

5. **Install Graphviz**: 

   Graphviz is an open-source graph visualization software. You need to install it separately on your system. 

   - **Windows**: Download the installer from [Graphviz website](https://graphviz.org/download/).
   - **macOS**: `brew install graphviz`
   - **Linux (Debian/Ubuntu)**: `sudo apt-get install graphviz`

   After installation, ensure that the Graphviz `bin` directory is added to your system's PATH.

## Usage

To generate a diagram, run the `diagram_graphviz.py` script:

```bash
python diagram_graphviz.py
```

The script will then prompt you to "Enter what you want to learn:". Type your topic and press Enter. The generated diagram will be saved as a PNG file in the same directory.

Type `exit` when prompted to quit the program.

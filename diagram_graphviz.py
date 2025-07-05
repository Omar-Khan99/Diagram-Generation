from graphviz import Digraph
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from .prompt import prompt_description, prompt_fix_code, prompt_code_graphviz
import time
import re
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv("API.env")

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

GEMINI_API_KEY = "your_api_key"

# Configure the generative AI model for flashcards
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

# Initialize the LLM model
llm = ChatGroq(model="llama3-70b-8192", temperature=0)

# Input from user for the topic to explain
topic = input("Enter what you want to learn: ")


# Get the structured description from the LLM
structured_description_content = gemini_model.generate_content(f"{prompt_description}\n\nGenerate a structured explanation for: {user_query}")
structured_description_content = structured_description_content.text.strip()

#Get the Graphviz Python code from LLM
graphviz_code_response = gemini_model.generate_content(f"{prompt_code_graphviz}\n\nGenerate a structured explanation for: {structured_description_content}")
graphviz_code_response = graphviz_code_response.text.strip()

# Handle the code execution safely with isolated namespace
filename = f"diagram_{topic.replace(' ', '_')}_{int(time.time())}"
filename = sanitize_filename(filename)

try:
    exec(graphviz_code)
    print(f"✅ Diagram generated successfully: {filename}.png")
except Exception as e:
    error_message = f"{str(e)}\n\n{traceback.format_exc()}"
    print(f"❌ Initial attempt failed with error: {str(e)}")

    # Enter loop for error correction (up to 2 additional attempts)
    for i in range(2):
        # Prepare prompt to fix the code
        fix_prompt = prompt_fix_code.format(
            topic=topic,
            description=content.content,
            erroneous_code=graphviz_code,
            error_message=error_message
        )

        # Get corrected code from LLM
        fix_response = llm.invoke([SystemMessage(content=fix_prompt)])
        fixed_code = fix_response.content

        # Clean the fixed code
        if '```' in fixed_code:
            fixed_code = fixed_code.split('```')[1].strip('python\n')
        else:
            fixed_code = fixed_code.strip()

        print(f"🛠️ Attempting to fix code for retry {i+1}/2")
        graphviz_code = fixed_code  # Update code for next attempt

        try:
            exec(graphviz_code)
            print(f"✅ Diagram generated successfully: {filename}.png")
            break
        except Exception as e:
            error_message = f"{str(e)}\n\n{traceback.format_exc()}"
            print(f"❌ Attempt {i+1}/2 failed with error: {str(e)}")
            if i == 1:
                print(f"❌ All attempts failed. Could not generate diagram.")

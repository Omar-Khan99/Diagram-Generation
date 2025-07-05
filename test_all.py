import re
import subprocess
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import Tool
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_experimental.autonomous_agents.autogpt.agent import AutoGPT
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from dotenv import load_dotenv
load_dotenv("project-3\\API.env")


def create_mermaid_code(content):
    prompt_sys = f"""
    You are a Tool that works with AutoGPT to create a Mermaid code and ensure it's correct.
    Based on the content that will be given to you as input.
    Your response should only be the Mermaid code.
    Make sure to create the code without errors and follow the correct syntax.
    """

    llm = ChatGroq(model="llama3-70b-8192", temperature=0,api_key='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')
    response = llm.invoke([
    SystemMessage(content=prompt_sys),
    HumanMessage(content=content)
    ])
    response_text = response.content
    response_text = re.sub(r'\bmermaid\b', '', response.content, flags=re.IGNORECASE)

    # Save the generated Mermaid code to a file (e.g., diagram.mmd)
    with open("generated_diagram.mmd", "w") as file:
        file.write(response_text)

    return response_text

mmdc_path = "C:\\Users\\Windows 11\\AppData\\Roaming\\npm\\mmdc.cmd"  # Update this path!
def cheak_mermaid_code(path="generated_diagram.mmd"):
    # Running the mermaid-cli to generate the diagram
    result = subprocess.run(
        [mmdc_path, "-i", path, "-o", "diagram.png", "-s", "4"],
        capture_output=True, text=True
    )

    # Check for errors in the Mermaid generation
    if result.returncode != 0:
        return result.stderr.strip().split('Parser3')[0]

    return "Diagram generated successfully"

def edit_mermaid_code(inputs: dict):
    error = inputs.get("error", "")
    code = inputs.get("code", "")
    prompt_sys = f"""
    You are a Tool that works with AutoGPT to fix invalid Mermaid code.

    You will be given:
    1. An error message from Mermaid CLI.
    2. The original Mermaid code.

    Fix the code based on the error.

    ERROR:
    {error}
    """
    
    llm = ChatGroq(model="llama3-70b-8192", temperature=0,api_key='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')
    response = llm.invoke([
    SystemMessage(content=prompt_sys),
    HumanMessage(content=code)
    ])
    response_text = response.content
    response_text = re.sub(r'\bmermaid\b', '', response.content, flags=re.IGNORECASE)

    # Save the generated Mermaid code to a file (e.g., diagram.mmd)
    with open("generated_diagram.mmd", "w") as file:
        file.write(response_text)

    return response_text

# Set up the tools for AutoGPT
tools = [
    Tool(
        name="create Mermaid code",
        func=create_mermaid_code,
        description="Useful when you want to create a diagram using Mermaid code and display it",
        return_direct=True
    ),
    Tool(
        name="cheak mermaid code",
        func=cheak_mermaid_code,
        description="Useful when you want to check if the Mermaid code is correct and works",
        return_direct=True
    ),
    Tool(
        name="Edit mermaid code",
        func=edit_mermaid_code,
        description="Fix Mermaid code based on a previous error. Input must be a dictionary with 'error' and 'code' keys.",
        return_direct=True
    )
]

# Set up the memory and vector store

embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embedding_size = 384

import faiss
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embedding_function.embed_query, index, InMemoryDocstore({}), {})

# Set up the model and AutoGPT

agent = AutoGPT.from_llm_and_tools(
    ai_name="Jim",
    ai_role="Assistant",
    tools=tools,
    llm=ChatGroq(model="llama3-70b-8192", temperature=0,api_key='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'),
    memory=vectorstore.as_retriever()
)

# Set verbose to be true
agent.chain.verbose = True

# Task to generate and check Mermaid code
task = "I want to learn and understand Deep learning very will when use it in image classfication"

# Run the agent
agent.run([task])

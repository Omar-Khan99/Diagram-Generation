from graphviz import Digraph
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import time
import re

# Load environment variables from .env file
load_dotenv("API.env")

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Initialize the LLM model
llm = ChatGroq(model="llama3-70b-8192", temperature=0)

# Input from user for the topic to explain
topic = input("Enter what you want to learn: ")

# First prompt: Explanation generation
prompt_content = """
You are an expert explainer working in a multi-agent system.

Your job is to generate a clear, structured, and technically accurate description of a given topic so it can be turned into a diagram.

Requirements:
- Break down the topic into logical steps, layers, or components.
- Describe each part in order of how it flows or interacts with others.
- Focus on function, purpose, input/output, and relationships.
- Keep the explanation concise but informative — not too short, not too long.
- The description should be suitable for transforming into a technical diagram using Graphviz.

Your output must be plain text, without code or special formatting.
"""

# Get the structured description from the LLM
content = llm.invoke([SystemMessage(content=prompt_content), HumanMessage(content=topic)])

# Second prompt: Code generation based on the description
prompt_sys = """
You are an expert technical diagram assistant. Your job is to generate annotated, educational diagrams using Python's Graphviz library.

Your output should be a Python script that:
- Use `Digraph(format='png')` and set `dpi='300'` for high-quality image generation.
- Uses `graphviz.Digraph()` to create diagrams.
- Is vertical (top to bottom) using `rankdir='TB'`.
- Explains the topic clearly, with well-labeled nodes and structured flow.
- Includes **side notes** as `note`-shaped nodes connected with dashed edges for learning aid.
- Uses colors and groupings to visually separate concepts (e.g., attention, embedding, logic, output).
- Adds emoji or icons when relevant to make the diagram engaging.
- Groups components logically (e.g., encoder, decoder, steps).
- Adds short, simple labels for each node.
- Adds 1–2 sentence notes for difficult concepts (e.g., “Masked Self-Attention” or “Softmax Layer”).
Your goal is to teach students or junior developers about a complex technical subject in a clean, visual, and readable format.

🧠 The diagram should:
- Represent concepts with *friendly labels* and visual structure.
- Help someone understand the subject quickly.
- Be suitable for use in a blog post, classroom, or tech presentation.

🛠️ Your response should ONLY include the full Python code using Graphviz to render the diagram. Don't add explanations outside of the code. Make sure the final diagram is complete and renders without error.

💡 Example Topics:
- How Self-Attention Works in Transformers
- Neural Network Architecture (CNN, RNN, etc.)
- How Gradient Descent Works
- LLM Pipeline: Tokenization to Generation
- Blockchain Transaction Lifecycle

Only output working Python code using the `graphviz` library. Do not include markdown formatting or extra explanation.
---

Here is an example of the kind of Python code you should generate:

EX 1:
```python
from graphviz import Digraph

g = Digraph('Transformer', format='png')
g.attr(rankdir='TB', dpi='300', nodesep='0.7', ranksep='1.1')
g.attr('node', shape='box', style='filled,rounded', fontsize='10', fontname='Helvetica', color='#444444')

# === Color Palette ===
colors = {
    'attention': '#E6CCFF',
    'masked_attention': '#FFD6CC',
    'ff': '#D9F0FF',
    'norm': '#E2F7E1',
    'embed': '#FFE9EC',
    'pos': '#FFFFFF',
    'final': '#FFFACD',
    'label': '#F0F0F0',
    'note': '#FFFFDD'
}

# === Main Nodes ===
def styled_node(name, label, fill):
    g.node(name, label, fillcolor=fill)

styled_node('Input', '🡒 Inputs', 'white')
styled_node('InputEmbed', 'Input Embedding', colors['embed'])
styled_node('PosEnc1', 'Positional Encoding', colors['pos'])
styled_node('EncMHA', 'Multi-Head Attention', colors['attention'])
styled_node('EncNorm1', 'Add & Norm', colors['norm'])
styled_node('EncFF', 'Feed Forward', colors['ff'])
styled_node('EncNorm2', 'Add & Norm', colors['norm'])
styled_node('EncoderNx', 'Nx Encoder Blocks', colors['label'])

styled_node('Output', '🡒 Outputs (shifted right)', 'white')
styled_node('OutputEmbed', 'Output Embedding', colors['embed'])
styled_node('PosEnc2', 'Positional Encoding', colors['pos'])
styled_node('DecMaskedMHA', 'Masked\nMulti-Head Attention', colors['masked_attention'])
styled_node('DecNorm1', 'Add & Norm', colors['norm'])
styled_node('DecMHA', 'Multi-Head Attention\n(from Encoder)', colors['attention'])
styled_node('DecNorm2', 'Add & Norm', colors['norm'])
styled_node('DecFF', 'Feed Forward', colors['ff'])
styled_node('DecNorm3', 'Add & Norm', colors['norm'])
styled_node('DecoderNx', 'Nx Decoder Blocks', colors['label'])

styled_node('Linear', 'Linear', colors['final'])
styled_node('Softmax', 'Softmax', colors['final'])
styled_node('OutputProbs', '🎯 Output Probabilities', 'white')

# === Flow Edges ===
g.edge('Input', 'InputEmbed')
g.edge('InputEmbed', 'PosEnc1')
g.edge('PosEnc1', 'EncMHA')
g.edge('EncMHA', 'EncNorm1')
g.edge('EncNorm1', 'EncFF')
g.edge('EncFF', 'EncNorm2')
g.edge('EncNorm2', 'EncoderNx')

g.edge('Output', 'OutputEmbed')
g.edge('OutputEmbed', 'PosEnc2')
g.edge('PosEnc2', 'DecMaskedMHA')
g.edge('DecMaskedMHA', 'DecNorm1')
g.edge('DecNorm1', 'DecMHA')
g.edge('EncoderNx', 'DecMHA')  # Cross attention
g.edge('DecMHA', 'DecNorm2')
g.edge('DecNorm2', 'DecFF')
g.edge('DecFF', 'DecNorm3')
g.edge('DecNorm3', 'DecoderNx')

g.edge('DecoderNx', 'Linear')
g.edge('Linear', 'Softmax')
g.edge('Softmax', 'OutputProbs')

# === Subgraph Labels ===
with g.subgraph() as encoder:
    encoder.attr(rank='same')
    encoder.node('EncoderNx')
    encoder.attr(label='<<B>ENCODER</B>>', labelloc='t', style='dashed')

with g.subgraph() as decoder:
    decoder.attr(rank='same')
    decoder.node('DecoderNx')
    decoder.attr(label='<<B>DECODER</B>>', labelloc='t', style='dashed')

# === Educational Notes ===
g.attr('node', shape='note', style='filled', fillcolor=colors['note'], fontcolor='black')

g.node('NoteMHA', '🧠 Self-Attention allows each word to "look at" other words in a sentence\nto decide which ones are important for its own representation.')
g.edge('EncMHA', 'NoteMHA', style='dashed', arrowhead='none')

g.node('NoteMaskedMHA', '🚫 Masked Self-Attention prevents the decoder from "cheating" by looking at future words during training.')
g.edge('DecMaskedMHA', 'NoteMaskedMHA', style='dashed', arrowhead='none')

g.node('NoteCrossAttention', '🔄 Decoder MHA (cross-attention) focuses on the encoder\'s output.\nIt helps the decoder decide what parts of the input are relevant.')
g.edge('DecMHA', 'NoteCrossAttention', style='dashed', arrowhead='none')

g.node('NotePositionalEncoding', '📍 Since self-attention lacks order, positional encoding adds\ninformation about word positions.')
g.edge('PosEnc1', 'NotePositionalEncoding', style='dashed', arrowhead='none')

g.node('NoteNx', '♻️ The blocks are repeated Nx times (often 6). Each repetition refines\nthe representation further.')
g.edge('EncoderNx', 'NoteNx', style='dashed', arrowhead='none')

g.node('NoteSoftmax', '🎯 Final layer produces probabilities for each word in the vocabulary.')
g.edge('Softmax', 'NoteSoftmax', style='dashed', arrowhead='none')

# === Render ===
g.render('transformer_with_notes', view=True)
```

EX 2:

```python
from graphviz import Digraph

g = Digraph('Transformer', format='png')
g.attr(rankdir='TB', dpi='300', nodesep='0.7', ranksep='1.1')
g.attr('node', shape='box', style='filled,rounded', fontsize='10', fontname='Helvetica', color='#444444')

# === Color Palette ===
colors = {
    'attention': '#E6CCFF',     # lavender
    'masked_attention': '#FFD6CC',  # light peach
    'ff': '#D9F0FF',            # light blue
    'norm': '#E2F7E1',          # mint green
    'embed': '#FFE9EC',         # soft pink
    'pos': '#FFFFFF',           # white
    'final': '#FFFACD',         # lemon chiffon
    'label': '#F0F0F0'
}

# === Helper to make styled nodes ===
def styled_node(name, label, fill):
    g.node(name, label, fillcolor=fill)

# === ENCODER BLOCK ===
styled_node('Input', '🡒 Inputs', 'white')
styled_node('InputEmbed', 'Input Embedding', colors['embed'])
styled_node('PosEnc1', 'Positional Encoding', colors['pos'])
styled_node('EncMHA', 'Multi-Head Attention', colors['attention'])
styled_node('EncNorm1', 'Add & Norm', colors['norm'])
styled_node('EncFF', 'Feed Forward', colors['ff'])
styled_node('EncNorm2', 'Add & Norm', colors['norm'])
styled_node('EncoderNx', 'Nx Encoder Blocks', colors['label'])

# === DECODER BLOCK ===
styled_node('Output', '🡒 Outputs (shifted right)', 'white')
styled_node('OutputEmbed', 'Output Embedding', colors['embed'])
styled_node('PosEnc2', 'Positional Encoding', colors['pos'])
styled_node('DecMaskedMHA', 'Masked MHA', colors['masked_attention'])
styled_node('DecNorm1', 'Add & Norm', colors['norm'])
styled_node('DecMHA', 'Multi-Head Attention\n(from Encoder)', colors['attention'])
styled_node('DecNorm2', 'Add & Norm', colors['norm'])
styled_node('DecFF', 'Feed Forward', colors['ff'])
styled_node('DecNorm3', 'Add & Norm', colors['norm'])
styled_node('DecoderNx', 'Nx Decoder Blocks', colors['label'])

# === FINAL LAYERS ===
styled_node('Linear', 'Linear', colors['final'])
styled_node('Softmax', 'Softmax', colors['final'])
styled_node('OutputProbs', '🎯 Output Probabilities', 'white')

# === FLOW: Encoder ===
g.edge('Input', 'InputEmbed')
g.edge('InputEmbed', 'PosEnc1')
g.edge('PosEnc1', 'EncMHA')
g.edge('EncMHA', 'EncNorm1')
g.edge('EncNorm1', 'EncFF')
g.edge('EncFF', 'EncNorm2')
g.edge('EncNorm2', 'EncoderNx')

# === FLOW: Decoder ===
g.edge('Output', 'OutputEmbed')
g.edge('OutputEmbed', 'PosEnc2')
g.edge('PosEnc2', 'DecMaskedMHA')
g.edge('DecMaskedMHA', 'DecNorm1')
g.edge('DecNorm1', 'DecMHA')
g.edge('EncoderNx', 'DecMHA')  # Cross attention from encoder
g.edge('DecMHA', 'DecNorm2')
g.edge('DecNorm2', 'DecFF')
g.edge('DecFF', 'DecNorm3')
g.edge('DecNorm3', 'DecoderNx')

# === FINAL FLOW ===
g.edge('DecoderNx', 'Linear')
g.edge('Linear', 'Softmax')
g.edge('Softmax', 'OutputProbs')

# === GROUP LABELS ===
with g.subgraph() as encoder:
    encoder.attr(rank='same')
    encoder.node('EncoderNx')
    encoder.attr(label='<<B>ENCODER</B>>', labelloc='t', style='dashed')

with g.subgraph() as decoder:
    decoder.attr(rank='same')
    decoder.node('DecoderNx')
    decoder.attr(label='<<B>DECODER</B>>', labelloc='t', style='dashed')

# === Render ===
g.render('modern_transformer_diagram', view=True)
```
"""

#Get the Graphviz Python code from LLM
response = llm.invoke([SystemMessage(content=prompt_sys), HumanMessage(content=content.content)])

#Extract and clean the generated code
response_text = response.content
print("Generated Content:", content.content)

#Handle the code execution safely with isolated namespace
for i in range(3):
    try:
        graphviz_code = response_text.split('```')[1].strip('python\n')
        filename = f"diagram_{topic.replace(' ', '_')}_{int(time.time())}"
        filename = sanitize_filename(filename)

        # Safely execute the generated code in an isolated namespace
        exec(graphviz_code)
    except Exception as e:
        print(f"❌ Error executing generated code: {e}")

#Optionally, save the topic, description, and code to a text file for review
with open(f"{filename}.txt", "w", encoding="utf-8") as f: 
    f.write(f"## Topic: {topic}\n\n")
    f.write(f"### Description:\n{content.content}\n\n")
    f.write(f"### Code:\n{graphviz_code}")
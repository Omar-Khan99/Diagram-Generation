from graphviz import Digraph

g = Digraph('CNN', format='png')
g.attr(rankdir='TB', dpi='300', nodesep='0.7', ranksep='1.1')
g.attr('node', shape='box', style='filled,rounded', fontsize='10', fontname='Helvetica', color='#444444')

colors = {
    'convolutional': '#A0C4FF',  # Soft Blue
    'activation': '#FFD6CC',  # Light Peach
    'pooling': '#D9F0FF',  # Light Blue
    'flatten': '#E2F7E1',  # Mint Green
    'fully_connected': '#FFFACD',  # Lemon Chiffon
    'input': '#FFFFFF',  # White
    'output': '#F0F0F0'  # Light Gray
}

def styled_node(name, label, fill):
    g.node(name, label, fillcolor=fill)

styled_node('InputData', 'Input Data', colors['input'])

g.edge('InputData', 'ConvolutionalLayer')

def convolutional_layer(name):
    styled_node(name, 'Convolutional Layer', colors['convolutional'])
    g.edge(name, 'ActivationFunction')

convolutional_layer('ConvolutionalLayer')

def activation_function(name):
    styled_node(name, 'Activation Function', colors['activation'])
    g.edge(name, 'PoolingLayer')

activation_function('ActivationFunction')

def pooling_layer(name):
    styled_node(name, 'Pooling Layer', colors['pooling'])
    g.edge(name, 'FlattenLayer')

pooling_layer('PoolingLayer')

def flatten_layer(name):
    styled_node(name, 'Flatten Layer', colors['flatten'])
    g.edge(name, 'FullyConnectedLayer')

flatten_layer('FlattenLayer')

def fully_connected_layer(name):
    styled_node(name, 'Fully Connected Layer', colors['fully_connected'])
    g.edge(name, 'Output')

fully_connected_layer('FullyConnectedLayer')

styled_node('Output', 'Output', colors['output'])

g.render('cnn_diagram', view=True)
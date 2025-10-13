from bots import dumb_bot, smart_bot, whisper_bot, multimodal_bot
import bots
import os

# Run this like this: python -m bots.coordinator_graph

class CoordinatorGraph():

    def __init__(self):  
        self.graph = {}
        self.execution_order = []
    

    def add_node(self, node):
        # TODO update the graph with this node.        
        self.graph[node.name] = node
        #return self.graph[node]
        '''
        if node.bot not in self.graph:
            #self.graph = [node, []]
            self.graph(node.bot) = node.bot
        '''
        
    def add_edge(self, from_node, to_node):
        self.graph[from_node].output_edges.append(self.graph[to_node])
        self.graph[to_node].input_edges.append(self.graph[from_node])
    
    '''
    def add_input_edge(self, from_node, to_node):
        self.graph[from_node].output_edges.append(self.graph[to_node])

    def add_output_edge(self, from_node, to_node):
        self.graph[from_node].input_edges.append(self.graph[to_node])
    '''

    def topilogical_sort(self):
        visited = set()
        order = []

        def dfs(node):
            if node.bot in visited:
                return
            visited.add(node.bot)
            for output_node in node.output_edges:
                dfs(output_node)
            order.append(node)

        for node in self.graph.values():
            dfs(node)

        self.execution_order = order[::-1]  # Reverse for correct order
    def run(self, context):
        self.topilogical_sort()
        self.display_graph()
        self.display_execution_order()

        for node in self.execution_order:
            #print(f"\nContext here: {context}")
            res = node.process(node, context) 
            print(f"--- From {node.name}: \n {res} \n----")

            # Save result under node name for use by later bots
            context[node.name] = res

        return context, self.execution_order

    # ______________ Printing 

    def display_graph(self):
        print("\nGraph Connectivity (Topological Order):\n")
        for node in self.execution_order:
            outputs = [out.name for out in node.output_edges]
            print(f"{node.name} → {outputs if outputs else '[]'}")
        print("\n")

    def display_execution_order(self):
        print(f"Graph's execution order.\n")

        for node in self.execution_order:
            print(f"{node.name}")
        print("\n")
        

    # -------------- Remove -------    
    def run_dfs(self, context):
        self.display_graph()
        self.display_execution_order()

        visited = set()

        def dfs(node):
            if node.bot in visited:
                return
            visited.add(node.bot)

            # Only process if all inputs are satisfied (optional)
            result = node.process(node, context)
            print(f"\n--- From {node.name}:\n{result}\n---")

            context[node.name] = result

            for next_node in node.output_edges:
                dfs(next_node)

        # Start traversal from nodes with no inputs
        start_nodes = [node for node in self.graph.values() if not node.input_edges]
        #start_nodes = self.graph.values()

        for node in start_nodes:
            dfs(node)

        return context


class BotNode:

    def __init__(self, name, bot, method):
        self.bot = bot
        #self.name = bot.model_name
        self.name = name  # Explicit node name (e.g., "zealot", "smart")
        self.input_edges = []
        self.output_edges = []
        self.method = method

    def process(self, bot, context):
        resutlt = bot.method(context)
        return resutlt
    # Add some memory component?


def build_graph_from_config(nodes, edges):
    graph = CoordinatorGraph()

    # Add nodes with custom names
    for bot, method in nodes:
        node = BotNode(bot, method)
        graph.add_node(node)

    # Add edges by name
    for from_node, to_node in edges:
        graph.add_edge(from_node, to_node)

    return graph

def graph_setup(vision, dumb, smart, zealot):

    m = ["llava", "microsoft/DialoGPT-large", "llama3.2", "zealot"]
    graph = build_graph_from_config(
        nodes=[
            (vision, vision.reply_from_dictionary),
            (dumb, dumb.reply_from_dictionary),
            (smart, smart.reply_from_dictionary)
        ],
        edges=[
            (f"{m[1]}", f"{m[0]}"),
            (f"{m[0]}", f"{m[2]}"),
            (f"{m[1]}", f"{m[2]}")
            
            

        ]
    )
    return graph

def graph_setup_with_names(vision, dumb, smart, zealot):
    graph = build_graph_from_config_with_names(
        nodes=[
            ("vision", vision, vision.reply_from_dictionary),
            ("dumb", dumb, dumb.reply_from_dictionary),
            ("smart", smart, smart.reply_from_dictionary),
            ("zealot", zealot, zealot.reply_from_dictionary),
        ],
        edges=[
            ("vision", "smart"),
            ("dumb", "smart"),
            ("zealot", "smart"),
            ("smart", "zealot"),  # cycle
        ]
    )
    return graph

def build_graph_from_config_with_names(nodes, edges):
    graph = CoordinatorGraph()

    for name, bot, method in nodes:
        node = BotNode(name, bot, method)
        graph.add_node(node)

    for from_node, to_node in edges:
        graph.add_edge(from_node, to_node)

    return graph


def main():

    dumb = dumb_bot.Dumb_Bot("microsoft/DialoGPT-large")
    smart = bots.build_smart_bot("llama3.2", "repeater")
    zealot = bots.build_zealot_bot("llama3.2", "fanatic")
    vision = bots.build_vision_bot("llava", 1)
    #sound = bots.build_whisper_bot()

    '''
    # Build graph
    graph = CoordinatorGraph()

    # Add nodes
    graph.add_node(BotNode(vision, vision.reply_from_dictionary))
    graph.add_node(BotNode(dumb, dumb.reply_from_dictionary))
    graph.add_node(BotNode(smart, smart.reply))

    #graph.add_edge("llava", "microsoft/DialoGPT-large")
    graph.add_edge("llava", "llama3.2")
    graph.add_edge("llama3.2", "llama3.2")
    graph.add_edge("llama3.2", "microsoft/DialoGPT-large")

    graph.add_edge("microsoft/DialoGPT-large", "llama3.2") 
    '''
    graph = graph_setup_with_names(vision, dumb, smart, zealot)

    # Input context
    user_input = "Please comment on this:"
    homedir = os.getcwd()
    image_path = os.path.join(f"{homedir}","Ollama", "images", "image2.jpg")

    context = {
        "user_text": user_input,
        "image": image_path
    }

    # Run the graph
    result, order = graph.run(context)
    #print(f"\n\nFINAL RESULT: {result}")
    print(result[order[-1].name])  # Final smart reasoning output

if __name__ == "__main__":
    main()
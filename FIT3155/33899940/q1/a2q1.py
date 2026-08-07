import sys

class SuffixTreeNode:
    def __init__(self, start, end, node_id):
        self.children = {} # Key: Character representing the edge label.
        self.suffix_link = None  
        self.start = start  # Start index of the substring represented by the edge leading to this node
        self.end = end      # End index of the substring represented by the edge leading to this node (list form to be mutable)
        self.suffix_index = -1  # Index of the suffix represented by the path from root to this node // -1 indicates that the node is an internal node
        self.node_id = node_id      # for run Log

# Helper function to calculate edge length for a given node -> child O(1)
def edge_length(node):
    return node.end[0] - node.start + 1

def construct_index_based_tree(text, log_file):
    text = text + '$'
    n = len(text)
    node_counter = [1]          # Incremental node count for run log

    # HELPER FUNCTION to create new nodes and keep track of node_counter for run log
    def new_node(start, end):
        node = SuffixTreeNode(start, end, node_counter[0])
        node_counter[0] += 1
        return node
    
    root = new_node(-1, [-1])     # Construct I_1 
    root.suffix_link = root
    print(f"Root Node {root.node_id}", file=log_file)

    # Variable intilasation 
    global_end = [-1] # (Rule 1 Optimization)
    lastj = 0
    current_node = root         #The last resolved internal node
    current_edge = -1           #txt index of character that is being currently being traversed (by cur_node)
    remainder = 0               # num of characters traversed down that current edge

    # PHASE i
    for i in range(n):
        global_end[0] = i           # Rule 1
        lastj += 1
        last_new_node = None        # Initialize last_new_node at the start of each phase ( suffix link )
        print(f"Phase {i + 1} starts from Extn {i - lastj + 2}", file=log_file)

        while lastj > 0:
            if remainder == 0:         # If we are at a node we now need to look for the edge to go to
                current_edge = i
            start_char = text[current_edge]    

            active_id = current_node.node_id
            link_id   = current_node.suffix_link.node_id
            if remainder == 0:
                rem_str = "EMPTY"
            else:
                rem_str = f"S[{current_edge + 1}...{current_edge + remainder}]"
            # Extension number: suffix whose start = i - lastj + 1 
            extn_num = i - lastj + 2

            if start_char not in current_node.children:  # No outgoing edge // destination node found
                print(f"    Extn {extn_num} applies Rule 2 (alternate)", file=log_file)
                print(f"    Active Node = Node {active_id} "
                      f"(suffix link to Node {link_id}); Remainder = {rem_str}", file=log_file)
 
                # RULE 2 (Standard insert): No outgoing edge starts with the required character 
                # So Create a new leaf node and append it to the current node.
                new_leaf = new_node(i, global_end)
                new_leaf.suffix_index = i - lastj + 1
                current_node.children[start_char] = new_leaf
                print(f"        Node {new_leaf.node_id} created: Leaf node!", file=log_file)
                

                # Resolve suffix link to the existing current_node
                if last_new_node is not None:
                    last_new_node.suffix_link = current_node
                    print(f"        Linking Node {last_new_node.node_id} "
                          f"to Node {current_node.node_id}", file=log_file)
                    last_new_node = None
                current_node = current_node.suffix_link 
                lastj -= 1      # New leaf created, can skip subsequent extensions

            # RULE 3: The suffix already implicitly exists in the tree 
            # Resolve suffix link to the existing current_node
            else:                                 
                child = current_node.children[start_char]
                edge_len = edge_length(child)

                if remainder >= edge_len:                                
                        current_edge += edge_len
                        remainder -= edge_len
                        current_node = child
                        continue
                
                tree_char = text[child.start + remainder]               # Character currently at the active point mid-edge
                new_char = text[i]                                      # we need to start at txt[i]

                if tree_char == new_char:                                # Rule 3 again, we know its an implict match
                    print(f"    Extn {extn_num} applies Rule 3", file=log_file)
                    print(f"    Active Node = Node {active_id} "
                          f"(suffix link to Node {link_id}); Remainder = {rem_str}", file=log_file)
                    if last_new_node is not None:
                        last_new_node.suffix_link = current_node
                        print(f"        Linking Node {last_new_node.node_id} "
                              f"to Node {current_node.node_id}", file=log_file)
                        last_new_node = None
                    remainder += 1    
                    break    # Extension complete // Show stopper again   
                else:                                           
                # RULE 2 (Edge Split): Mismatch between the edge and current_suffix 
                    print(f"    Extn {extn_num} applies Rule 2 (regular)", file=log_file)
                    print(f"    Active Node = Node {active_id} "
                          f"(suffix link to Node {link_id}); Remainder = {rem_str}", file=log_file)                
                    split_end = [child.start + remainder -1]                  
                    split_node = new_node(child.start, split_end)                    # Create an internal node // end is fixed
                    print(f"        Node {split_node.node_id} created: Internal node!", file=log_file)
                    current_node.children[start_char] = split_node                # Attach split node to the current node

                    child.start += remainder                              # Adjust existing child's start index and attach to split node
                    split_node.children[text[child.start]] = child

                    new_leaf = new_node(i, global_end)              # Create new leaf for the divergent character and attach
                    split_node.children[new_char] = new_leaf        # Attach new leaf to split node
                    new_leaf.suffix_index = i - lastj + 1
                    print(f"        Node {new_leaf.node_id} created: Leaf node!", file=log_file)

                    # Establish link from previously created node to this new split_node
                    if last_new_node is not None:
                        last_new_node.suffix_link = split_node
                        print(f"        Linking Node {last_new_node.node_id} "
                              f"to Node {split_node.node_id}", file=log_file)
                    last_new_node = split_node
                    # State transition for the next extension
                    if current_node == root:
                        remainder -= 1
                        current_edge = i - remainder
                    else:
                        current_node = current_node.suffix_link 
                    lastj -= 1  # Extension complete
                            
    return root

def extract_lcp(root, n):
    lcp = [0] * n
    leaf_count = [0]  # Tracks the implicit lexicographical index

    def dfs(node, string_depth):
        
        # Base Case: Leaf Node
        if not node.children:
            leaf_count[0] += 1
            return

        # Sort keys for lexicographical traversal
        sorted_keys = sorted(node.children.keys())
        is_first_child = True

        for key in sorted_keys:
            child = node.children[key]
            
            # The transition between adjacent subtrees represents the lowest common node of the 
            # last visited leaf (leaf_count - 1) and the next visited leaf (leaf_count)
            if not is_first_child:
                lcp[leaf_count[0]] = string_depth
            
            # Calculate string depth for the recursive call
            child_edge_len = edge_length(child)
            
            dfs(child, string_depth + child_edge_len)
            
            is_first_child = False

    # Initiate DFS from the root with a string depth of 0
    dfs(root, 0)
    
    return lcp


if __name__ == '__main__':
        
    with open(sys.argv[1], 'r') as f:
        text = f.readline().strip()

    # Open the run log file and pass it to the tree constructor
    with open("runlog_a2q1.txt", "w") as log_file:
        root = construct_index_based_tree(text, log_file)

    # Execution on the constructed tree
    # construct_index_based_tree implicitly appends '$', so length is len(text) + 1
    N = len(text) + 1
    lcp = extract_lcp(root, N)

    # Write out the LCP array 
    with open("output_a2q1.txt", 'w') as out_file:
        for val in lcp:
            out_file.write(str(val) + "\n")


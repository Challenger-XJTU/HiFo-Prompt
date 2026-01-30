
class GetPrompts():
    def __init__(self):
        self.prompt_task = "Given a set of nodes with their coordinates, \
you need to find the shortest route that visits each node once and returns to the starting node. \
The task can be solved step-by-step by starting from the current node and iteratively choosing the next node. \
Design a sophisticated node selection strategy that considers: \
1) Candidate sets - maintain a limited set of promising neighbors for each node rather than considering all neighbors \
2) Look-ahead evaluation - assess potential future moves beyond just the immediate connection \
3) Minimum spanning tree properties - consider how your edges might relate to a global minimum spanning tree \
4) Edge cost normalization - evaluate edge costs in relation to their global context \
5) Path momentum and direction - consider the current trajectory when selecting next nodes \
6) Nearest neighbor clusters - identify and leverage clustered regions of nodes intelligently \
7) Monte Carlo Tree Search (MCTS) inspired selection - consider how principles from MCTS could guide node choice. This might involve a lightweight simulation of several potential path continuations from candidate next nodes, using the outcomes of these simulations (e.g., estimated quality of the partial tours, likelihood of achieving a good overall tour) to score and select the most promising immediate next node. The goal is to use MCTS-like statistical reasoning rather than a full MCTS implementation. \
8) Beam Search guided path exploration - employ a beam search-like mechanism by maintaining a limited set (the 'beam width') of the most promising diverse partial paths at each construction step. The selection of the next node should be influenced by its ability to extend these leading partial paths towards high-quality complete tours, allowing for a focused yet multi-faceted exploration of the search space. \
"

        self.prompt_func_name = "select_next_node"
        self.prompt_func_inputs = ["current_node","destination_node","univisited_nodes","distance_matrix"]
        self.prompt_func_outputs = ["next_node"]
        self.prompt_inout_inf = "'current_node', 'destination_node', 'next_node', and 'unvisited_nodes' are node IDs. 'distance_matrix' is the distance matrix of nodes."
        self.prompt_other_inf = "All are Numpy arrays."

    def get_task(self):
        return self.prompt_task
    
    def get_func_name(self):
        return self.prompt_func_name
    
    def get_func_inputs(self):
        return self.prompt_func_inputs
    
    def get_func_outputs(self):
        return self.prompt_func_outputs
    
    def get_inout_inf(self):
        return self.prompt_inout_inf

    def get_other_inf(self):
        return self.prompt_other_inf

if __name__ == "__main__":
    getprompts = GetPrompts()
    print(getprompts.get_task())

class GetPrompts():
    def __init__(self):
        self.prompt_task = "Given a sequence of items and a set of identical bins with a fixed capacity, \
you need to assign each item to a bin to minimize the total number of bins used. \
The task can be solved step-by-step by taking the next item and deciding which bin to place it in based on a score. \
"
        self.prompt_func_name = "score"
        self.prompt_func_inputs = ['item', 'bins']
        self.prompt_func_outputs = ['scores']
        self.prompt_inout_inf = "'item' and 'bins' are the size of current item and the rest capacities of feasible bins, which are larger than the item size. \
The output named 'scores' is the scores for the bins for assignment. "
        self.prompt_other_inf = "Note that 'item' is of type int, while 'bins' and 'scores' are both Numpy arrays. The novel function should be sufficiently complex in order to achieve better performance. It is important to ensure self-consistency."
#Include the following imports at the beginning of the code: 'import numpy as np', and 'from numba import jit'. Place '@jit(nopython=True)' just above the 'priority' function definition."

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


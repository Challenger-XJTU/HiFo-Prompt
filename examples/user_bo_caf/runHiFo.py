from hifo import hifo
from hifo.utils.getParas import Paras
from prob import Evaluation

# Parameter initilization #
paras = Paras() 

# Set your local problem
problem_local = Evaluation()

# Set parameters #
paras.set_paras(method = "hifo",    # ['ael','hifo']
                problem = problem_local, # Set local problem, else use default problems
                llm_api_endpoint = "http://xxx/completions", # set your LLM endpoint
                llm_api_key = "xxxxx",   # set your key
                llm_model = "xxxxx",
                ec_pop_size = 8, # number of samples in each population
                ec_n_pop = 4,  # number of populations
                exp_n_proc = 1,  # multi-core parallel
                exp_debug_mode = False,
                eva_numba_decorator = False)

# initilization
evolution = hifo.EVOL(paras)

# run 
evolution.run()
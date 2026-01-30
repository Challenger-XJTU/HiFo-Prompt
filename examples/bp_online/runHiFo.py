from hifo import hifo
from hifo.utils.getParas import Paras

# Parameter initilization #
paras = Paras() 

# Set parameters #
paras.set_paras(method = "hifo",    # ['ael','hifo']
                problem = "bp_online", #['tsp_construct','bp_online']
                llm_api_endpoint = "http://xxx/completions", # set your LLM endpoint
                llm_api_key = "xxxxxxxx",   # set your key
                llm_model = "xxxxxxxx",
                ec_pop_size = 8, # number of samples in each population
                ec_n_pop = 8,  # number of populations
                exp_n_proc = 4,  # multi-core parallel
                exp_debug_mode = False)
# initilization
evolution = hifo.EVOL(paras)

# run 
evolution.run()
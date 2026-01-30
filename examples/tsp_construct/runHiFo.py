from hifo import hifo
from hifo.utils.getParas import Paras

# Parameter initilization #
paras = Paras() 

# Set parameters #
paras.set_paras(method = "hifo",    # ['ael','hifo']
                problem = "tsp_construct", #['tsp_construct','bp_online']
                llm_api_endpoint = "http://xxx/completions", # set your LLM endpoint
                llm_api_key = "xxxxx",   # set your key
                llm_model = "xxxxx",
                ec_pop_size = 8, # number of samples in each population
                ec_n_pop = 8,  # number of populations
                exp_n_proc = 4,  # multi-core parallel
                exp_debug_mode = False)

# initilization
evolution = hifo.EVOL(paras)
# run 
evolution.run()
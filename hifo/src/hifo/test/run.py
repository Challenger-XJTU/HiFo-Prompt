### Test Only ###
# Set system path
import sys
import os
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(ABS_PATH, "..", "..")
sys.path.append(ROOT_PATH)  # This is for finding all the modules
sys.path.append(ABS_PATH)
print(ABS_PATH)
from hifo import hifo
from hifo.utils.getParas import Paras
# from evol.utils.createReport import ReportCreator
# 

# Parameter initilization #
paras = Paras() 

# Set parameters #
paras.set_paras(method = "hifo",    
                ec_operators  = ['e1','e2','m1','m2','m3'], # operators in HiFo
                problem = "bp_online", # ['tsp_construct','bp_online','tsp_gls','fssp_gls']
                llm_api_endpoint = "XXX", # set endpoint
                llm_api_key = "XXX",   # set your key
                llm_model = "XXX", # set llm
                ec_pop_size = 4,
                ec_n_pop = 2,
                exp_n_proc = 4,
                exp_debug_mode = False)

# HiFo initilization
evolution = hifo.EVOL(paras)

# run HiFo
evolution.run()

# Generate HiFo Report
# RC = ReportCreator(paras)
# RC.generate_doc_report()





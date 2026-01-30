import numpy as np
import json
import random
import time

from .hifo_interface_EC import InterfaceEC

class HiFo:

    def __init__(self, paras, problem, select, manage, **kwargs):
        self.prob = problem
        self.select = select
        self.manage = manage
        
        self.use_local_llm = paras.llm_use_local
        self.llm_local_url = paras.llm_local_url
        self.api_endpoint = paras.llm_api_endpoint
        self.api_key = paras.llm_api_key
        self.llm_model = paras.llm_model

        self.pop_size = paras.ec_pop_size
        self.n_pop = paras.ec_n_pop

        self.operators = paras.ec_operators
        self.operator_weights = paras.ec_operator_weights
        if paras.ec_m > self.pop_size or paras.ec_m == 1:
            print("m should not be larger than pop size or smaller than 2, adjust it to m=2")
            paras.ec_m = 2
        self.m = paras.ec_m

        self.debug_mode = paras.exp_debug_mode
        self.ndelay = 1

        self.use_seed = paras.exp_use_seed
        self.seed_path = paras.exp_seed_path
        self.load_pop = paras.exp_use_continue
        self.load_pop_path = paras.exp_continue_path
        self.load_pop_id = paras.exp_continue_id

        self.output_path = paras.exp_output_path
        self.exp_n_proc = paras.exp_n_proc
        self.timeout = paras.eva_timeout
        self.use_numba = paras.eva_numba_decorator

        self.use_hifo_prompt = kwargs.get('use_hifo_prompt', True)
        
        print("- HiFo parameters loaded -")
        
        if self.use_hifo_prompt:
            self.hifo_prompt_log_path = self.output_path + "/results/hifo_prompt_log.json"
            print("- HiFo-Prompt enabled: Insight pool and Evolutionary Navigator will guide the evolution -")

        random.seed(2024)

    def add2pop(self, population, offspring):
        for off in offspring:
            for ind in population:
                if ind['objective'] == off['objective']:
                    if (self.debug_mode):
                        print("duplicated result, retrying ... ")
            population.append(off)

    def run(self):
        print("- Evolution Start -")
        time_start = time.time()

        interface_prob = self.prob

        interface_ec = InterfaceEC(
            self.pop_size, self.m, self.api_endpoint, self.api_key, self.llm_model, 
            self.use_local_llm, self.llm_local_url, self.debug_mode, interface_prob, 
            select=self.select, n_p=self.exp_n_proc, timeout=self.timeout, use_numba=self.use_numba
        )

        population = []
        if self.use_seed:
            with open(self.seed_path) as file:
                data = json.load(file)
            population = interface_ec.population_generation_seed(data, self.exp_n_proc)
            filename = self.output_path + "/results/pops/population_generation_0.json"
            with open(filename, 'w') as f:
                json.dump(population, f, indent=5)
            n_start = 0
        else:
            if self.load_pop:
                print("load initial population from " + self.load_pop_path)
                with open(self.load_pop_path) as file:
                    data = json.load(file)
                for individual in data:
                    population.append(individual)
                print("initial population has been loaded!")
                n_start = self.load_pop_id
            else:
                print("creating initial population:")
                population = interface_ec.population_generation()
                population = self.manage.population_management(population, self.pop_size)
                
                print(f"Pop initial: ")
                for off in population:
                    print(" Obj: ", off['objective'], end="|")
                print()
                print("initial population has been created!")
                filename = self.output_path + "/results/pops/population_generation_0.json"
                with open(filename, 'w') as f:
                    json.dump(population, f, indent=5)
                n_start = 0

        hifo_prompt_logs = []
        n_op = len(self.operators)

        for pop in range(n_start, self.n_pop):
            for i in range(n_op):
                op = self.operators[i]
                print(f" OP: {op}, [{i + 1} / {n_op}] ", end="|") 
                op_w = self.operator_weights[i]
                if (np.random.rand() < op_w):
                    parents, offsprings = interface_ec.get_algorithm(population, op)
                self.add2pop(population, offsprings)
                for off in offsprings:
                    print(" Obj: ", off['objective'], end="|")
                size_act = min(len(population), self.pop_size)
                population = self.manage.population_management(population, size_act)
                print()

            filename = self.output_path + "/results/pops/population_generation_" + str(pop + 1) + ".json"
            with open(filename, 'w') as f:
                json.dump(population, f, indent=5)

            filename = self.output_path + "/results/pops_best/population_generation_" + str(pop + 1) + ".json"
            with open(filename, 'w') as f:
                json.dump(population[0], f, indent=5)

            if self.use_hifo_prompt:
                hifo_prompt_log = {
                    "generation": pop + 1,
                    "timestamp": time.time(),
                    "best_fitness": population[0]["objective"] if population else None,
                    "diversity": interface_ec.diversity_history[-1] if interface_ec.diversity_history else None,
                    "current_insight_count": len(interface_ec.insight_pool.tips),
                    "recent_insights": list(interface_ec.insight_pool.tips)[-3:] if interface_ec.insight_pool.tips else [],
                    "navigator_guidance": interface_ec.navigator.last_guidance
                }
                hifo_prompt_logs.append(hifo_prompt_log)
                
                if (pop + 1) % 5 == 0 or pop + 1 == self.n_pop:
                    with open(self.hifo_prompt_log_path, 'w') as f:
                        json.dump(hifo_prompt_logs, f, indent=4)

            print(f"--- {pop + 1} of {self.n_pop} populations finished. Time Cost: {((time.time()-time_start)/60):.1f} m")
            print("Pop Objs: ", end=" ")
            for i in range(len(population)):
                print(str(population[i]['objective']) + " ", end="")
            print()

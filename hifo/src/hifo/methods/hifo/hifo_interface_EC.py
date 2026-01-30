import numpy as np
import time
from .hifo_evolution import Evolution
import warnings
from joblib import Parallel, delayed
from .evaluator_accelerate import add_numba_decorator
import re
import concurrent.futures

class InterfaceEC():
    def __init__(self, pop_size, m, api_endpoint, api_key, llm_model, llm_use_local, llm_local_url, 
                 debug_mode, interface_prob, select, n_p, timeout, use_numba, **kwargs):
        self.pop_size = pop_size
        self.interface_eval = interface_prob
        prompts = interface_prob.prompts
        self.evol = Evolution(api_endpoint, api_key, llm_model, llm_use_local, llm_local_url, debug_mode, prompts, **kwargs)
        self.m = m
        self.debug = debug_mode

        if not self.debug:
            warnings.filterwarnings("ignore")

        self.select = select
        self.n_p = n_p
        self.timeout = timeout
        self.use_numba = use_numba
        
        from .insight_pool import InsightPool
        from .evolutionary_navigator import EvolutionaryNavigator
        
        self.insight_pool = InsightPool(max_size=30)
        self.navigator = EvolutionaryNavigator()
        
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.diversity_history = []
        self.insight_feedback_buffer = []
        
    def code2file(self, code):
        with open("./ael_alg.py", "w") as file:
            file.write(code)
        return 
    
    def add2pop(self, population, offspring):
        for ind in population:
            if ind['objective'] == offspring['objective']:
                if self.debug:
                    print("duplicated result, retrying ... ")
                return False
        population.append(offspring)
        return True
    
    def check_duplicate(self, population, code):
        for ind in population:
            if code == ind['code']:
                return True
        return False

    def population_generation(self):
        n_create = 2
        population = []
        for i in range(n_create):
            _, pop = self.get_algorithm([], 'i1')
            for p in pop:
                population.append(p)
        return population
    
    def population_generation_seed(self, seeds, n_p):
        population = []
        fitness = Parallel(n_jobs=n_p)(delayed(self.interface_eval.evaluate)(seed['code']) for seed in seeds)

        for i in range(len(seeds)):
            try:
                seed_alg = {
                    'algorithm': seeds[i]['algorithm'],
                    'code': seeds[i]['code'],
                    'objective': None,
                    'other_inf': None
                }
                obj = np.array(fitness[i])
                seed_alg['objective'] = np.round(obj, 5)
                population.append(seed_alg)
            except Exception as e:
                print("Error in seed algorithm")
                exit()

        print("Initiliazation finished! Get " + str(len(seeds)) + " seed algorithms")
        return population
    
    def calculate_insight_effectiveness(self, offspring, population):
        if offspring['objective'] is None:
            return -0.5

        if not population:
            return 0.0
        
        valid_fitnesses = [ind['objective'] for ind in population if ind['objective'] is not None]
        if not valid_fitnesses:
            return 0.0
        
        offspring_fitness = offspring['objective']
        population_best = min(valid_fitnesses)
        population_worst = max(valid_fitnesses)
        population_avg = sum(valid_fitnesses) / len(valid_fitnesses)
        
        if population_worst == population_best:
            return 0.1
        
        normalized_performance = (population_worst - offspring_fitness) / (population_worst - population_best)
        
        if offspring_fitness <= population_best:
            effectiveness = 0.8 + 0.2 * normalized_performance
        elif offspring_fitness <= population_avg:
            effectiveness = 0.2 + 0.6 * normalized_performance
        else:
            effectiveness = -0.3 + 0.5 * normalized_performance
            
        return max(-1.0, min(1.0, effectiveness))
    
    def update_insight_feedback(self, offspring, population):
        if 'metadata' not in offspring or 'insights' not in offspring['metadata']:
            return
        
        insights = offspring['metadata']['insights']
        if not insights:
            return
        
        effectiveness = self.calculate_insight_effectiveness(offspring, population)
        
        for tip in insights:
            self.insight_pool.update_tip_stats(tip, effectiveness)
            
        if self.debug:
            print(f"Updated insight feedback - effectiveness: {effectiveness:.3f}, insights count: {len(insights)}")

    def _get_alg(self, pop, operator):
        regime, design_directive = self.navigator.get_guidance(
            pop=pop,
            best_fitness_history=self.best_fitness_history,
            avg_fitness_history=self.avg_fitness_history,
            diversity_history=self.diversity_history
        )
        
        insights = self.insight_pool.get_tips(k=3)
        
        offspring = {
            'algorithm': None,
            'code': None,
            'objective': None,
            'other_inf': None,
            'metadata': {
                'operator': operator,
                'insights': insights,
                'design_directive': design_directive,
                'regime': regime,
                'timestamp': time.time()
            }
        }
        
        if operator == "i1":
            parents = None
            [offspring['code'], offspring['algorithm']] = self.evol.i1(insights, design_directive, regime)
        elif operator == "e1":
            parents = self.select.parent_selection(pop, self.m)
            [offspring['code'], offspring['algorithm']] = self.evol.e1(parents, insights, design_directive, regime)
        elif operator == "e2":
            parents = self.select.parent_selection(pop, self.m)
            [offspring['code'], offspring['algorithm']] = self.evol.e2(parents, insights, design_directive, regime)
        elif operator == "m1":
            parents = self.select.parent_selection(pop, 1)
            [offspring['code'], offspring['algorithm']] = self.evol.m1(parents[0], insights, design_directive, regime)
        elif operator == "m2":
            parents = self.select.parent_selection(pop, 1)
            [offspring['code'], offspring['algorithm']] = self.evol.m2(parents[0], insights, design_directive, regime)
        elif operator == "m3":
            parents = self.select.parent_selection(pop, 1)
            [offspring['code'], offspring['algorithm']] = self.evol.m3(parents[0], insights, design_directive, regime)
        else:
            print(f"Evolution operator [{operator}] has not been implemented!")

        return parents, offspring

    def get_offspring(self, pop, operator):
        try:
            p, offspring = self._get_alg(pop, operator)
            
            if self.use_numba:
                pattern = r"def\s+(\w+)\s*\(.*\):"
                match = re.search(pattern, offspring['code'])
                function_name = match.group(1)
                code = add_numba_decorator(program=offspring['code'], function_name=function_name)
            else:
                code = offspring['code']

            n_retry = 1
            while self.check_duplicate(pop, offspring['code']):
                n_retry += 1
                if self.debug:
                    print("duplicated code, wait 1 second and retrying ... ")
                    
                p, offspring = self._get_alg(pop, operator)

                if self.use_numba:
                    pattern = r"def\s+(\w+)\s*\(.*\):"
                    match = re.search(pattern, offspring['code'])
                    function_name = match.group(1)
                    code = add_numba_decorator(program=offspring['code'], function_name=function_name)
                else:
                    code = offspring['code']
                    
                if n_retry > 1:
                    break
                
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.interface_eval.evaluate, code)
                fitness = future.result(timeout=self.timeout)
                offspring['objective'] = np.round(fitness, 5)
                future.cancel()
                
            self.update_insight_feedback(offspring, pop)

        except Exception as e:
            offspring = {
                'algorithm': None,
                'code': None,
                'objective': None,
                'other_inf': None
            }
            p = None
            
            if 'metadata' in offspring and 'insights' in offspring['metadata']:
                insights = offspring['metadata']['insights']
                for tip in insights:
                    self.insight_pool.update_tip_stats(tip, -0.8)

        return p, offspring

    def get_algorithm(self, pop, operator):
        self.insight_pool.update_generation(len(self.best_fitness_history))
        
        results = []
        try:
            results = Parallel(n_jobs=self.n_p, timeout=self.timeout+15)(
                delayed(self.get_offspring)(pop, operator) for _ in range(self.pop_size)
            )
        except Exception as e:
            if self.debug:
                print(f"Error: {e}")
            print("Parallel time out .")
            
        time.sleep(2)

        out_p = []
        out_off = []

        for p, off in results:
            out_p.append(p)
            out_off.append(off)
            if self.debug:
                print(f">>> check offsprings: \n {off}")
        
        if pop and len(pop) > 0:
            self.update_population_metrics(pop)
            if np.random.random() < 0.8:
                self.extract_insights_from_population(pop)
        
        return out_p, out_off
        
    def update_population_metrics(self, pop):
        if not pop:
            return
            
        valid_fitnesses = [ind['objective'] for ind in pop if ind['objective'] is not None]
        if valid_fitnesses:
            best_fitness = min(valid_fitnesses)
            avg_fitness = sum(valid_fitnesses) / len(valid_fitnesses)
            
            self.best_fitness_history.append(best_fitness)
            self.avg_fitness_history.append(avg_fitness)
            
            max_history = 50
            if len(self.best_fitness_history) > max_history:
                self.best_fitness_history = self.best_fitness_history[-max_history:]
                self.avg_fitness_history = self.avg_fitness_history[-max_history:]

        if len(pop) >= 2:
            diversity = 0
            for i in range(len(pop)):
                for j in range(i+1, len(pop)):
                    if pop[i]['algorithm'] != pop[j]['algorithm']:
                        diversity += 1
            diversity = diversity / (len(pop) * (len(pop) - 1) / 2)
            self.diversity_history.append(diversity)
            
            if len(self.diversity_history) > max_history:
                self.diversity_history = self.diversity_history[-max_history:]
    
    def extract_insights_from_population(self, pop):
        if not pop or len(pop) < 3:
            return
            
        sorted_pop = sorted(pop, key=lambda x: x['objective'] if x['objective'] is not None else float('inf'))
        top_individuals = sorted_pop[:max(1, int(len(sorted_pop) * 0.3))]
        
        prompt = "The following are core descriptions of high-performance optimization algorithms evolved recently:\n"
        
        for i, ind in enumerate(top_individuals):
            description = ind.get('algorithm', '').strip()
    
            if description and len(description) > 8:
                content_to_analyze = f"{description}"
            else:
                code_to_analyze = ind.get('code', '')
                if len(code_to_analyze) > 1000:
                    code_to_analyze = code_to_analyze[:800] + "...\n# (truncated for brevity)"
                content_to_analyze = f"{code_to_analyze}"
            prompt += f"{i+1}. Algorithm: {content_to_analyze}\n"
        
        prompt += "\nPlease extract 1-2 concise, generic, and performance-positive [design principles] or [effective patterns] from the above algorithms."
        prompt += "\nThese principles should be applicable to various combinatorial optimization problems, not just the specific problem domain."
        prompt += "\nWhen formulating these principles, it is essential to draw insights from *both* the conceptual natural language descriptions *and* their corresponding code implementations. Focus on identifying the underlying strategic design choices and algorithmic methodologies rather than superficial characteristics or specific implementation minutiae."
        prompt += "\nEach principle/pattern should be expressed as an independent sentence in the following format:"
        prompt += "\n- Balance local optimization with global solution structure when making decisions."
        prompt += "\n- Prioritize choices that maintain flexibility for future decision-making steps."
        prompt += "\n- Implement adaptive mechanisms that respond to problem instance characteristics."
        
        try:
            response = self.evol.interface_llm.get_response(prompt)
            
            insight_items = []
            for line in response.split('\n'):
                if line.strip().startswith('-'):
                    insight_items.append(line.strip()[2:].strip())
            
            for item in insight_items:
                if item and len(item) > 10:
                    self.insight_pool.add_tip(item, tags=["extracted", "high_performance"])
                    
            if self.debug:
                print(f"Extracted {len(insight_items)} insight items: {insight_items}")
        except Exception as e:
            if self.debug:
                print(f"Failed to extract insights: {e}")

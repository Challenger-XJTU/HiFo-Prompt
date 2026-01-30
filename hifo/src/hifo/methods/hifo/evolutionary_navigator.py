import numpy as np
import random

class EvolutionaryNavigator:
    
    def __init__(self):
        self.stagnation_count = 0
        self.improvement_count = 0
        self.last_best_fitness = None
        self.last_guidance = None
        self.learning_rate = 0.1

        self.regimes = [
            "exploration",
            "exploitation",
            "balanced"
        ]
        
        self.design_directives = {
            "general": [
                "optimizing objective function evaluation criteria",
                "considering long-term impact of current decisions",
                "balancing local optimality with global search strategies", 
                "improving algorithm robustness across different problem instances",
                "managing computational complexity and time efficiency"
            ],
            "exploitation": [
                "refining core evaluation and scoring functions",
                "fine-tuning critical algorithm parameters and thresholds",
                "optimizing established successful strategies and patterns",
                "reducing unnecessary computational overhead and redundancy",
                "improving precision of existing heuristics and rules"
            ],
            "exploration": [
                "exploring novel solution construction methodologies",
                "investigating alternative problem decomposition approaches", 
                "introducing new randomization or adaptive mechanisms",
                "considering completely different algorithmic paradigms",
                "experimenting with hybrid strategy combinations"
            ]
        }
    
    def get_guidance(self, pop=None, best_fitness_history=None, avg_fitness_history=None, diversity_history=None):
        regime = "balanced"
        design_directive = random.choice(self.design_directives["general"])
       
        if not best_fitness_history or len(best_fitness_history) < 2:
            return regime, design_directive
        
        current_best = best_fitness_history[-1]
        if self.last_best_fitness is not None:
            improvement = self.last_best_fitness - current_best
            
            if improvement <= 1e-4:
                self.stagnation_count += 1
                self.improvement_count = 0
            else:
                self.improvement_count += 1
                self.stagnation_count = 0
        
        self.last_best_fitness = current_best
        
        low_diversity = False
        if diversity_history and len(diversity_history) > 0:
            if diversity_history[-1] < 0.3:
                low_diversity = True
        
        if self.stagnation_count >= 3:
            regime = "exploration"
            design_directive = random.choice(self.design_directives["exploration"])
            
        elif low_diversity:
            regime = "exploration"
            design_directive = random.choice(self.design_directives["exploration"])
            
        elif self.improvement_count >= 2:
            regime = "exploitation"
            design_directive = random.choice(self.design_directives["exploitation"])
            
        else:
            weights = [0.25, 0.25, 0.5]
            regime = random.choices(self.regimes, weights=weights, k=1)[0]
            
            if regime == "exploration":
                design_directive = random.choice(self.design_directives["exploration"])
            elif regime == "exploitation":
                design_directive = random.choice(self.design_directives["exploitation"])
            else:
                directive_pool = (self.design_directives["general"] + 
                                  self.design_directives["exploitation"] + 
                                  self.design_directives["exploration"])
                design_directive = random.choice(directive_pool)
        
        self.last_guidance = (regime, design_directive)
        
        return regime, design_directive

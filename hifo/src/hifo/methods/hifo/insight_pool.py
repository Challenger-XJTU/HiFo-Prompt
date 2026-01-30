import time
import random
import math
from collections import deque

class InsightPool:
    
    
    def __init__(self, max_size=30, initial_tips=None):

        self.max_size = max_size
        self.tips = deque(maxlen=max_size)
        self.tip_stats = {}  # record statistics for each tip
        self.current_generation = 0  # current generation number
        
        # initial tips
        default_initial_tips = [
            "Design adaptive hybrid meta-heuristics synergistically fusing multiple search paradigms and dynamically tune operator parameters based on search stage or problem features",
            "Employ machine learning or pattern recognition to mine deep problem structures and optimal solution patterns then use learned insights to intelligently bias towards promising search regions or constructive choices", 
            "Explore objective function engineering by introducing auxiliary or surrogate objectives or by dynamically adjusting weights to reshape the search landscape aiding escape from local optima or guiding diverse exploration",
            "Construct problem specialized efficient solution representations and co design dedicated core operators to fully leverage representation structure for powerful solution space exploration",
            "Implement intelligent diversification and restart strategies based on solution feature space analysis systematically targeting uncovered feature regions to promote global search coverage and escape deep local optima",
        ]
        
        if initial_tips:
            for tip in initial_tips:
                self.add_tip(tip)
        else:
            for tip in default_initial_tips:
                self.add_tip(tip)
    
    def add_tip(self, tip, tags=None):
     
        for existing_tip in self.tips:
            if self._similarity(tip, existing_tip) > 0.7:
                return False
        
        if len(self.tips) >= self.max_size:
            self._evict_tips()
        
        # tips attributes
        self.tips.append(tip)
        self.tip_stats[tip] = {
            'used_count': 0,
            'effectiveness': 0.0,
            'total_effectiveness': 0.0,  # cumulative effectiveness
            'last_used_generation': self.current_generation,  # record last used generation
            'tags': tags or []  # classification tags
        }
        return True
    
    def _calculate_eviction_score(self, tip_stats):

        PROBATION_USAGE_COUNT = 3  # probation usage count

        if tip_stats['used_count'] < PROBATION_USAGE_COUNT:
            return float('inf')  # grant "probation immunity"

    
        effectiveness_score = tip_stats['effectiveness']
        

        generations_idle = self.current_generation - tip_stats.get('last_used_generation', self.current_generation)
        
        # use a decay function to penalize effectiveness over time
        DECAY_RATE = 0.01
        time_penalty = generations_idle * DECAY_RATE
        
  
        final_score = effectiveness_score - time_penalty
        
        return final_score
    
    def _evict_tips(self):

        if len(self.tips) < self.max_size:
            return
        
        # calculate eviction scores for all tips
        eviction_candidates = []
        for tip in self.tips:
            score = self._calculate_eviction_score(self.tip_stats[tip])
            if score != float('inf'):  
                eviction_candidates.append((tip, score))
        
        # if no candidates, just evict the oldest tip
        if not eviction_candidates:
            oldest_tip = min(self.tips, key=lambda t: self.tip_stats[t].get('last_used_generation', 0))
            self.tips.remove(oldest_tip)
            del self.tip_stats[oldest_tip]
            return
        
        # evict the tip with the lowest score
        tip_to_evict = min(eviction_candidates, key=lambda x: x[1])[0]
        self.tips.remove(tip_to_evict)
        del self.tip_stats[tip_to_evict]
    
    def update_generation(self, generation):
       
        self.current_generation = generation
    
    def get_tips(self, k=3, strategy="adaptive"):
        
        if not self.tips:
            return []
            
        if len(self.tips) <= k:
            
            for tip in self.tips:
                self.tip_stats[tip]['used_count'] += 1
                self.tip_stats[tip]['last_used_generation'] = self.current_generation
            return list(self.tips)
        
        selected_tips = []
        
        if strategy == "random":
            selected_tips = random.sample(list(self.tips), k)
            
        elif strategy == "recent":
            
            sorted_tips = sorted(self.tips, 
                               key=lambda t: self.tip_stats[t]['last_used_generation'], 
                               reverse=True)
            selected_tips = sorted_tips[:k]
            
        elif strategy == "effective":
            
            sorted_tips = sorted(self.tips, 
                               key=lambda t: self.tip_stats[t]['effectiveness'], 
                               reverse=True)
            selected_tips = sorted_tips[:k]
            
        elif strategy == "balanced":
            
            if random.random() < 0.6:
                pool = sorted(self.tips, 
                               key=lambda t: self.tip_stats[t]['effectiveness'], 
                               reverse=True)
                selected_tips = pool[:k]
            else:
                pool = sorted(self.tips, 
                               key=lambda t: self.tip_stats[t]['used_count'])
                selected_tips = pool[:k]
                
        elif strategy == "adaptive":
            
            scored_tips = []
            for tip in self.tips:
                stats = self.tip_stats[tip]
                
                
                effectiveness_score = stats['effectiveness']
                usage_penalty = -0.1 * math.log(stats['used_count'] + 1)
                recency_bonus = 0.2 if (self.current_generation - stats['last_used_generation']) <= 2 else 0
                
                total_score = effectiveness_score + usage_penalty + recency_bonus
                scored_tips.append((tip, total_score))
            
            
            scored_tips.sort(key=lambda x: x[1], reverse=True)
            selected_tips = [tip for tip, score in scored_tips[:k]]
        
        else:
            
            selected_tips = random.sample(list(self.tips), k)
        
        
        for tip in selected_tips:
            self.tip_stats[tip]['used_count'] += 1
            self.tip_stats[tip]['last_used_generation'] = self.current_generation
            
        return selected_tips
    
    def update_tip_stats(self, tip, effectiveness):
    
        if tip in self.tip_stats:
            stats = self.tip_stats[tip]
            
   
            stats['total_effectiveness'] += effectiveness
            

            alpha = 0.3  # smoothing factor
            old_eff = stats['effectiveness']
            stats['effectiveness'] = (1-alpha) * old_eff + alpha * effectiveness
            
            
            stats['effectiveness'] = max(-1.0, min(1.0, stats['effectiveness']))
            
     
            stats['last_used_generation'] = self.current_generation
    
    def get_stats_summary(self):
        
        if not self.tips:
            return {"total_tips": 0}
        
        effectiveness_values = [self.tip_stats[tip]['effectiveness'] for tip in self.tips]
        usage_counts = [self.tip_stats[tip]['used_count'] for tip in self.tips]
        
        
        probation_count = sum(1 for tip in self.tips if self.tip_stats[tip]['used_count'] < 5)
        mature_count = len(self.tips) - probation_count
        
        return {
            "total_tips": len(self.tips),
            "probation_tips": probation_count,
            "mature_tips": mature_count,
            "avg_effectiveness": sum(effectiveness_values) / len(effectiveness_values),
            "max_effectiveness": max(effectiveness_values),
            "min_effectiveness": min(effectiveness_values),
            "avg_usage": sum(usage_counts) / len(usage_counts),
            "most_used_count": max(usage_counts),
            "best_tip": max(self.tips, key=lambda t: self.tip_stats[t]['effectiveness']),
            "most_used_tip": max(self.tips, key=lambda t: self.tip_stats[t]['used_count'])
        }
    
    def _similarity(self, tip1, tip2):
        
        words1 = set(tip1.lower().split())
        words2 = set(tip2.lower().split())
        
        if not words1 or not words2:
            return 0
            
        common_words = words1.intersection(words2)
        return len(common_words) / max(len(words1), len(words2))

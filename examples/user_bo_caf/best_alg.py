import torch
import torch.distributions as tdist
def utility(train_x, train_y, best_x, best_y, test_x, mean_test_y, std_test_y, cost_test_y, budget_used, budget_total):
    # Compute the improvement over the current best solution
    improvement = torch.clamp(mean_test_y - best_y, min=0)
    
    # Normalize the improvement by the standard deviation (scaled uncertainty)
    normalized_improvement = improvement / (std_test_y + 1e-6)
    
    # Compute the remaining budget and its ratio to the total budget
    remaining_budget = budget_total - budget_used
    budget_ratio = remaining_budget / budget_total
    
    # Adjust the utility based on cost efficiency relative to the remaining budget
    cost_efficiency = budget_ratio / (cost_test_y + 1e-6)
    
    # Introduce an adaptive penalty factor to discourage overly expensive evaluations
    penalty_factor = torch.exp(-cost_test_y / (remaining_budget + 1e-6))
    
    # Long-term impact factor: emphasize solutions with high potential cumulative gain
    cumulative_gain_factor = (remaining_budget * improvement) / (cost_test_y**2 + 1e-6)
    
    # Combine all factors into the final utility value
    utility_value = normalized_improvement * cost_efficiency + cumulative_gain_factor - penalty_factor
    
    return utility_value

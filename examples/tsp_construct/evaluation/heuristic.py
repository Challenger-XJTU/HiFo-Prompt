import numpy as np

def select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix):
    def build_quadtree_regions(unvisited_nodes, distance_matrix):
        if len(unvisited_nodes) <= 1:
            return {node: 0 for node in unvisited_nodes}
        coords = np.array([[distance_matrix[node, :].mean(), distance_matrix[:, node].mean()] for node in unvisited_nodes])
        x_min, x_max = coords[:, 0].min(), coords[:, 0].max()
        y_min, y_max = coords[:, 1].min(), coords[:, 1].max()
        mid_x, mid_y = (x_min + x_max) / 2, (y_min + y_max) / 2
        regions = {
            "top_left": [],
            "top_right": [],
            "bottom_left": [],
            "bottom_right": []
        }
        for node in unvisited_nodes:
            x, y = coords[list(unvisited_nodes).index(node)]
            if x < mid_x and y >= mid_y:
                regions["top_left"].append(node)
            elif x >= mid_x and y >= mid_y:
                regions["top_right"].append(node)
            elif x < mid_x and y < mid_y:
                regions["bottom_left"].append(node)
            else:
                regions["bottom_right"].append(node)
        return regions
    
    def perform_lookahead_simulation(node, current_node, unvisited_nodes, distance_matrix, simulations=8):
        total_cost = 0
        for _ in range(simulations):
            remaining_nodes = list(unvisited_nodes)
            remaining_nodes.remove(node)
            path = [current_node, node]
            while remaining_nodes:
                next_node = min(remaining_nodes, key=lambda x: distance_matrix[path[-1], x])
                path.append(next_node)
                remaining_nodes.remove(next_node)
            path.append(destination_node)
            total_cost += sum(distance_matrix[path[i], path[i+1]] for i in range(len(path)-1))
        return total_cost / simulations
    
    def structural_alignment_penalty(node, current_node, destination_node, distance_matrix):
        forward_cost = distance_matrix[current_node, node]
        backward_cost = distance_matrix[node, destination_node]
        detour_ratio = forward_cost / (backward_cost + 1e-9)
        return abs(detour_ratio - 1) ** 2 * forward_cost
    
    def calculate_hierarchical_score(node, current_node, destination_node, unvisited_nodes, distance_matrix, progress_ratio, region_weights):
        edge_cost = distance_matrix[current_node, node]
        look_ahead_cost = np.mean([distance_matrix[node, n] for n in unvisited_nodes])
        penalty = structural_alignment_penalty(node, current_node, destination_node, distance_matrix)
        region_weight = region_weights.get(node, 1.0)
        return 0.6 * edge_cost + 0.2 * (1 - progress_ratio) * look_ahead_cost + 0.2 * progress_ratio * penalty * region_weight
    
    # Progress ratio: Dynamically adjusts focus between local exploitation (early) and global exploration (late)
    progress_ratio = len(unvisited_nodes) / (len(unvisited_nodes) + len(distance_matrix) - 1)
    
    # Decompose unvisited nodes into hierarchical regions
    regions = build_quadtree_regions(unvisited_nodes, distance_matrix)
    
    # Assign weights to regions based on density and proximity to the destination
    region_weights = {}
    for region, nodes in regions.items():
        if not nodes:
            continue
        avg_distance_to_destination = np.mean([distance_matrix[node, destination_node] for node in nodes])
        region_weights.update({node: avg_distance_to_destination for node in nodes})
    max_weight = max(region_weights.values()) if region_weights else 1
    region_weights = {node: weight / max_weight for node, weight in region_weights.items()}
    
    # Perform lookahead simulations for global exploration insights
    simulation_scores = {node: perform_lookahead_simulation(node, current_node, unvisited_nodes, distance_matrix) for node in unvisited_nodes}
    
    # Calculate hierarchical scores combining edge costs, look-ahead evaluation, and structural penalties
    hierarchical_scores = {}
    for node in unvisited_nodes:
        hierarchical_score = calculate_hierarchical_score(node, current_node, destination_node, unvisited_nodes, distance_matrix, progress_ratio, region_weights)
        combined_score = 0.4 * simulation_scores[node] + 0.6 * hierarchical_score
        hierarchical_scores[node] = combined_score
    
    # Select the next node with the best combined score
    next_node = min(hierarchical_scores, key=hierarchical_scores.get)
    return next_node

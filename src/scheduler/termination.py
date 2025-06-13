import numpy as np
import time
from typing import List

def max_generations_reached(current_gen: int, max_gens: int) -> bool:
    """Check if maximum generations reached"""
    return current_gen >= max_gens

def target_fitness_reached(current_fitness: float, 
                         target: float) -> bool:
    """Check if target fitness achieved"""
    return current_fitness <= target

def time_limit_exceeded(start_time: float,
                       limit_seconds: float) -> bool:
    """Check if time limit exceeded"""
    if limit_seconds is None:
        return False
    return time.time() - start_time > limit_seconds
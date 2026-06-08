import os
import json
from pathlib import Path

def task_checkpoint(output_file):
    """
    Decorator to check if a task's output already exists.
    If it exists, the task can be skipped or the result loaded.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if output_file and os.path.exists(output_file):
                print(f"--- Task checkpoint found: {output_file} ---")
                # In a real CrewAI setup, we'd need to return something that
                # the Crew knows how to handle as a 'finished' task.
                # For now, this is a conceptual placeholder for logic we will
                # inject into the task execution flow.
            return func(*args, **kwargs)
        return wrapper
    return decorator

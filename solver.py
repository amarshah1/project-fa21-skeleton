from Task import Task
from parse import read_input_file, write_output_file
import os

# def getBestTask(tasks, time):
#     """
#     Args:
#         tasks: list[Task], list of igloos to polish
#         time: current time; int between 0 and 2440
#     Returns:
#         output: best igloo that we can finish before the deadline
#     """

#     for task in tasks:
        

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    
    output = list()
    curr_time = 0

    while curr_time <= 1400:
        scores = {t: t.get_score(t, curr_time) for t in tasks}
        next_igloo = min(scores, key=scores.get)
        output.append(next_igloo)
        curr_time += next_igloo.get_duration(next_igloo)
        tasks.remove(next_igloo)
    
    return output
        

# Here's an example of how to run your solver.
# if __name__ == '__main__':
#     for input_path in os.listdir('inputs/'):
#         output_path = 'outputs/' + input_path[:-3] + '.out'
#         tasks = read_input_file(input_path)
#         output = solve(tasks)
#         write_output_file(output_path, output)
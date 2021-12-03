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
        

# the first solve function we wrote
# used a heuristic that was a linear combination of (profit/time) and -(deadline)
def solve1(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """

    # correct_output_path = "samples/100.out"
    # correct_value = 0
    # time = 0
    # f = open(correct_output_path)
    # for elem in range(47):
    #     igloo_number = int(f.readline())
    #     # print(igloo_number)
    #     this_igloo = tasks[igloo_number - 1]
    #     time += this_igloo.get_duration()
    #     correct_value += this_igloo.get_late_benefit(this_igloo.get_deadline() - time)

    # print(time)
    # print(correct_value)
    
    
    output = list()
    curr_time = 0
    value = 0

    while curr_time <= 1440 and len(tasks) > 0:
        # sort tasks by profit in descending order
        tasks.sort(key= lambda x: x.get_late_benefit(), reverse= True)
        
        scores = {t: t.get_Score(curr_time) for t in tasks}
        next_igloo = max(scores, key=scores.get)

        # checks if there is none of the tasks finish before 1440
        if scores[next_igloo] == float('-inf'):
            # print('break')
            break

        output.append(next_igloo.get_task_id())
        curr_time += next_igloo.get_duration()
        tasks.remove(next_igloo)
        value += next_igloo.get_late_benefit(next_igloo.get_deadline() - curr_time)
    
    # print(value)
    # print(curr_time)
    return output


# a slighlty better greedy algorithm
# first finds the most valuable igloos and then picks then ones that have the earliest deadline
def solve(tasks):
    bestIgloos = list()
    curr_time = 0
    value = 0

    while curr_time <= 1440 and len(tasks) > 0:
        # scores = {t: t.get_max_benefit() for t in tasks}
        # apparently using get_max_benefit_before_deadline makes it run worse. This should not be the case :(
        next_igloo = max(tasks, key = (lambda x: x.get_max_benefit_before_deadline(curr_time)))

        #checks if out time goes over 1440
        if next_igloo.get_max_benefit_before_deadline(curr_time) == float("-inf"):
            break

        bestIgloos.append(next_igloo)
        curr_time += next_igloo.get_duration()
        tasks.remove(next_igloo)
    
    bestIgloos.sort(key = (lambda x: x.get_deadline())) #sorting by deadline instead of deadline - duration

    output = list()
    for igloo in bestIgloos:
        output.append(igloo.get_task_id())

    return output


# Here's an example of how to run your solver.
# if __name__ == '__main__':
#     for input_path in os.listdir('inputs/'):
#         output_path = 'outputs/' + input_path[:-3] + '.out'
#         tasks = read_input_file(input_path)
#         output = solve(tasks)
#         write_output_file(output_path, output)

# Solving outputs
if __name__ == '__main__':
    for input_path in os.listdir('inputs/small/'):
        if input_path[0] == '.':
            continue
        print(input_path)
        output_path = 'outputs/small/' + input_path[:-3] + '.out'
        tasks = read_input_file('inputs/small/' + input_path)
        output = solve(tasks)
        write_output_file(output_path, output)
    for input_path in os.listdir('inputs/medium/'):
        if input_path[0] == '.':
            continue
        print(input_path)
        output_path = 'outputs/medium/' + input_path[:-3] + '.out'
        tasks = read_input_file('inputs/medium/' + input_path)
        output = solve(tasks)
        write_output_file(output_path, output)
    for input_path in os.listdir('inputs/large/'):
        if input_path[0] == '.':
            continue
        print(input_path)
        output_path = 'outputs/large/' + input_path[:-3] + '.out'
        tasks = read_input_file('inputs/large/' + input_path)
        output = solve(tasks)
        write_output_file(output_path, output)

# Testing samples/100.in
# if __name__ == '__main__':
#     input_path = 'samples/100.in'
#     output_path = 'sample.out'
#     tasks = read_input_file(input_path)
#     output = solve(tasks)
#     write_output_file(output_path, output)
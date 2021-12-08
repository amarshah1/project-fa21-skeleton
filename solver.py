from Task import Task
from Strand import Strand
from parse import read_input_file, write_output_file
import os
from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue
from Tree import Tree
import math


#code for Priority Queus
# @dataclass(order=True)
# class PrioritizedItem:
#     priority: int
#     item: Any=field(compare=False)

# pq = []                         # list of entries arranged in a heap
# entry_finder = {}               # mapping of tasks to entries
# REMOVED = '<removed-task>'      # placeholder for a removed task
# counter = itertools.count()     # unique sequence count

# def add_task(task, priority=0):
#     'Add a new task or update the priority of an existing task'
#     if task in entry_finder:
#         remove_task(task)
#     count = next(counter)
#     entry = [priority, count, task]
#     entry_finder[task] = entry
#     heappush(pq, entry)

# def remove_task(task):
#     'Mark an existing task as REMOVED.  Raise KeyError if not found.'
#     entry = entry_finder.pop(task)
#     entry[-1] = REMOVED

# def pop_task():
#     'Remove and return the lowest priority task. Raise KeyError if empty.'
#     while pq:
#         priority, count, task = heappop(pq)
#         if task is not REMOVED:
#             del entry_finder[task]
#             return task
#     raise KeyError('pop from an empty priority queue')


#have this run whichever version of solver that we want
def solve(tasks):
    return solve_greg_for_loop(tasks)

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
        tasks.sort(key= lambda x: x.get_late_benefit(curr_time), reverse= True)
        
        # scores = {t: t.get_Score(curr_time) for t in tasks}
        next_igloo = max(tasks, key = lambda x: x.get_Score(curr_time))

        # checks if there is none of the tasks finish before 1440
        if next_igloo.get_Score == float('-inf'):
            # print('break')
            break

        output.append(next_igloo.get_task_id())
        curr_time += next_igloo.get_duration()
        tasks.remove(next_igloo)
        value += next_igloo.get_late_benefit(next_igloo.get_deadline() - curr_time)
    
    # print(value)
    # print(curr_time)
    return output, value


# a slighlty better greedy algorithm
# first finds the most valuable igloos and then picks then ones that have the earliest deadline
def solve2(tasks):
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

    time = 0
    output = list()
    for igloo in bestIgloos:
        output.append(igloo.get_task_id())
        value += igloo.get_late_benefit_before_time_limit(time)
        time += igloo.get_duration()

    return output, value

def solve_greg(tasks, snippet_size):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    
    output = list()
    curr_time = 0
    value = 0

    while curr_time <= 1440 and len(tasks) > 0:
        # sort tasks by profit per minute (including late benefits) in descending order
        tasks.sort(key= lambda x: x.get_late_benefit_before_time_limit(curr_time) / x.get_duration(), reverse= True)
        
        # Compare the soonest deadline of the first x number of igloos (tried with different snippet sizes from 40 to 1, and 20 seemed to work the best) (now trying to get a snippet size as a function to the length of tasks, so far len(tasks)/20(50?) seems to work the best)
        snip_size = math.ceil(len(tasks)/50)
        snippet = tasks[:snippet_size]
        snippet.sort(key= lambda x: x.get_deadline())
        
        next_igloo = snippet[0]

        if next_igloo.get_late_benefit_before_time_limit(curr_time) == float('-inf'):
            # print('break')
            break
        
        output.append(next_igloo.get_task_id())
        curr_time += next_igloo.get_duration()
        tasks.remove(next_igloo)
        value += next_igloo.get_late_benefit(next_igloo.get_deadline() - curr_time)

    return output, value

def solve_greg_for_loop(tasks):
    # write for loop in here
    snippetPQ = PriorityQueue()

    tasks_copy = tasks.copy()
    output1, value1 = solve1(tasks_copy)

    tasks_copy2 = tasks.copy()
    output2, value2 = solve2(tasks_copy)

    for i in range(1, len(tasks)):
        snippet_size = i
        sgOutput, sgValue = solve_greg(tasks, snippet_size)
        snippetPQ.put((-1 * sgValue, sgOutput))

    bestResult = snippetPQ.get()
    bestOutput = bestResult[1]
    bestValue = -1* bestResult[0]

    if value1 > bestValue:
        print("one")
        bestValue = value1
        bestOutput = output1
        
    if value2 > value1:
        print("two")
        bestValue = value2
        bestOutput = output2


    return bestOutput, bestValue

def solve_greg_2(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    start_tree = Tree(list(), 0, 0, None, None)
    helper(tasks, start_tree)

def helper(tasks, branch: Tree):
    if (len(tasks) < 1):
        return 
    curr_time = branch.get_total_time()
    benefit = branch.get_total_benefit()

    tasks.sort(key= lambda x: x.get_late_benefit_before_time_limit(curr_time), reverse= True)
    
    next_igloo = tasks[0]
    if next_igloo.get_late_benefit_before_time_limit(curr_time) != float('-inf'):
        branch.add_igloo(next_igloo, "left")
    else:
        branch.add_igloo(None, "left")
    
    branch.add_igloo(None, "right")
    
    tasks.remove(next_igloo)
    
    helper(tasks, branch.get_left_branch())
    helper(tasks, branch.get_right_branch())
    
    # print(value)
    # print(curr_time)
    return 

# #writing a program that uses a naive dp
# #basically, we assume that there is no late payoff, so the best tasks to do would be to 
# def dp_solver(tasks):

# # Here's an example of how to run your solver.
# # if __name__ == '__main__':
# #     for input_path in os.listdir('inputs/'):
# #         output_path = 'outputs/' + input_path[:-3] + '.out'
# #         tasks = read_input_file(input_path)
# #         output = solve(tasks)
# #         write_output_file(output_path, output)

#         """
#     Args:
#         tasks: list[Task], list of igloos to polish
#     Returns:
#         output: list of igloos in order of polishing  
#     """
    
#     output = list()
#     curr_time = 0
#     value = 0

#     tasks.sort(key= lambda x: get_deadline(curr_time))

#     while curr_time <= 1440 and len(tasks) > 0:
#         return max
    
#     # print(value)
#     # print(curr_time)
#     return output

# def dp_solver_helper(tasks, time):
#     if not tasks:
#         return 0


#trying to first sort
def memoized_dp_solver(tasks):
    sgAnswer, sgValue = solve_greg(tasks)
    tasks.sort(key= lambda x: x.get_deadline(), reverse = True)
    n = len(tasks)
    currentPQ = PriorityQueue(maxsize = 1000)
    firstStrand = Strand([], 0, 0, 0)
    currentPQ.put((0, firstStrand))
    for i in range(n):
        currentPQ = memoized_dp_helper(tasks, currentPQ, sgValue)
        tasks = tasks[1:]
        print('loop')

    bestStrand = currentPQ.queue[0][1]

    if sgValue > -1 * bestStrand.get_value():
        print(sgValue)
        return sgAnswer, sgValue
    else:
        print('hit')
        print(-1 * bestStrand.get_value())
        return bestStrand.get_chosen_list(), -1 * bestStrand.get_value()


def memoized_dp_helper(tasks, currentPQ, sgValue):
    nextPQ = PriorityQueue(maxsize = 1000)
    while not currentPQ.empty() and nextPQ.qsize() < 1000:
        if nextPQ.empty():
            bestStrand = Strand([], 1440, 1, 0)
        else:
            bestStrand = nextPQ.queue[0][1]
        # print(currentPQ.queue[0][1].get_printed_strand())
        # if currentPQ.queue[0][1].get_value() == 332.923:
        #     print(currentPQ.queue)
        #     curr1 = currentPQ.get()
        #     print('hurrah')
        currentStrand = currentPQ.get()[1]
        # print(len(tasks))
        # print(currentStrand.get_printed_strand())
        current_chosen_list = currentStrand.get_chosen_list()
        current_time = currentStrand.get_time()
        current_value = currentStrand.get_value()
        current_position = currentStrand.get_position()

        sameStrand = Strand(current_chosen_list, current_time, current_value, current_position + 1)

        currentTask = tasks[0]
        augmented_chosen_list = current_chosen_list + [currentTask.get_task_id()]
        current_value -= currentTask.get_late_benefit_before_time_limit(current_time)
        current_time += currentTask.get_duration()
        augmentedStrand = Strand(augmented_chosen_list, current_time, current_value, current_position + 1)

        sgValue_over_time = -1 * sgValue / 1440.

        # (sameStrand.get_time() < bestStrand.get_time() or sameStrand.get_value() < bestStrand.get_value())
        if (sameStrand.get_value_over_time() < bestStrand.get_value_over_time()) or not sameStrand.get_chosen_list() or sameStrand.get_value_over_time() < 0.99 * sgValue_over_time:
            if sameStrand.get_time() < 1440:
                nextPQ.put((sameStrand.get_value_over_time(), sameStrand))

        # augmentedStrand.get_time() < bestStrand.get_time() or augmentedStrand.get_value() < bestStrand.get_value()
        if augmentedStrand.get_value_over_time() <  bestStrand.get_value_over_time() or not augmentedStrand.get_chosen_list() or sameStrand.get_value_over_time() < 0.99 * sgValue_over_time:
            if augmentedStrand.get_time() < 1440:
                nextPQ.put((augmentedStrand.get_value_over_time(), augmentedStrand))

    # print(nextPQ.queue)
    return nextPQ

# Solving outputs
def run_solver():
    # start: for local testing
    subname = "-snipsize"
    # end: for local testing
    
    if __name__ == '__main__':
        # start: for local testing
        overall_total = 0
        count = 0
        # end: for local testing
        for input_path in os.listdir('inputs/small/'):
            if input_path[0] == '.':
                continue
            print(input_path)
            output_path = 'outputs/small/' + input_path[:-3] + '.out'
            tasks = read_input_file('inputs/small/' + input_path)
            output, total_benefit = solve(tasks)
            
            # start: for local testing
            file = open("testing" + subname + "/small_inputs_total_benefits.txt", "a")
            file.write(input_path + ": " + str(total_benefit) + "\n")
            overall_total += total_benefit
            count += 1
            # end: for local testing
            
            write_output_file(output_path, output)
        # start: for local testing
        mean = overall_total / count
        file.write("OVERALL TOTAL: " + str(overall_total) + "\n")
        file.write("MEAN: " + str(mean) + "\n")
        # end: for local testing
        
        # start: for local testing
        overall_total = 0
        count = 0
        # end: for local testing
        for input_path in os.listdir('inputs/medium/'):
            if input_path[0] == '.':
                continue
            print(input_path)
            output_path = 'outputs/medium/' + input_path[:-3] + '.out'
            tasks = read_input_file('inputs/medium/' + input_path)
            output, total_benefit = solve(tasks)
            
            # start: for local testing
            file = open("testing" + subname + "/medium_inputs_total_benefits.txt", "a")
            file.write(input_path + ": " + str(total_benefit) + "\n")
            overall_total += total_benefit
            count += 1
            # end: for local testing
            
            write_output_file(output_path, output)
        # start: for local testing
        mean = overall_total / count
        file.write("OVERALL TOTAL: " + str(overall_total) + "\n")
        file.write("MEAN: " + str(mean) + "\n")
        # end: for local testing
            
        # start: for local testing
        overall_total = 0
        count = 0
        # end: for local testing
        for input_path in os.listdir('inputs/large/'):
            if input_path[0] == '.':
                continue
            print(input_path)
            output_path = 'outputs/large/' + input_path[:-3] + '.out'
            tasks = read_input_file('inputs/large/' + input_path)
            output, total_benefit = solve(tasks)
            
            # start: for local testing
            file = open("testing" + subname + "/large_inputs_total_benefits.txt", "a")
            file.write(input_path + ": " + str(total_benefit) + "\n")
            overall_total += total_benefit
            count += 1
            # end: for local testing
            
            write_output_file(output_path, output)
        # start: for local testing
        mean = overall_total / count
        file.write("OVERALL TOTAL: " + str(overall_total) + "\n")
        file.write("MEAN: " + str(mean) + "\n")
        # end: for local testing

    # Testing samples/100.in
    # if __name__ == '__main__':
    #     input_path = 'samples/100.in'
    #     output_path = 'sample.out'
    #     tasks = read_input_file(input_path)
    #     output = solve(tasks)
    #     write_output_file(output_path, output)
    
run_solver()

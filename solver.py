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
        scores = {t: t.get_Score(curr_time) for t in tasks}
        next_igloo = max(scores, key=scores.get)

        #checks if there is none of the tasks finish before 1440
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
        

# Here's an example of how to run your solver.
if __name__ == '__main__':
    for input_path in os.listdir('inputs/'):
        output_path = 'outputs/' + input_path[:-3] + '.out'
        tasks = read_input_file(input_path)
        output = solve(tasks)
        write_output_file(output_path, output)




# if __name__ == '__main__':
#     input_path = 'samples/100.in'
#     output_path = 'sample.out'
#     tasks = read_input_file(input_path)
#     output = solve(tasks)
#     write_output_file(output_path, output)
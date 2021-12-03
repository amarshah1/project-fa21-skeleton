from solver import solve
from Task import Task
from parse import *
import os

# Comparing solution (100.out) to out out (sample.out)

if __name__ == '__main__':
    input_path = 'samples/100.in'
    sol_path = 'samples/100.out'
    out_path = 'sample.out'
    
    tasks = read_input_file(input_path)
    output = solve(tasks)
    solution = read_output_file(sol_path)
    out = read_output_file(out_path)
    
    solution_tasks = map(lambda x: tasks[x - 1], solution)
    
    print(solution_tasks)
import Task
import math
from queue import PriorityQueue
from functools import total_ordering


@total_ordering
class Strand:
    def __init__(self, chosen_list: list, time: int, value: float, position: int) -> None:
        """
        Creates a new strand with the corresponding task_list, time, value

        Args: 
        # - task_list(list[Task]): list of tasks left to -> deleted it to save space
        - chosen_list(list[int]): list of the task_id's of the Tasks that we have picked so far
        - time (int): time that the tasks we have chosen so far have taken
        - value (float): value realized by all of the Tasks that we have chose so far
        - position (int): basically telling you how many Tasks we have considered so far

        Output:
        - Strand object: corresponding Task object

        """
        # self.task_list = task_list
        self.chosen_list = chosen_list
        self.time = time
        self.value = value
        self.position = position
 
    # def get_task_list(self) -> list:
    # 	return self.task_list


    def get_chosen_list(self) -> list:
    	return self.chosen_list

    def get_time(self) -> int:
    	return self.time

    def get_value(self) -> float:
    	return self.value

    def get_position(self) -> int:
    	return self.position

    def get_value_over_time(self) -> float:
    	if self.time == 0:
    		return 0
    	return self.value / self.time

    def get_printed_strand(self) -> str:
    	return "[" + "".join(str(e) + "|" for e in self.get_chosen_list()) + ", " + str(self.get_time()) + ", " + str(self.get_value()) + ", " + str(self.get_position()) + "]"

    def __eq__(self, other):
    	return False

    def __lt__(self, other):
    	return True



from Task import Task

class Tree:
    def __init__(self, task_ids: list, total_time: int, total_benefit: float, right_branch, left_branch) -> None:
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
        self.task_ids = task_ids
        self.total_time = total_time
        self.total_benefit = total_benefit
        
        self.right_branch = right_branch
        self.left_branch = left_branch
        
    def get_right_branch(self):
        return self.right_branch
    
    def get_left_branch(self):
        return self.left_branch
    
    def get_total_time(self):
        return self.total_time
    
    def get_task_ids(self):
        return self.task_ids
    
    def get_total_benefit(self):
        return self.total_benefit
    
    def add_igloo(self, task: Task, branch):
        if (task == None):
            new_branch = Tree(self.get_task_ids(), self.get_total_time(), self.get_total_benefit(), None, None)
        elif (task != None):
            time = self.total_time + task.get_duration()
            benefit = self.total_benefit + task.get_late_benefit(time - task.get_duration())
            ids = self.get_task_ids() + [task.get_task_id()]
            new_branch = Tree(ids, time, benefit, None, None)
            
        if branch == "left":
            self.left_branch = new_branch
        elif branch == "right":
            self.right_branch = new_branch

    def tree_to_string(self):
        result = str(self.get_total_benefit())
        if (self.get_left_branch() != None):
            result += "\n    " + self.get_left_branch().tree_to_string()
        if (self.get_right_branch() != None):
            result += "\n    " + self.get_right_branch().tree_to_string()
        return result
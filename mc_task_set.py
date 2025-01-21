from math_utils import lcm_list
class MCTaskSet:
    def __init__(self, tasks):
        self.tasks = tasks
        self.periods = [task.get_t() for task in tasks]
        max_d = 0
        sum_wcet_1 = 0
        for task in tasks:
            tmp = task.get_d(0)
            if tmp > max_d:
                max_d = tmp
            sum_wcet_1 += task.get_wcet(1)
        self.average_wcet = sum_wcet_1 / len(tasks)
        self.hyperperiod = lcm_list(self.periods) + max_d

    def get_tasks(self):
        return self.tasks

    def get_utilization_lo(self):
        util = 0
        for task in self.tasks:
            util += task.get_wcet(0) / task.get_t()
        return util

    def get_utilization_hi_hi(self):
        util = 0
        for task in self.tasks:
            if task.get_l() == 1:
                util += task.get_wcet(1) / task.get_t()
        return util

    def get_utilization_hi_lo(self):
        util = 0
        for task in self.tasks:
            if task.get_l() == 1:
                util += task.get_wcet(0) / task.get_t()
        return util

    def get_utilization_lo_lo(self):
        util = 0
        for task in self.tasks:
            if task.get_l() == 0:
                util += task.get_wcet(0) / task.get_t()
        return util

    def get_utilization_lo_hi(self):
        util = 0
        for task in self.tasks:
            if task.get_l() == 0:
                util += task.get_wcet(1) / task.get_t()
        return util

    def get_schedulability_bound_hi(self):
        periods = [task.get_t() for task in self.tasks]
        hyperperiod = lcm_list(periods)
        u = self.get_utilization_hi_hi()
        max_value = 0
        max_d = 0
        for task in self.tasks:
            tmp = task.get_t() - (task.get_d(1) - task.get_d(0))
            if tmp > max_value:
                max_value = tmp
            tmp = task.get_d(1)
            if tmp > max_d:
                max_d = tmp
        if hyperperiod <= 0:
            return int(max_value * u / (1 - u))
        return min(hyperperiod + max_d, int(max_value * u / (1 - u)))

    def get_schedulability_bound_lo(self):
        periods = [task.get_t() for task in self.tasks]
        hyperperiod = lcm_list(periods)
        u = self.get_utilization_hi_hi()
        max_value = 0
        max_d = 0
        for task in self.tasks:
            tmp = task.get_t() - task.get_d(0)
            if tmp > max_value:
                max_value = tmp
            tmp = task.get_d(0)
            if tmp > max_d:
                max_d = tmp
        if hyperperiod <= 0:
            return int(max_value * u / (1 - u))
        return min(hyperperiod + max_d, int(max_value * u / (1 - u)))

    def hyperperiod(self):
        return self.hyperperiod

    def reorder(self, task_index, priority_level):
        self.tasks[task_index], self.tasks[priority_level] = self.tasks[priority_level], self.tasks[task_index]

    def get_average_wcet(self):
        return self.average_wcet

    def __str__(self):
        return str(self.tasks)

    def export(self):
        export_str = ""
        for task in self.tasks:
            export_str += f"{task.get_wcet(0)} {task.get_wcet(1)} {task.get_t()} {task.get_d(0)} {task.get_d(1)} {task.get_l()}\n"
        return export_str

    def get_cp(self):
        sum_hi = sum(1 for task in self.tasks if task.get_l() == 1)
        return sum_hi / len(self.tasks)

    def lo_count(self):
        return sum(1 for task in self.tasks if task.get_l() == 0)

    def hi_count(self):
        return sum(1 for task in self.tasks if task.get_l() == 1)

    def __hash__(self):
        return hash(tuple(self.tasks))

    def __eq__(self, other):
        if isinstance(other, MCTaskSet):
            return set(self.tasks) == set(other.tasks)
        return False
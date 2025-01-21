class ResponseTimeHI:
    def response_time(self, i, task_set):
        tasks = task_set.get_tasks()
        task = tasks[i]
        R = 0
        C = task.get_wcet(1)
        D = task.get_d()
        t = C
        while R!= t and R <= D:
            R = t
            t = C
            for j in range(i):
                task_j = tasks[j]
                if task_j.get_l() > 0:
                    t += round(R / task_j.get_t()) * task_j.get_wcet(1)
        return R

    def print_response_time(self, i, priority_order, ordered_set):
        tasks = ordered_set.get_tasks()
        task = tasks[i]
        C = task.get_wcet(1)
        D = task.get_d()
        R = self.response_time(i, ordered_set)
        idx = priority_order[i]
        formula = f"R_{idx + 1}^{{HI}} = {C}"
        for j in range(i):
            task_j = tasks[j]
            if task_j.get_l() == 1:
                formula += f" + \\lceil\\frac{{R_{idx + 1}}}{{{task_j.get_t()}}}\\rceil \\cdot {task_j.get_wcet(1)}"
        formula += f" = {R}"
        return formula
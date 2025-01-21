from mc_task_set import MCTaskSet

class PriorityAssignmentOPA:
    def __init__(self, response_time):
        self.response_time = response_time

    def testOPA(self, i, j, task_set):
        R = self.response_time.response_time(j, task_set)
        return R <= task_set.get_tasks()[j].get_d()

    def assign(self, task_set):
        n = len(task_set.get_tasks())
        unassigned = True

        assigned = task_set.get_tasks()[:]

        for j in range(n - 1, -1, -1):
            unassigned = True
            for i in range(j + 1):
                assigned[i], assigned[j] = assigned[j], assigned[i]
                if self.testOPA(i, j, MCTaskSet(assigned)) and unassigned:
                    unassigned = False
                    break
                else:
                    assigned[i], assigned[j] = assigned[j], assigned[i]
            if unassigned:
                return None
        return MCTaskSet(assigned)

    def __str__(self):
        return "OPA"
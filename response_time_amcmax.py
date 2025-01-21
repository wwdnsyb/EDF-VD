from response_time_lo import ResponseTimeLO

from response_time_hi import ResponseTimeHI

class ResponseTimeAMCmax:
    def __init__(self):
        self.response_time_hi = ResponseTimeHI()
        self.response_time_lo = ResponseTimeLO()
        self.smax = 0
        self.M = 0

    def response_time(self, i, task_set):
        tasks = task_set.get_tasks()
        task = tasks[i]
        R = 0
        Rmax = 0
        L = task.get_l()
        C = task.get_wcet(1)
        D = task.get_d()
        t = C
        R_lo = self.response_time_lo.response_time(i, task_set)
        if L == 0:
            return R_lo
        if R_lo > D:
            return R_lo
        S = self.get_s(i, task_set, R_lo)
        Rmax = C
        m = 0
        for s in S:
            R = 0
            t = C
            while R!= t and R <= D:
                R = t
                t = C
                for j in range(i):
                    task_j = tasks[j]
                    if task_j.get_l() == 0:
                        t += (s // task_j.get_t() + 1) * task_j.get_wcet(0)
                    else:
                        m = self.get_m(task_j.get_t(), task_j.get_d(), s, R)
                        t += m * task_j.get_wcet(1) + ((R // task_j.get_t() + 1) - m) * task_j.get_wcet(0)
            if R > Rmax:
                Rmax = R
                self.smax = s
                self.M = m
        R_hi = self.response_time_hi.response_time(i, task_set)
        Rmax = max(Rmax, R_lo, R_hi)
        return Rmax

    def get_m(self, Tk, Dk, s, t):
        return min(int((t - s - (Tk - Dk)) / Tk + 1), int(t / Tk))

    def get_s(self, i, task_set, r_lo):
        for_export = []
        tasks = task_set.get_tasks()
        task = tasks[i]
        for j in range(i):
            task_j = tasks[j]
            if task_j.get_l() < task.get_l() and j!= i:
                for s in range(0, (r_lo // task_j.get_t() - 1) * task_j.get_t() + 1, task_j.get_t()):
                    if s not in for_export:
                        for_export.append(s)
        return for_export

    def __str__(self):
        return "AMC-max"

    def print_response_time(self, i, priority_order, task_set):
        tasks = task_set.get_tasks()
        task = tasks[i]
        L = task.get_l()
        C = task.get_wcet(L)
        CLO = task.get_wcet(0)
        R = self.response_time(i, task_set)
        RLO = self.response_time_lo.response_time(i, task_set)
        RHI = self.response_time_hi.response_time(i, task_set)
        idx = priority_order[i]
        for_export = "\n"
        for_export += f"R_{idx + 1}^{{LO}} = {CLO}"
        for j in range(i):
            task_j = tasks[j]
            for_export += f" + \\lceil\\frac{{R_{idx + 1}}}{{{task_j.get_t()}}}\\rceil \\cdot {task_j.get_wcet(0)}"
        for_export += f" = {RLO}\n"
        for_export += f"R_{idx + 1}^{{HI}} = {C}"
        for j in range(i):
            if tasks[j].get_l() == 1:
                task_j = tasks[j]
                for_export += f" + \\lceil\\frac{{R_{idx + 1}}}{{{task_j.get_t()}}}\\rceil \\cdot {task_j.get_wcet(1)}"
        for_export += f" = {RHI}\n"
        for_export += f"R_{idx + 1}^{{MC}} = {C}"
        for j in range(i):
            task_j = tasks[j]
            if task_j.get_l() == 0:
                for_export += f" + \\big(\\lfloor\\frac{{{self.smax}}}{{{task_j.get_t()}}}\\rfloor + 1 \\big) \\cdot {task_j.get_wcet(0)}"
            else:
                for_export += f" + {self.M} \\cdot {task_j.get_wcet(1)} + \\big(\\lceil\\frac{{R_{idx + 1}^{{MC}}}}{{{task_j.get_t()}}}\\rceil - {self.M} \\big) \\cdot {task_j.get_wcet(0)}"
        for_export += f" = {R}\n"
        return for_export
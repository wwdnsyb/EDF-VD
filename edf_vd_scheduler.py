from mc_task import MCTask
from mc_task_set import MCTaskSet
from math_utils import lcm_list

class EDFVDScheduler:
    def __init__(self):
        pass

    def calc_x(self, task_set: MCTaskSet):
        # 计算X参数（虚拟截止期缩放因子）
        tasks = task_set.get_tasks()
        u_lo_lo = sum(t.get_wcet(0)/t.get_t() for t in tasks if t.get_l() == 0)
        u_hi = sum(t.get_wcet(1)/t.get_t() for t in tasks if t.get_l() == 1)
        u_lo_hi = sum(t.get_wcet(0)/t.get_t() for t in tasks if t.get_l() == 1)
        if 1 - u_lo_lo == 0:
            return 1.0
        x = u_lo_hi / (1 - u_lo_lo)
        chk = x * u_lo_lo + u_hi
        if chk <= 1:
            return min(round(x, 4), 1.0)
        else:
            return 1.0

    def schedule(self, task_set: MCTaskSet):
        tasks = task_set.get_tasks()
        n = len(tasks)
        x = self.calc_x(task_set)
        # 构造虚拟截止期
        vd_deadlines = []
        for t in tasks:
            if t.get_l() == 1:
                vd_deadlines.append(x * t.get_d(0))
            else:
                vd_deadlines.append(t.get_d(0))
        # 计算超周期
        periods = [t.get_t() for t in tasks]
        hyperperiod = lcm_list(periods)
        # 生成所有任务实例
        instances = []
        for i, t in enumerate(tasks):
            release = 0
            while release < hyperperiod:
                if t.get_l() == 1:
                    deadline = release + vd_deadlines[i]
                    exec_time = t.get_wcet(0)
                else:
                    deadline = release + vd_deadlines[i]
                    exec_time = t.get_wcet(0)
                instances.append({
                    'task_id': i+1,
                    'release': release,
                    'deadline': deadline,
                    'exec_time': exec_time,
                    'remain': exec_time,
                    'L': t.get_l(),
                })
                release += t.get_t()
        # 按release和deadline排序
        instances.sort(key=lambda x: (x['release'], x['deadline']))
        time = 0
        schedule = []
        ready = []
        running = None
        while time < hyperperiod:
            # 加入新释放的任务
            for inst in instances:
                if inst['release'] == time and inst['remain'] > 0:
                    ready.append(inst)
            # 移除已完成
            ready = [r for r in ready if r['remain'] > 0]
            # 选最早截止期
            if ready:
                ready.sort(key=lambda x: x['deadline'])
                running = ready[0]
                running['remain'] -= 1
                schedule.append(f"Time {time}: Task {running['task_id']} (L={running['L']})")
            else:
                schedule.append(f"Time {time}: Idle")
            time += 1
        # 检查可调度性
        schedulable = True
        for inst in instances:
            finish_time = None
            spent = 0
            for t, entry in enumerate(schedule):
                if f"Task {inst['task_id']}" in entry:
                    spent += 1
                    if spent == inst['exec_time']:
                        finish_time = t
                        break
            if finish_time is None or finish_time >= inst['deadline']:
                schedulable = False
                break

        # 分析输出：X参数和虚拟截止期
        print(f"X参数: {x}")
        for i, t in enumerate(tasks):
            print(f"任务{i+1} 虚拟截止期: {vd_deadlines[i]}, C(LO): {t.get_wcet(0)}")

        return {
            'schedulable': schedulable,
            'schedule': schedule,
            'X': x,
            'hyperperiod': hyperperiod
        } 
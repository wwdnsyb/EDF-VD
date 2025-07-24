from mc_task import MCTask
from mc_task_set import MCTaskSet
from priority_assignment_opa import PriorityAssignmentOPA
from response_time_amcmax import ResponseTimeAMCmax

# 新增：导入EDF-VD调度器
from edf_vd_scheduler import EDFVDScheduler


def read_tasks_from_txt(filename):
    tasks = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = [x.strip() for x in line.strip().split(',')]
            if len(parts) >= 9:
                try:
                    C_LO, C_HI, T, D_LO, D_HI, L = map(int, [parts[3], parts[4], parts[5], parts[6], parts[7], parts[8]])
                    tasks.append(MCTask([C_LO, C_HI], T, [D_LO, D_HI], L))
                except Exception:
                    continue
    return tasks


def main():
    import os
    txt_path = os.path.join(os.path.dirname(__file__), 'Tasks.txt')
    if os.path.exists(txt_path):
        task_list = read_tasks_from_txt(txt_path)
    else:
        task_list = []
    if not task_list:
        task_list = [
            MCTask([10, 20], 50, [30, 40], 1),
            MCTask([5, 10], 30, [20, 25], 0)
        ]
    task_set = MCTaskSet(task_list)

    response_time_calculator = ResponseTimeAMCmax()
    priority_assigner = PriorityAssignmentOPA(response_time_calculator)
    assigned_task_set = priority_assigner.assign(task_set)
    print("\n=== AMC-Max 算法调度分析 ===")
    if assigned_task_set is None:
        print("无法成功分配优先级，任务集不存在可行的优先级分配方案")
    else:
        is_schedulable = True
        for i, task in enumerate(assigned_task_set.get_tasks()):
            if response_time_calculator.response_time(i, assigned_task_set) > task.get_d():
                is_schedulable = False
                break
        if is_schedulable:
            print("任务集可调度")
            for i in range(len(assigned_task_set.get_tasks())):
                priority_order = {j: j for j in range(len(assigned_task_set.get_tasks()))}
                print(response_time_calculator.print_response_time(i, priority_order, assigned_task_set))
        else:
            print("任务集不可调度")

    print("\n=== EDF-VD 算法调度分析 ===")
    edf_vd_scheduler = EDFVDScheduler()
    edf_vd_result = edf_vd_scheduler.schedule(task_set)
    if edf_vd_result['schedulable']:
        print("任务集可调度 (EDF-VD)")
        print("调度序列:")
        for entry in edf_vd_result['schedule']:
            print(entry)
    else:
        print("任务集不可调度 (EDF-VD)")


if __name__ == "__main__":
    main()

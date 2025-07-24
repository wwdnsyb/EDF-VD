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
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # 新格式: 任务ID,任务名称,任务描述,C(LO),C(HI),T,D(LO),D(HI),L
            parts = [x.strip() for x in line.split(',')]
            if len(parts) < 9:
                continue
            # 只提取数字字段
            try:
                C_LO = int(parts[3])
                C_HI = int(parts[4])
                T = int(parts[5])
                D_LO = int(parts[6])
                D_HI = int(parts[7])
                L = int(parts[8])
                tasks.append(MCTask([C_LO, C_HI], T, [D_LO, D_HI], L))
            except Exception as e:
                print(f"跳过格式错误行: {line} ({e})")
    return tasks


def main():
    # 从Tasks.txt读取任务集
    import os
    txt_path = os.path.join(os.path.dirname(__file__), 'Tasks.txt')
    if os.path.exists(txt_path):
        task_list = read_tasks_from_txt(txt_path)
        if not task_list:
            print('Tasks.txt 文件为空或格式不正确，使用默认任务集')
            task_list = [
                MCTask([10, 20], 50, [30, 40], 1),
                MCTask([5, 10], 30, [20, 25], 0)
            ]
    else:
        print('未找到 Tasks.txt，使用默认任务集')
        task_list = [
            MCTask([10, 20], 50, [30, 40], 1),
            MCTask([5, 10], 30, [20, 25], 0)
        ]
    task_set = MCTaskSet(task_list)

    # AMC算法调度分析
    response_time_calculator = ResponseTimeAMCmax()
    priority_assigner = PriorityAssignmentOPA(response_time_calculator)
    assigned_task_set = priority_assigner.assign(task_set)
    print("\n=== AMC-Max 算法调度分析 ===")
    if assigned_task_set is None:
        print("无法成功分配优先级，任务集不存在可行的优先级分配方案")
    else:
        is_schedulable = True
        for i in range(len(assigned_task_set.get_tasks())):
            response_time = response_time_calculator.response_time(i, assigned_task_set)
            task = assigned_task_set.get_tasks()[i]
            if response_time > task.get_d():
                is_schedulable = False
                break
        if is_schedulable:
            print("任务集可调度")
            for i in range(len(assigned_task_set.get_tasks())):
                priority_order = {j: j for j in range(len(assigned_task_set.get_tasks()))}
                print(response_time_calculator.print_response_time(i, priority_order, assigned_task_set))
        else:
            print("任务集不可调度")

    # 新增：EDF-VD算法调度分析
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

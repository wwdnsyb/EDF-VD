from mc_task import MCTask
from mc_task_set import MCTaskSet
from priority_assignment_opa import PriorityAssignmentOPA
from response_time_amcmax import ResponseTimeAMCmax


def main():
    # 创建任务实例
    task1 = MCTask([10, 20], 50, [30, 40], 1)
    task2 = MCTask([5, 10], 30, [20, 25], 0)
    # 构建初始任务集
    task_set = MCTaskSet([task1, task2])

    # 实例化用于计算响应时间的对象（这里是ResponseTimeAMCmax，可按需替换）
    response_time_calculator = ResponseTimeAMCmax()

    # 实例化PriorityAssignmentOPA对象，传入响应时间计算器
    priority_assigner = PriorityAssignmentOPA(response_time_calculator)
    # 使用assign方法进行优先级分配，得到分配好优先级后的任务集
    assigned_task_set = priority_assigner.assign(task_set)
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


if __name__ == "__main__":
    main()

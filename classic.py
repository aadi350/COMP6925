from pulp import LpMinimize, LpProblem, lpSum, LpVariable, LpBinary, LpStatus, LpMaximize

WINDOW = 180
HIGH = 100
LOW = 70


def optimize_single_classic(task_list):
    model = LpProblem(name='MinPower', sense=LpMinimize)

    high_f = {i: LpVariable(name=f"high_{i}", lowBound=0, cat=LpBinary) for i in range(len(task_list))}
    low_f = {i: LpVariable(name=f"low_{i}", lowBound=0, cat=LpBinary) for i in range(len(task_list))}

    # single processor constraint
    for i in range(len(task_list)):
        model.add(high_f[i] + low_f[i] == 1)

    model.add(lpSum(
        (task_list[i].cycles / HIGH) * high_f[i] + (task_list[i].cycles / LOW) * low_f[i] for i in range(len(task_list))) <= WINDOW)

    # # Maximize priority
    # model += lpSum(task_list[i].priority*(high_f[i] + low_f[i]) for i in range(len(task_list)))

    # Minimize power
    model += lpSum(task_list[i].cycles * high_f[i] + task_list[i].cycles * low_f[i] for i in range(len(task_list)))

    status = LpStatus[model.solve()]
    best_time = lpSum((task_list[i].cycles / HIGH) * high_f[i].value() + (task_list[i].cycles / LOW) * low_f[i].value() for i in range(len(task_list)))
    best_power = lpSum((task_list[i].cycles*(HIGH*high_f[i].value() + LOW*low_f[i].value())) for i in range(len(task_list)))

    # for i in range(len(tasks)):
    #     print(high_f[i].value(),' ',low_f[i].value() )

    return status, best_time, best_power, len(task_list), None

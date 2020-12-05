import pulp as pl
from pulp import LpMinimize, LpProblem, lpSum, LpVariable, LpBinary

from tasks_gen import get_tasks
print(pl.listSolvers())
TIME_MAX = 100
HIGH = 100
LOW = 70
tasks = get_tasks(90)
task_matrix = []

# for i in range(len(tasks)):
#     task_matrix.append([
#         tasks[i].id,
#         tasks[i].priority,
#         tasks[i].cycles,
#         0,  # HIGH frequency assignment
#         0  # LOW frequency assignment
#     ])
#
# print(task_matrix)

model = LpProblem(name='MaxPriority', sense=LpMinimize)


high_f = {i: LpVariable(name=f"high_{i}", lowBound=0, cat=LpBinary) for i in range(len(tasks))}
low_f = {i: LpVariable(name=f"low_{i}", lowBound=0, cat=LpBinary) for i in range(len(tasks))}


# single processor constraint
for i in range(len(tasks)):
    model.add(high_f[i] + low_f[i] == 1)

model.add(lpSum((tasks[i].cycles/HIGH)*high_f[i] + (tasks[i].cycles/LOW)*low_f[i] for i in range(len(tasks))) <= TIME_MAX)

# # Maximize priority
# model += lpSum(tasks[i].priority*(high_f[i] + low_f[i]) for i in range(len(tasks)))

# Minimize power
model += lpSum(tasks[i].cycles*high_f[i] + tasks[i].cycles*low_f[i] for i in range(len(tasks)))

status = model.solve(pl.getSolver('GLPK_CMD'))

print('Net time', lpSum((tasks[i].cycles/HIGH)*high_f[i].value() + (tasks[i].cycles/LOW)*low_f[i].value() for i in range(len(tasks))))
print('Net power', lpSum(HIGH*high_f[i].value() + LOW*low_f[i].value() for i in range(len(tasks))))

# for i in range(len(tasks)):
#     print(high_f[i].value(),' ',low_f[i].value() )

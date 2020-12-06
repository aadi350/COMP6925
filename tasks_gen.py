import random
from Task import Task
from numpy.random import normal
from numpy.random import poisson

HIGH = 100
LOW = 70
WINDOW = 90


def get_tasks(mean=100, limit_upper=200):
    n = int(gen_num_tasks(mean))
    priority = gen_priority(n)
    clk_cycles = gen_clk_cycles(n, limit_upper)
    task_list = []
    for i in range(1, n):
        temp_task = Task(id=i, priority=priority[i], clk_cycles=clk_cycles[i])
        temp_task.set_processor(HIGH)
        task_list.append(temp_task)
    return task_list


def gen_priority(n):
    return [random.choice(range(1, 4)) for i in range(n)]


def gen_num_tasks(mean):
    return normal(mean, 4)


def gen_clk_cycles(n, limit_upper):
    clk_cycles = poisson(100, int(n))
    clk_cycles[clk_cycles > limit_upper] = limit_upper
    return clk_cycles

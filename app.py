import time
import csv
import logging
from Task import Task
from tasks_gen import get_tasks

HIGH = 100
PRINT_LOGS = False
LOW = 70
WINDOW = 300


def load_tasks(file_path='tasks.csv'):
    task_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            row_list = []
            for i in row:
                params = [int(param) for param in i.split()]
                logging.debug('params', params)
                temp_task = Task(id=params[0], priority=params[1], clk_cycles=params[2])
                temp_task.set_processor(HIGH)
                row_list.append(temp_task)
            logging.debug('Row list', row_list)
            task_list.append(row_list)
        logging.debug('Task list', task_list)
    return task_list


def optimize_single_set(task_list):
    initial_list_size = len(task_list)
    print('Number of tasks: ', initial_list_size)
    status = None
    # priority
    best_solution = 0
    best_schedule = None
    remaining_schedules = []
    task_list.sort(key=lambda x: x.priority, reverse=True)

    for task in task_list:
        schedule = [task]
        remaining_schedules.append(schedule)

    s_new = None
    for s in remaining_schedules:
        print("Num remaining_schedules", len(remaining_schedules))
        remaining_schedules.remove(s)
        if len(remaining_schedules) < 1:
            break
        for task in task_list:
            if task not in s:
                new_time = sum(s[i].time for i in range(1, len(s))) + task.time
                if new_time < WINDOW:
                    s_new = s
                    s_new.append(task)
                    priority_new = sum(s_new[i].priority for i in range(1, len(s_new)))
                    if priority_new > best_solution:
                        best_solution = priority_new
                        best_schedule = s_new
                    # step-down processing power for last added task
                    logging.info('Fast time: {}'.format(s_new[-1].get_time()))
                    s_new[-1].set_processor(LOW)
                    logging.info('Slow time: {}'.format(s_new[-1].get_time()))
                    step_down_time = sum(s[i].time for i in range(1, len(s))) + task.time
                    if step_down_time > WINDOW:
                        logging.debug('Step down not feasible')
                        s_new[-1].set_processor(HIGH)
                    else:
                        logging.debug('Stepped-down')
                    status = True
                else:
                    status = False
        remaining_schedules.append(s_new)
    best_time = sum(best_schedule[i].time for i in range(1, len(best_schedule)))
    return status, best_time, initial_list_size, len(best_schedule)


def main():
    task_list = load_tasks()
    print(optimize_single_set(task_list=task_list[400]))


if __name__ == '__main__':
    main()

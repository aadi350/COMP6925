import time
import csv
import logging
from  Task import Task
from tasks_gen import get_tasks

HIGH = 100
PRINT_LOGS = False
LOW = 70
WINDOW = 90
task_list = []


def load_tasks(file_path='tasks.csv'):
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


def optimize_single_set(task_list=task_list):
    status = None
    best_solution = 0
    best_schedule = None
    remaining_schedules = []
    start_time = time.perf_counter()
    print('Gen task:', task_list)
    task_list.sort(key=lambda x: x.priority, reverse=True)
    sort_time = time.perf_counter() - start_time
    logging.debug(task_list)

    for task in task_list:
        schedule = [task]
        remaining_schedules.append(schedule)

    for s in remaining_schedules:
        remaining_schedules.remove(s)
        for task in task_list:
            if task not in s:
                new_time = sum(s[i].time for i in range(1, len(s))) + task.time
                if new_time < WINDOW:
                    s_new = s
                    s_new.append(task)
                    priority_new = sum(s_new[i].priority for i in range(1, len(s_new)))
                    duration_new = sum(s_new[i].time for i in range(1, len(s_new)))
                    remaining_schedules.append(s_new)
                    if priority_new > best_solution:
                        best_solution = priority_new
                        best_schedule = s_new
                    # step-down processing power for last added task
                    logging.info('Fast time: {}'.format(s_new[-1].get_time()))
                    s_new[-1].set_processor(LOW)
                    if PRINT_LOGS: print('Slow time: {}'.format(s_new[-1].get_time()))
                    duration_step_down = sum(s_new[i].time for i in range(1, len(s_new)))
                    step_down_time = sum(s[i].time for i in range(1, len(s))) + task.time
                    if step_down_time > WINDOW:
                        logging.debug('Step down not feasible')
                        s_new[-1].set_processor(HIGH)
                    else:
                        logging.debug('Stepped-down')
                    status = 'Solution found'
                else:
                    status = 'Not feasible'
    print(status)
    end_time = time.perf_counter() - start_time
    print(best_solution)

    print(len(best_schedule), best_schedule)
    print(sum(best_schedule[i].time for i in range(1, len(best_schedule))))
    print(len(task_list))

    # timing
    print('Start: {}, Sort: {}, End: {}'.format(start_time, sort_time, end_time))


def main():
    load_tasks()
    optimize_single_set(task_list=task_list[100])


if __name__ == '__main__':
    main()

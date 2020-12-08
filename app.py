import csv
import logging

from Task import Task
from classic import optimize_single_classic

HIGH = 100
PRINT_LOGS = False
LOW = 70
WINDOW = 180


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
    best_schedule = 0
    remaining_schedules = []
    task_list.sort(key=lambda x: x.priority, reverse=False)

    for task in task_list:
        schedule = [task]
        remaining_schedules.append(schedule)

    s_new = None
    i = 0
    while len(remaining_schedules) > 0:
        if i > len(remaining_schedules) - 1:
            i = 0
        s = remaining_schedules[i]
        i += 1
        remaining_schedules.remove(s)
        logging.debug("Num remaining_schedules (rem)", len(remaining_schedules))
        if len(remaining_schedules) < 1:
            break
        task_list_i = 0
        for task in task_list:
            task_list_i += 1
            if task not in s:
                new_time = sum(s[i].cycles/s[i].freq for i in range(1, len(s))) + task.cycles/task.freq
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
                        best_schedule = s_new
                    status = True
                    remaining_schedules.append(s_new)
                else:
                    status = False

    if True:
        best_time = sum(best_schedule[i].time for i in range(len(best_schedule)))
        best_power = sum(best_schedule[i].freq*best_schedule[i].cycles for i in range(len(best_schedule)))
        return status, best_time, best_power, initial_list_size, len(best_schedule)

    return None


def main():
    tasks_list = load_tasks()
    with open('custom_stats.csv', 'w', newline='\n') as file:
        file_writer = csv.writer(file, delimiter=',')
        for task_list in tasks_list:
            temp = optimize_single_set(task_list=task_list)
            file_writer.writerow(temp)

    with open('classic_stats.csv', 'w', newline='\n') as file:
        file_writer = csv.writer(file, delimiter=',')
        for task_list in tasks_list:
            temp = optimize_single_classic(task_list=task_list)
            file_writer.writerow(temp)


if __name__ == '__main__':
    main()

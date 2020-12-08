import csv
from tasks_gen import get_tasks

NUM_ITERATIONS = 5

task_num = [10, 20, 30, 40, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
tasks_list = []
for i in range(len(task_num)):
    for j in range(NUM_ITERATIONS):
        tasks_list.append(get_tasks(task_num[i]))


with open('tasks.csv', 'w', newline='\n') as file:
    file_writer = csv.writer(file, delimiter=',')
    for task_list in tasks_list:
        file_writer.writerow(task_list)

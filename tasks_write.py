import csv
from tasks_gen import get_tasks

"""
    File is responsible for randomly generating set of normally-distributed tasks
    with means as defined in task_num for NUM_ITERATIONS
    Output is written to tasks.csv
"""

NUM_ITERATIONS = 25

task_num = [10,20,30,40,50,75,100,200,250]
print(task_num)
tasks_list = []
for i in range(len(task_num)):
    for j in range(NUM_ITERATIONS):
        tasks_list.append(get_tasks(task_num[i]))


with open('data/tasks.csv', 'w', newline='\n') as file:
    file_writer = csv.writer(file, delimiter=',')
    for task_list in tasks_list:
        file_writer.writerow(task_list)

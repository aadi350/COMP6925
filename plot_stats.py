import csv
import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
tasks = []
num_tasks = []
cat_avg = []
cat_var = []
with open('tasks.csv', 'r') as task_file:
    reader = csv.reader(task_file, delimiter=',')
    for row in reader:
        tasks.append(row)
        num_tasks.append(len(row))

    num_tasks = num_tasks[3:]
    for i in range(0, len(num_tasks), 5):
        # average number of tasks for each category
        cat_var.append(np.var(num_tasks[i:i + 5]))
        cat_avg.append(sum(num_tasks[i:i + 5]) / 5)

dist = []
for i in range(len(cat_var)):
    # table with means and variances of number of tasks per category
    dist.append([cat_avg[i], cat_var[i]])

# scheduling stats

df_classic = pd.read_csv('classic_stats.csv', delimiter=',', header=None)
df_custom = pd.read_csv('classic_stats.csv', delimiter=',', header=None)

num_scheduled = pd.concat([df_classic[3], df_custom[3]], axis=1)
num_scheduled_avg = num_scheduled.groupby(np.arange(len(num_scheduled)) // 5).mean()
task_num = pd.DataFrame([10, 20, 30, 40, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900])

num_scheduled_avg = pd.concat([num_scheduled_avg, task_num], axis=1)
num_scheduled_avg.columns = ['classic', 'custom', 'task_num']

import plotly.express as px

# fig = px.bar(num_scheduled_avg.iloc[:, 0:2],  labels=num_scheduled_avg['task_num'], barmode='group', height=400, width=800)
# fig.update_xaxes(title_text='Number of Tasks', showgrid=True, dtick=1)
# fig.update_yaxes(title_text='Number Scheduled', showgrid=True)
# fig.show()

mean_tasks = [20, 20, 20, 20, 20, 30, 30, 30, 30, 30, 40, 40, 40, 40, 40, 50, 50, 50, 50, 50, 100, 100, 100, 100, 100,
              200, 200, 200, 200, 200, 300, 300, 300, 300, 300, 400, 400, 400, 400, 400, 500, 500, 500, 500, 500, 600,
              600, 600, 600, 600, 700, 700, 700, 700, 700, 800, 800, 800, 800, 800, 900, 900, 900, 900, 900]

length_of_schedule = pd.concat([df_classic[1], df_custom[1], df_classic[3]], axis=1)[3:]
length_of_schedule.columns = ['classic', 'custom', 'num_tasks']
length_of_schedule['mean_tasks'] = mean_tasks

print(length_of_schedule)
length_of_schedule_avg = length_of_schedule.groupby(np.arange(len(length_of_schedule)) // 5).mean()
print(length_of_schedule_avg)

# fig = px.line(length_of_schedule_avg, x='num_tasks', y=['classic', 'custom'], height=400, width=800)
# fig.update_xaxes(title_text='Number of tasks', showgrid=True)
# fig.update_yaxes(title_text='Mean Execution Time', showgrid=True)
# fig.data[0].update(mode='markers+lines')
# fig.show()
ax = sns.boxplot(x=length_of_schedule['mean_tasks'], y=length_of_schedule['custom'])
ax.set(yscale='log')
plt.show()
fig = px.box(length_of_schedule, x='mean_tasks', y=['classic'], log_x=True, log_y=True, height=400, width=600)
fig.update_layout(boxgroupgap=0)
fig.show()

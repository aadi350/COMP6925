import csv
import pandas as pd
import numpy as np

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
    for i in range(0, len(num_tasks), 25):
        # average number of tasks for each category
        cat_var.append(np.var(num_tasks[i:i + 5]))
        cat_avg.append(sum(num_tasks[i:i + 5]) / 5)

dist = []
for i in range(len(cat_var)):
    # table with means and variances of number of tasks per category
    dist.append([cat_avg[i], cat_var[i]])

# scheduling stats

df_classic = pd.read_csv('classic_stats.csv', delimiter=',', header=None)
df_custom = pd.read_csv('custom_stats.csv', delimiter=',', header=None)

num_scheduled = pd.concat([df_classic[3].astype(int), df_custom[4].astype(int), df_custom[3].astype(int)], axis=1)
num_scheduled.columns = ['classic_num', 'custom_num', 'original_num']
num_scheduled = num_scheduled.sort_values(by='original_num')

num_scheduled_avg = num_scheduled.groupby(np.arange(len(num_scheduled)) // 5).mean()
print(num_scheduled_avg)

import plotly.express as px

fig = px.bar(num_scheduled_avg.iloc[:, 0:2],  labels=num_scheduled_avg['original_num'], barmode='group', height=400, width=800)
fig.update_xaxes(title_text='Number of Tasks', showgrid=True, dtick=1)
fig.update_yaxes(title_text='Number Scheduled', showgrid=True)
fig.show()

import pandas as pd
import plotly.express as px

with open('./data/stats_classic.txt', 'r') as file:
    line = file.readline().rstrip('\n')
    line_temp_2 = file.readline().rstrip('\n')
    line_temp_3 = file.readline().rstrip('\n')
    classic_stats = pd.DataFrame(columns=['num_tasks', 'fn_calls', 'time'])
    classic_stats = classic_stats.append({
        'num_tasks': line,
        'fn_calls': line_temp_2,
        'time': line_temp_3
    }, ignore_index=True)
    while line:
        line_1 = file.readline().rstrip('\n')
        line_2 = file.readline().rstrip('\n')
        line = file.readline().rstrip('\n')
        new_row = pd.Series(data={
            'num_tasks': line_1,
            'fn_calls': line_2,
            'time': line
        })
        classic_stats = classic_stats.append(new_row, ignore_index=True)
    classic_stats = classic_stats[:-1]

with open('./data/stats_custom.txt', 'r') as file:
    line = file.readline().rstrip('\n')
    line_temp_2 = file.readline().rstrip('\n')
    line_temp_3 = file.readline().rstrip('\n')
    custom_stats = pd.DataFrame(columns=['num_tasks', 'fn_calls', 'time'])
    custom_stats = custom_stats.append({
        'num_tasks': line,
        'fn_calls': line_temp_2,
        'time': line_temp_3
    }, ignore_index=True)
    while line:
        line_1 = file.readline().rstrip('\n')
        line_2 = file.readline().rstrip('\n')
        line = file.readline().rstrip('\n')
        new_row = pd.Series(data={
            'num_tasks': line_1,
            'fn_calls': line_2,
            'time': line
        })
        custom_stats = custom_stats.append(new_row, ignore_index=True)
    custom_stats = custom_stats[:-1]

time = pd.DataFrame(data={
    'num_tasks': classic_stats.num_tasks,
    'classic_time': classic_stats.time,
    'custom_time': custom_stats.time
})
time = time.astype(float)
time.num_tasks = time.num_tasks.astype(int)
time = time.sort_values(by=['num_tasks'], ignore_index=True, ascending=True)

fn_calls = pd.DataFrame(data={
    'num_tasks': classic_stats.num_tasks,
    'classic_fn_calls': classic_stats.fn_calls,
    'custom_fn_calls': custom_stats.fn_calls
})
fn_calls = fn_calls.astype(float)
fn_calls.num_tasks = fn_calls.num_tasks.astype(int)
fn_calls = fn_calls.sort_values(by=['num_tasks'], ignore_index=True, ascending=True)


ratio = pd.DataFrame(data={
    'num_tasks': classic_stats.num_tasks.astype(float),
    'classic_ratio': classic_stats.fn_calls.astype(float)/classic_stats.num_tasks.astype(float),
    'custom_ratio': custom_stats.fn_calls.astype(float)/classic_stats.num_tasks.astype(float)
})

ratio = ratio.sort_values(by=['num_tasks'], ignore_index=True, ascending=True)

fig_ratio = px.line(ratio, x='num_tasks', y=['classic_ratio', 'custom_ratio'], log_x=False, log_y=False)
fig_ratio.update_yaxes(title='Ratio of Function Calls to Number of Tasks')
fig_ratio.update_xaxes(title='Number of Tasks')
fig_ratio.update_layout(title='Ratio of Function Calls to Number of Tasks')
fig_ratio.show()


time_ratio = pd.DataFrame(data={
    'num_tasks': classic_stats.num_tasks.astype(float),
    'classic_ratio': classic_stats.time.astype(float)/classic_stats.num_tasks.astype(float),
    'custom_ratio': custom_stats.time.astype(float)/classic_stats.num_tasks.astype(float)
})

time_ratio = time_ratio.sort_values(by=['num_tasks'], ignore_index=True, ascending=True)

fig_time_ratio = px.line(time_ratio, x='num_tasks', y=['classic_ratio', 'custom_ratio'], log_x=False, log_y=False)
fig_time_ratio.update_yaxes(title='Ratio of Time to Number of Tasks')
fig_time_ratio.update_xaxes(title='Number of Tasks')
fig_time_ratio.update_layout(title='Ratio of Time to Number of Tasks')
fig_time_ratio.show()

print(time[:25])

print(fn_calls[:25])

fig = px.line(fn_calls, x='num_tasks', y='custom_fn_calls', log_x=False, log_y=False)
fig.update_yaxes(title='Time')
fig.update_xaxes(title='Number of Tasks')
fig.update_layout(title='Custom Function Calls')
fig.show()

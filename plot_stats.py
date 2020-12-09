import csv
import math
import pandas as pd
import numpy as np

tasks = []
PROCESSOR_FREQ = 30
SCHEDULE_WINDOW = 900
num_tasks = []
cat_avg = []
cat_var = []
with open('data/tasks.csv', 'r') as task_file:
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

df_classic = pd.read_csv('data/classic_stats.csv', delimiter=',', header=None)
df_custom = pd.read_csv('data/custom_stats.csv', delimiter=',', header=None)

num_scheduled = pd.concat([df_classic[3].astype(int), df_custom[4].astype(int), df_custom[3].astype(int)], axis=1)
num_scheduled.columns = ['classic_num', 'custom_num', 'original_num']
num_scheduled = num_scheduled.sort_values(by='original_num')

num_scheduled_avg = num_scheduled.groupby(np.arange(len(num_scheduled)) // 25).mean()
print(num_scheduled_avg)

import plotly.express as px

fig = px.bar(num_scheduled_avg, x='original_num', y=['classic_num', 'custom_num'], barmode='group', height=400,
             width=600)
fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=num_scheduled_avg.original_num
    )
)
fig.update_xaxes(title_text='Number of Tasks', showgrid=True, dtick=1)
fig.update_yaxes(title_text='Number Scheduled', showgrid=True)
fig.update_layout(title='Number of Tasks Scheduled')
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

custom_stats.time = custom_stats.time.astype(float)
classic_stats.time = classic_stats.time.astype(float)

time = pd.DataFrame(data={
    'num_tasks': classic_stats.num_tasks,
    'classic_time': classic_stats.time * PROCESSOR_FREQ,
    'custom_time': custom_stats.time * PROCESSOR_FREQ
})
time = time.astype(float)
time.num_tasks = time.num_tasks.astype(int)
time = time.sort_values(by=['num_tasks'], ignore_index=True, ascending=True)

fig_time_both = px.line(time, x='num_tasks', y=['classic_time', 'custom_time'], log_x=False, log_y=False)
fig_time_both.update_yaxes(title='Time Taken')
fig_time_both.update_xaxes(title='Number of Tasks')
fig_time_both.update_layout(title='Time taken to Number of Tasks')
fig_time_both.show()

classic_time_max_num = 1
classic_time_max_num_y = 1
for i in range(len(time)):
    if math.isclose(time['classic_time'][i], SCHEDULE_WINDOW, rel_tol=0.1):
        classic_time_max_num_y = time.iloc[i]['classic_time']
        classic_time_max_num = time.iloc[i]['num_tasks']

fig_time_classic = px.line(time, x='num_tasks', y=['classic_time'], log_x=False, log_y=True)
if classic_time_max_num_y != 1:
    fig_time_classic.add_annotation(x=classic_time_max_num, y=math.log10(classic_time_max_num_y),
                                    text="Maximum Number of Tasks: " + str(classic_time_max_num),
                                    showarrow=True,
                                    arrowhead=1)

fig_time_classic.update_yaxes(title='Time Taken')
fig_time_classic.update_xaxes(title='Number of Tasks')
fig_time_classic.update_layout(title='Time taken to Number of Tasks')
fig_time_classic.show()

fig_time_custom = px.line(time, x='num_tasks', y=['custom_time'], log_x=False, log_y=True)
fig_time_custom.update_yaxes(title='Time Taken')
fig_time_custom.update_xaxes(title='Number of Tasks')
fig_time_custom.update_layout(title='Time taken to Number of Tasks')


custom_time_max_num = -1
custom_time_max_num_y = -1
for i in range(len(time)):
    if math.isclose(time['custom_time'][i], SCHEDULE_WINDOW, rel_tol=0.1):
        custom_time_max_num_y = time.iloc[i]['custom_time']
        custom_time_max_num = time.iloc[i]['num_tasks']

fig_time_custom.add_annotation(x=custom_time_max_num, y=math.log10(custom_time_max_num_y),
                               text="Maximum Number of Tasks: " + str(custom_time_max_num),
                               showarrow=True,
                               arrowhead=1)

fig_time_custom.show()

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
    'classic_ratio': classic_stats.fn_calls.astype(float) / classic_stats.num_tasks.astype(float),
    'custom_ratio': custom_stats.fn_calls.astype(float) / classic_stats.num_tasks.astype(float)
})

ratio = ratio.sort_values(by=['num_tasks'], ignore_index=True, ascending=True)

fig_ratio = px.line(ratio, x='num_tasks', y=['classic_ratio', 'custom_ratio'], log_x=False, log_y=False)
fig_ratio.update_yaxes(title='Ratio of Function Calls to Number of Tasks')
fig_ratio.update_xaxes(title='Number of Tasks')
fig_ratio.update_layout(title='Ratio of Function Calls to Number of Tasks')
fig_ratio.show()

time_ratio = pd.DataFrame(data={
    'num_tasks': classic_stats.num_tasks.astype(float),
    'classic_ratio': (classic_stats.time.astype(float) * PROCESSOR_FREQ) / classic_stats.num_tasks.astype(float),
    'custom_ratio': (custom_stats.time.astype(float) * PROCESSOR_FREQ) / classic_stats.num_tasks.astype(float)
})

time_ratio = time_ratio.sort_values(by=['num_tasks'], ignore_index=True, ascending=True)

fig_time_ratio = px.line(time_ratio, x='num_tasks', y=['classic_ratio', 'custom_ratio'], log_x=False, log_y=False)
fig_time_ratio.update_yaxes(title='Ratio of Time to Number of Tasks')
fig_time_ratio.update_xaxes(title='Number of Tasks')
fig_time_ratio.update_layout(title='Ratio of Time to Number of Tasks')
fig_time_ratio.show()

print(time[:25])

print(fn_calls[:25])

fig_custom_fn = px.line(fn_calls, x='num_tasks', y='custom_fn_calls', log_x=False, log_y=False)
fig_custom_fn.update_yaxes(title='Function Calls')
fig_custom_fn.update_xaxes(title='Number of Tasks')
fig_custom_fn.update_layout(title='Custom Function Calls')
fig_custom_fn.show()

fig_classic_fn = px.line(fn_calls, x='num_tasks', y='classic_fn_calls', log_x=False, log_y=False)
fig_classic_fn.update_yaxes(title='Function Calls')
fig_classic_fn.update_xaxes(title='Number of Tasks')
fig_classic_fn.update_layout(title='Classic Function Calls')
fig_classic_fn.show()

fn_calls['ratio'] = (fn_calls.classic_fn_calls / fn_calls.custom_fn_calls).astype(float)

fig_fn_ratio_compared = px.line(fn_calls, x='num_tasks', y='ratio', log_x=True, log_y=False)
fig_fn_ratio_compared.update_yaxes(title='Function Calls Ratio')
fig_fn_ratio_compared.update_xaxes(title='Number of Tasks')
fig_fn_ratio_compared.update_layout(title='Ratio of Number of Function Calls')
fig_fn_ratio_compared.show()

import pandas as pd

def retrive_chart_data(obj):
    '''
    Retrives data formated in a list. The functions search through the existing
    task-objects and retrives the total amount of time used and the task name
    in a list format.
    ---------------------------------------------------------------------------
    obj: Object - Object instance of the ProjectModel
    '''
    tasks = obj.task.all()
    data = []
    labels = []
    for task in tasks:
        time = pd.to_timedelta(task.total)
        hours = time.seconds//3600
        data.append(hours)
        labels.append(task.task)
    return data,labels

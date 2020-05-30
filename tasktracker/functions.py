import pandas as pd
import numpy as np
from datetime import date,time,timedelta

def convert_to_str(df,column_name):
    '''
    Converts a dataframe containing timedelta to str data
    -----------------------------------------------------
    df - DataFrame
    column_name: String - The name of the column to be converted
    '''
    to_str =[]
    for x in df[column_name].to_list():
        to_str.append(str(x))
    df[column_name]=to_str
    return df

def convert_to_timedelta(df,column_name):
    '''
    Converts a dataframe containing str's to timedelta data
    -----------------------------------------------------
    df - DataFrame
    obj - Object containg the task name
    '''
    to_timedelta =[]
    for x in df[column_name].to_list():
        to_timedelta.append(pd.to_timedelta(x))
    df[column_name]=to_timedelta
    return df

def update_total_avgtotal(proj_obj,task_obj=False):
    """
    If task_obj is not provided then the function updates the total and average
    daily total for the ProjectModel for all tasks. If a task is provided the
    function will subtract the time, used in deleteview for TaskModel.
    --------------------------------------------------------------
    proj_obj: Object - Instance of the ProjectModel
    task_obj: Object - Instance of the TaskModel
    """
    if task_obj == False:
        tasks = proj_obj.task.all()
        total = timedelta()
        avg = timedelta()
        for task in tasks:
            total += pd.to_timedelta(task.total)
            avg += pd.to_timedelta(task.daily_avg)
        proj_obj.project_total = total
        proj_obj.project_avg = avg
        proj_obj.save()
    else:
        proj_obj = task_obj.project
        proj_obj.project_total -= pd.to_timedelta(task_obj.total)
        proj_obj.project_avg -= pd.to_timedelta(task_obj.daily_avg)
        proj_obj.save()



def project_dataframe(obj):
    """
    Merge all the different task dataframes to one dataframe.
    """
    tasks = obj.task.all()
    concat_list=[]
    for task in tasks:
        concat_list.append(pd.read_json(task.dataframe))
    df = pd.concat(concat_list,axis=1,sort=True)
    df.fillna('0',inplace=True)
    return df

def format_timedelta(td):
    days = td.days
    hours = td.seconds//3600
    minutes = (td.seconds//60)%60
    ## format text
    day_text = 'day'
    hour_text = 'hour'
    minute_text = 'minute'
    if days > 1:
        day_text='days'
    if hours > 1:
        hour_text = 'hours'
    if minutes > 1:
        minute_text = 'minutes'
    if days == 0:
        return '{} {} {} {}'.format(hours,hour_text,minutes,minute_text)
    else:
        return '{} {} {} {} {} {}'.format(days,day_text,hours,hour_text,minutes,minute_text)

def format_timedelta_task(td):
    """
    Formats the the timedelta to display better timedelta
    -----------------------------------------------------
    td = Obj - TimeDelta Object
    """
    days = td.days
    hours = td.seconds//3600
    minutes = (td.seconds//60)%60
    ## format text
    day_text = 'D'
    hour_text = 'H'
    minute_text = 'M'
    if days == 0:
        return '{} h {} min '.format(hours,minutes)
    else:
        return '{} d {} h {} min '.format(days,hours,minutes)

def update_display_text_task(task_obj):
    """
    Updates the TaskModels display attributes to be more readable
    -----------------------------------------------------
    td = Obj - TimeDelta Object
    """
    task_obj.display_avg = format_timedelta_task(pd.to_timedelta(task_obj.daily_avg))
    task_obj.display_total = format_timedelta_task(pd.to_timedelta(task_obj.total))
    task_obj.save()

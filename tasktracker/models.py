from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import JSONField
import pandas as pd
from django.urls import reverse
from datetime import date,time,timedelta
from tasktracker.functions import convert_to_str,convert_to_timedelta,format_timedelta
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class ProjectModel(models.Model):
    #Color choices
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    ORANGE = 'orange'
    COLOR_CHOICES = [(RED,'Red'),(BLUE,'Blue'),(GREEN,'Green'),(ORANGE,'Orange')]

    user = models.ForeignKey(User,related_name='projects',on_delete=models.CASCADE)
    project = models.CharField(max_length=100, primary_key=True)
    color = models.CharField(max_length=10,choices=COLOR_CHOICES,default=GREEN)
    description = models.CharField(max_length=500,blank=True,null=True)
    dataframe = JSONField(blank=True,null=True)
    #Summaryinformation
    project_total = models.DurationField(blank=True,null=True)
    project_avg = models.DurationField(blank=True,null=True)


    def __str__(self):
        return self.project

    def get_absolute_url(self):
        return reverse('home')

    def print_total(self):
        return format_timedelta(self.project_total)

    def print_avg(self):
        return format_timedelta(self.project_avg)

class TaskModel(models.Model):
    project = models.ForeignKey(ProjectModel,related_name='task',on_delete=models.CASCADE)
    task = models.CharField(max_length=100)
    duration = models.DurationField(blank=True,null=True)
    custom_duration = models.DurationField(blank=True,null=True)
    daily_avg = models.CharField(max_length=100,blank=True,null=True,default=str(timedelta(0)))
    total = models.CharField(max_length=100,blank=True,null=True,default=str(timedelta(0)))
    display_avg = models.CharField(max_length=100,blank=True,null=True)
    display_total = models.CharField(max_length=100,blank=True,null=True)
    dataframe = dataframe = JSONField(blank=True,null=True)

    def __str__(self):
        return self.task

    def get_absolute_url(self):
        task_project = self.project
        obj = ProjectModel.objects.get(project=task_project)
        return reverse('tasktracker:projectdetail', kwargs={'pk':obj.pk})

    def click(self, *args, **kwargs):
        today = date.today()
        if self.dataframe == None:
            #Dataframe has not been created yet
            df = pd.DataFrame(index=[today],data=[self.duration],columns=[self.task])
            self.total = str(df[self.task].sum())
            self.daily_avg = str(df[self.task].sum()/len(df.index))
            #Convert dataframe data to strings before dumping to JSON format
            df = convert_to_str(df,self.task)
            self.dataframe = df.to_json()
            self.save()
        else:
            df = pd.read_json(self.dataframe)
            df = convert_to_timedelta(df,self.task)
            if today in df.index.to_list():
                #Update the row containg todays date
                df.loc[today][self.task] = df.loc[today][self.task]+self.duration
                self.total = str(df[self.task].sum())
                self.daily_avg = str(df[self.task].sum()/len(df.index))
                #Convert dataframe data to strings before dumping to JSON format
                df = convert_to_str(df,self.task)
                self.dataframe = df.to_json()
                self.save()
            else:
                #Create a new row containing todays date
                new_row = pd.DataFrame(index=[today],data=[self.duration],columns=[self.task])
                df=pd.concat([df,new_row])
                self.total = str(df[self.task].sum())
                self.daily_avg = str(df[self.task].sum()/len(df.index))
                df = convert_to_str(df,self.task)
                self.dataframe = df.to_json()
                self.save()

    def add_custom(self, *args, **kwargs):
        today = date.today()
        if self.dataframe == None:
            #Dataframe has not been created yet
            df = pd.DataFrame(index=[today],data=[self.custom_duration],columns=[self.task])
            self.total = str(df[self.task].sum())
            self.daily_avg = str(df[self.task].sum()/len(df.index))
            #Convert dataframe data to strings before dumping to JSON format
            df = convert_to_str(df,self.task)
            self.dataframe = df.to_json()
            self.save()
        else:
            df = pd.read_json(self.dataframe)
            df = convert_to_timedelta(df,self.task)
            if today in df.index.to_list():
                #Update the row containg todays date
                df.loc[today][self.task] = df.loc[today][self.task]+self.custom_duration
                self.total = str(df[self.task].sum())
                self.daily_avg = str(df[self.task].sum()/len(df.index))
                #Convert dataframe data to strings before dumping to JSON format
                df = convert_to_str(df,self.task)
                self.dataframe = df.to_json()
                self.save()
            else:
                #Create a new row containing todays date
                new_row = pd.DataFrame(index=[today],data=[self.custom_duration],columns=[self.task])
                df=pd.concat([df,new_row])
                self.total = str(df[self.task].sum())
                self.daily_avg = str(df[self.task].sum()/len(df.index))
                df = convert_to_str(df,self.task)
                self.dataframe = df.to_json()
                self.save()

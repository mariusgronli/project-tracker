from django.shortcuts import render
from tasktracker.forms import (CreateProjectForm,AddCustomTimeForm,
    UpdateTaskForm,CreateTaskForm)
from django.urls import reverse,reverse_lazy
from tasktracker.models import ProjectModel,TaskModel
from django.shortcuts import get_object_or_404
from django.views.generic import (TemplateView,ListView,DetailView,UpdateView,
    CreateView,DeleteView,RedirectView)
from tasktracker.functions import (update_total_avgtotal,
    project_dataframe,update_display_text_task)
from tasktracker.chart_functions import retrive_chart_data
from django.contrib.auth.mixins import LoginRequiredMixin
from io import BytesIO as IO
from django.http import HttpResponse
from django.views import View
import pandas as pd


# Create your views here.
class ProjectListView(LoginRequiredMixin,ListView):
    model = ProjectModel
    context_object_name='project'
    template_name='tasktracker/index.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        User = self.request.user
        projects = User.projects.all()

        context.update({
            'user_projects':projects,
            })
        return context

class ProjectDetailView(LoginRequiredMixin,DetailView):
    model = ProjectModel
    context_object_name = 'project'
    template_name='tasktracker/processes.html'

class FullReportView(LoginRequiredMixin,DetailView):
    model = ProjectModel
    context_object_name = 'project'
    template_name='tasktracker/report.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(FullReportView, self).get_context_data(**kwargs)
        project = get_object_or_404(ProjectModel,pk=pk)
        data, labels = retrive_chart_data(project)
        context.update({
            'chart_data':data,
            'chart_labels':labels,
            })
        return context

class ExcelFileDownload(LoginRequiredMixin,DetailView):
    model = ProjectModel
    context_object_name = 'project'
    template_name = 'tasktracker/download.html'

    def get(self, request, *args, **kwargs):
        obj = ProjectModel.objects.get(pk=self.kwargs['pk'])
        excel_file = IO()
        xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        df = project_dataframe(obj)
        df.to_excel(xlwriter, "Summary")
        xlwriter.save()
        xlwriter.close()

        excel_file.seek(0)

        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename="excel_file.xlsx"'
        return response

##############################################
############## CRUD Views#####################
##############################################

############### Project Model ################
class CreateProjectView(LoginRequiredMixin,CreateView):
    form_class= CreateProjectForm
    model = ProjectModel
    template_name = 'tasktracker/crud/projectmodel_form.html'

    def get_absolute_url(self):
        return reverse('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class UpdateProjectView(LoginRequiredMixin,UpdateView):
    form_class = CreateProjectForm
    model = ProjectModel
    template_name = 'tasktracker/crud/update_projectmodel.html'

class DeleteProjectView(LoginRequiredMixin,DeleteView):
    model = ProjectModel
    template_name = 'tasktracker/crud/project_confirm_delete.html'
    success_url = reverse_lazy('home')

class ClickRedirectView(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        task = get_object_or_404(TaskModel, pk=kwargs['pk'])
        obj = ProjectModel.objects.get(project=task.project)
        return reverse('tasktracker:projectdetail', kwargs={'pk':obj.pk})

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(TaskModel,pk=self.kwargs.get("pk"))
        task.click()
        proj = task.project
        update_display_text_task(task)
        update_total_avgtotal(proj)
        return super().get(request, *args, **kwargs)

############## Task Model ######################


class CreateTaskView(LoginRequiredMixin,CreateView):
    form_class= CreateTaskForm
    model = TaskModel
    template_name = 'tasktracker/crud/taskmodel_form.html'

    def get_absolute_url(self):
        return reverse('home')

    def get_form_kwargs(self):
        kwargs = super(CreateTaskView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class AddCustomTimeView(LoginRequiredMixin,UpdateView):
    form_class= AddCustomTimeForm
    model = TaskModel
    template_name = 'tasktracker/crud/addtime_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=True)
        self.object.add_custom()
        update_display_text_task(self.object)
        return super().form_valid(form)

class UpdateTaskView(LoginRequiredMixin,UpdateView):
    form_class=UpdateTaskForm
    model = TaskModel
    template_name = 'tasktracker/crud/update_task_form.html'

class DeleteTaskView(LoginRequiredMixin,DeleteView):
    model = TaskModel
    template_name = 'tasktracker/crud/task_confirm_delete.html'
    success_url = reverse_lazy('home')

    def delete(self, *args, **kwargs):
        task = self.get_object()
        proj = task.project
        update_total_avgtotal(proj,task)
        return super(DeleteTaskView, self).delete(*args, **kwargs)

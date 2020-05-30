from django.contrib import admin
from django.urls import path
from tasktracker import views

app_name = 'tasktracker'

urlpatterns=[
    path('processes/<str:pk>/',views.ProjectDetailView.as_view(),name='projectdetail'),
    path('createproject/',views.CreateProjectView.as_view(),name='createproject'),
    path('createtask/',views.CreateTaskView.as_view(),name='createtask'),
    path('click/<str:pk>/',views.ClickRedirectView.as_view(),name='click'),
    path('report/<str:pk>/',views.FullReportView.as_view(),name='report'),
    path('download/<str:pk>/',views.ExcelFileDownload.as_view(),name='download'),
    path('addtime/<int:pk>/',views.AddCustomTimeView.as_view(),name='addtime'),
    path('update/<int:pk>/',views.UpdateTaskView.as_view(),name='updatetask'),
    path('delete/<int:pk>/',views.DeleteTaskView.as_view(),name='deletetask'),
    path('update/<str:pk>/', views.UpdateProjectView.as_view(),name='updateproject'),
    path('delete/<str:pk>/',views.DeleteProjectView.as_view(),name='deleteproject'),
]

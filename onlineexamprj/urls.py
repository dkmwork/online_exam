"""onlineexamprj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from onlineexamapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.examform,name='exam'),
    path('center',views.centerform,name='center'),
    path('subject',views.subjectform,name='subject'),
    path('examsubject', views.exam_subjectform,name='examsubject'),
    path('question',views.questionform,name='question'),
    path('questionexam',views.question_examform,name='questionexam'),
    path('questionoption',views.question_optionform, name='questionoption'),
    path('questionanswer',views.question_answerform,name='questionanswer'),
    #path('examlist',views.examlist,name='examlist'),
    #path('examsearchinfo',views.examsearchinfo,name="examsearchinfo"),
    path('examedit/<int:examid>',views.exam_edit,name='examedit'),
    path('centerlist',views.centerlist,name='centerlist'),
    path('centeredit/<int:centerid>',views.center_edit,name='centeredit'),
    #path('subjectlist',views.subjectlist,name='subjectlist'),
    path('subjectedit/<int:subjectid>', views.subject_edit,name='subjectedit'),
    #path('examsearchpagination',views.examsearchpagination,name="examsearchpagination"),
    path('examlistpagination',views.examlistpagination,name='examlistpagination'),
    path('subjectlistpagination',views.subjectlistpagination,name='subjectlistpagination'),
    path('examsubject_bridgelist',views.examsubject_bridgelist,name='examsubject_bridgelist'),
    path('examsubject_edit/<int:es_id>',views.examsubject_edit,name='examsubject_edit'),
    path('questionlist',views.questionlist,name="questionlist"),
    path('question_edit/<int:questionid>',views.question_edit,name='question_edit'),
    path('questionexam_bridgelist',views.questionexam_bridgelist,name='questionexam_bridgelist'),
    path('questionexam_bridgeedit/<int:qebridgeid>',views.questionexam_bridgeedit,name='questionexam_bridgeedit'),
    path('question_optionlist',views.question_optionlist,name='question_optionlist'),
    path('questionoption_edit/<int:questionid>',views.questionoption_edit,name='questionoption_edit'),
    path('qexam_answerbridge_list',views.qexam_answerbridge_list,name='qexam_answerbridge_list'),
    path('questionanswer_edit/<int:qabridgeid>',views.questionanswer_edit,name='questionanswer_edit'),
    #path('answer_sheetform',views.answer_sheetform,name='answer_sheetform'),
    #path('student_exam_flagform',views.student_exam_flagform,name='student_exam_flagform'),
    path('exam_papermodified',views.exam_papermodified2,name='exam_papermodified'),
]

from django.db import models
import re
from django.core.exceptions import ValidationError
from django.db.models import Q

class Exam(models.Model):
    exam_id=models.IntegerField(primary_key=True,auto_created=True)
    type_choices=(("Descriptive","Descriptive"),("Lab","Lab"),("Multiple_choice","Multiple_choice"))
    
    level_choices=(("National","National"),("State","State"),("Local","Local"))
    exam_name=models.CharField(max_length=65,null=False,blank=False,unique=True)
    exam_code=models.CharField(max_length=40,null=False,blank=False,unique=True)
    exam_is_cat=models.BooleanField()
    exam_duration=models.CharField(max_length=10,null=False,blank=False)
    exam_no_questions=models.IntegerField(null=False,blank=False)
    exam_cut_of_mark=models.IntegerField(null=False,blank=False)
    exam_level=models.CharField(max_length=40,choices=level_choices, null=False,blank=False)      		
    exam_time=models.TimeField(null=False)
    exam_date=models.DateField(null=False)
    exam_year=models.IntegerField(null=True,blank=True)
    exam_type=models.CharField(max_length=20,choices=type_choices,verbose_name="Type")
    is_active=models.BooleanField(null=False,blank=False,default=True)
	
    def __str__(self):
        return f"{self.exam_name} {str(self. exam_year)}"

class Center(models.Model):
    center_id=models.IntegerField(primary_key=True,auto_created=True)
    center_name=models.CharField(max_length=40,null=False,blank=False,unique=True)
    center_code=models.CharField(max_length=40,null=False,blank=False,unique=True)
    center_capacity=models.IntegerField(null=False,blank=False,unique=True)
    is_active=models.BooleanField(null=False,blank=False,default=True)
	
    def __str__(self):
        return self.center_name

class Subject(models.Model):
    subject_id=models.IntegerField(primary_key=True,auto_created=True)
    category_choice=(("Arts","Arts"),("Science","Science"),("Language","Language"),("Management","Management"),("Technology","Technology"))
    subject_name=models.CharField(max_length=40,null=False,blank=False,unique=True)
    subject_code=models.CharField(max_length=40,null=False,blank=False,unique=True)
    subject_category=models.CharField(max_length=40,choices=category_choice,verbose_name="Category")
    is_active=models.BooleanField(null=False,blank=False,default=True)
	
    def __str__(self):
        return self.subject_name

class Exam_Subject_Bridge(models.Model):
    esbridge_id=models.IntegerField(primary_key=True,auto_created=True)
    exam=models.ForeignKey(Exam,related_name="exam_subject_bridge",on_delete=models.PROTECT)
    subject=models.ForeignKey(Subject,related_name="exam_subject_bridge",on_delete=models.PROTECT)
    no_questions=models.IntegerField(null=False,blank=False)
    is_active=models.BooleanField(null=False,blank=False,default=True)
	
    def __str__(self):
        return f"{self.exam} {self.subject}"

class Question_Master(models.Model):
    question_id=models.IntegerField(primary_key=True,auto_created=True)
    difficulty_level_choices=(("Easy","Easy"),("Medium","Medium"),("Difficult","Difficult"))
    type_choices=(("Descriptive","Descriptive"),("Lab","Lab"),("Multiple_choice","Multiple_choice"))
    question=models.CharField(max_length=120,null=False,blank=False,unique=True)
    question_difficulty_level=models.CharField(max_length=20,choices=difficulty_level_choices,verbose_name="Level")
    question_type=models.CharField(max_length=20,choices=type_choices,verbose_name="Type")
    max_no_option=models.IntegerField(blank=True,null=True,default=1)
    question_subject=models.ForeignKey(Subject,null=False,related_name="question_master",on_delete=models.PROTECT)
    is_active=models.BooleanField(null=False,blank=False,default=True)
	
    def __str__(self):
        return self.question

class Question_Exam_Bridge(models.Model):
    qebridge_id=models.IntegerField(primary_key=True,auto_created=True)
    exam=models.ForeignKey(Exam,null=False,related_name="question_exam_bridge",on_delete=models.PROTECT)
    question=models.ForeignKey(Question_Master,null=False,related_name="question_exam_bridge",on_delete=models.PROTECT)
    marks_to_add=models.IntegerField(null=False,blank=False)
    marks_to_deduct=models.IntegerField(null=False,blank=False)
    is_active=models.BooleanField(null=False,blank=False,default=True)
	
    def __str__(self):
        return  f"{self.exam} {self.question}"

class Question_Option(models.Model):
    option_id=models.IntegerField(primary_key=True,auto_created=True)
    question=models.ForeignKey(Question_Master,related_name="question_option",on_delete=models.PROTECT)
    option=models.CharField(max_length=40,null=False,blank=False)
    
    is_active=models.BooleanField(null=False,blank=False,default=True)
	
    def __str__(self):
        return self.option

class Questions_Answer_bridge(models.Model):
    qabridge_id=models.IntegerField(primary_key=True,auto_created=True)
    qebridge_id=models.ForeignKey(Question_Exam_Bridge,blank=False,null=False,related_name="question_answer_bridge",on_delete=models.PROTECT)
    answer=models.ForeignKey(Question_Option,max_length=100,null=False,related_name="question_answer_bridge",on_delete=models.PROTECT)
    is_active=models.BooleanField(null=False,blank=False,default=True)
	
    def __str__(self):
        return self.answer.option

class Student(models.Model):
    studentid=models.IntegerField(primary_key=True,auto_created=True)
    studen_name=models.CharField(max_length=40,null=False,blank=False)
    email_id=models.CharField(max_length=40,null=False,blank=False,unique=True)

    def __str__(self):
        return self.email_id

class Answer_Sheet(models.Model):
    answer_sheetid=models.IntegerField(primary_key=True,auto_created=True)
    exam_date=models.DateField(null=False)
    sl_no=models.IntegerField()
    studentid=models.ForeignKey(Student,max_length=100,null=False,related_name="answer_sheet",on_delete=models.PROTECT)
    examid=models.ForeignKey(Exam,max_length=100,null=False,related_name="answer_sheet",on_delete=models.PROTECT)
    questionid=models.ForeignKey(Question_Master,max_length=100,null=False,related_name="answer_sheet",on_delete=models.PROTECT)
    student_answerid=models.ForeignKey(Question_Option,max_length=100,null=True,related_name="answer_sheet",on_delete=models.PROTECT,default=1)
    correct_answerid=models.ForeignKey(Questions_Answer_bridge,max_length=100,null=False,related_name="answer_sheet",on_delete=models.PROTECT)
    correct_answer=models.BooleanField(null=False,blank=False,default=True)
    marks=models.IntegerField(null=False,blank=False)
	
    def __str__(self):
        return f"{self.studentid} {self.examid}"    

class Student_Exam_Flag(models.Model):
    studentexam_id=models.IntegerField(primary_key=True,auto_created=True)
    level_choices=(("E","E"),("M","M"),("D","D"))
    studentid=models.ForeignKey(Student,max_length=100,null=False,related_name="student_exam_flag",on_delete=models.PROTECT)
    examid=models.ForeignKey(Exam,max_length=100,null=False,related_name="student_exam_flag",on_delete=models.PROTECT)
    level=models.CharField(max_length=20,choices=level_choices,verbose_name="Level")
    count_attempted_questions=models.IntegerField(null=False,blank=False)

    def __str__(self):
        return f"{self.studentid}{self.examid}"

class Exam_Paper(models.Model):
    exam_paperid=models.IntegerField(primary_key=True,auto_created=True)
    question=models.ForeignKey(Question_Exam_Bridge,max_length=100,null=False,related_name="exam_paper",on_delete=models.PROTECT)
    options=models.ForeignKey(Question_Option,max_length=100,null=False,related_name="exam_paper",on_delete=models.PROTECT)
    
    def __str__(self):
        return self.question



# Create your models here.



	
	
	
	

from django import forms
from django.forms import ModelForm
from django_select2 import forms as select2forms
from onlineexamapp.models import Exam
from onlineexamapp.models import (Exam,Center,Subject,Exam_Subject_Bridge,Question_Master,Question_Exam_Bridge,Question_Option,
Questions_Answer_bridge,Student,Answer_Sheet,Student_Exam_Flag,Exam_Paper)

class exam_modelform(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['exam_name'].widget.attrs.update({'autofocus':'autofocus'})
        self.fields['exam_date']=forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker','autocomplete':'off'}))
        self.fields['exam_time']=forms.TimeField(widget=forms.TimeInput(attrs={"type":"time"}))
    class Meta:
        model=Exam
        exclude=('exam_id','is_active')

class center_modelform(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['center_name'].widget.attrs.update({'autofocus':'autofocus'})
    class Meta:
        model=Center
        exclude=('center_id','is_active')

class subject_modelform(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['subject_name'].widget.attrs.update({'autofocus':'autofocus'})
    class Meta:
        model=Subject
        exclude=('subject_id','is_active')

class examsubject_bridge_modelform(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['exam'].widget.attrs.update({'autofocus':'autofocus'})
    class Meta:
        model=Exam_Subject_Bridge
        exclude=('esbridge_id','is_active')

class question_master_modelform(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['question'].widget.attrs.update({'autofocus':'autofocus'})
    class Meta:
        model=Question_Master
        exclude=('question_id','is_active')

class questionexam_bridge_modelform(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['question'].widget.attrs.update({'autofocus':'autofocus'})
    class Meta:
        model=Question_Exam_Bridge
        exclude=('qebridge_id','is_active')

class questionoption_modelform(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #self['question'].widget.attrs.update({'autofocus':'autofocus'})
    class Meta:
        model=Question_Option
        exclude=('option_id','is_active')
        
class questionanswer_bridgemodelform(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #self['qabridge_id'].widget.attrs.update({'autofocus':'autofocus'})
    class Meta:
        model=Questions_Answer_bridge
        exclude=('qabridge_id','is_active')

class answersheet_modelform(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['exam_date']=forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker','autocomplete':'off'}))
        self.fields['exam_date'].widget.attrs.update({'autofocus':'autofocus'})
    class Meta:
        model=Answer_Sheet
        exclude=('answer_sheetid',)

class student_exam_flagmodelform(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['studentid'].widget.attrs.update({'autofocus':'autofocus'})
    class Meta:
        model=Student_Exam_Flag
        exclude=('studentexam_id',)

class exam_paper_modelform(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        
        #self.fields['question']=forms.MultipleChoiceField(widget=select2forms.Select2Widget(attrs={'class':'select2'}))
        #self.fields['option']=forms.ModelMultipleChoiceField(widget=select2forms.Select2MultipleWidget(attrs={'class':'select2','multiple':'multiple'}))
            #CHOICES =[('M','Male'),('F','Female')]
            
            #self.fields['options']=forms.ModelChoiceField(widget=forms.RadioSelect,queryset=CHOICES)
    class Meta:
        model=Exam_Paper
        exclude=('exam_paperid',)



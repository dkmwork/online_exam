from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q,Sum,DecimalField,Count
from django.conf import settings
from django.forms import modelformset_factory,inlineformset_factory
from django.http import JsonResponse,HttpResponse
from onlineexamapp.models import (Exam,Center,Subject,Exam_Subject_Bridge,Question_Master,Question_Exam_Bridge,Question_Option,
Questions_Answer_bridge,Student,Answer_Sheet,Student_Exam_Flag,Exam_Paper)
from onlineexamapp.forms import (exam_modelform,center_modelform,subject_modelform,examsubject_bridge_modelform,question_master_modelform,
questionexam_bridge_modelform,questionoption_modelform,questionanswer_bridgemodelform,student_exam_flagmodelform,answersheet_modelform,exam_paper_modelform)
from onlineexamapp.dboperations import insert_into_studentflag
from onlineexamapp.flagoperations import get_next_easyqn_and_options,get_next_mediumqn_and_options,get_next_difficultqn_and_options
def examform(request):
    template_name="onlineexamapp/exam.html"
    examform=exam_modelform()
    if request.method=="GET":
        context={"MyExam":examform}
        return render(request,template_name,context)
    elif request.method=="POST":
        examform=exam_modelform(request.POST)
        context={"MyExam":examform}
        if examform.is_valid():
            examform.save()
            examform=exam_modelform()
            context={"MyExam":examform}
            return render(request,template_name,context)
    return render(request,template_name,context)

def centerform(request):
    template_name="onlineexamapp/center.html"
    centerform=center_modelform()
    if request.method=="GET":
        context={"MyCenter":centerform}
        return render(request,template_name,context)
    elif request.method=="POST":
        centerform=center_modelform(request.POST)
        if centerform.is_valid():
            centerform.save()
        centerform=center_modelform()
        context={"MyCenter":centerform}
        return render(request,template_name,context)

def subjectform(request):
    template_name="onlineexamapp/subject.html"
    subjectform=subject_modelform()
    if request.method=="GET":
        context={"MySubject":subjectform}
        return render(request,template_name,context)
    elif request.method=="POST":
        subjectform=subject_modelform(request.POST)
        if subjectform.is_valid:
            subjectform.save()
        subjectform=subject_modelform()
        context={"MySubject":subjectform}
        return render(request,template_name,context)
    
def exam_subjectform(request):
    template_name="onlineexamapp/exam_subject_bridge.html"
    exam_subjectform=examsubject_bridge_modelform()
    if request.method=="GET":
        context={"ExamSubject":exam_subjectform}
        return render(request,template_name,context)
    elif request.method=="POST":
        
        exam_subjectform=examsubject_bridge_modelform(request.POST)
        if exam_subjectform.is_valid():
            #print("hi")
            exam_subjectform.save()
        exam_subjectform=examsubject_bridge_modelform()
        context={"ExamSubject":exam_subjectform}
        return render(request,template_name,context)

'''def exam_papermodified(request):
    template_name="onlineexamapp/exam_paper.html"
    exam='Reserve Bank of India Exam'
    exam_date='2022-04-01'
    examobj=Exam.objects.get(exam_name=exam)
    studentobj=Student.objects.get(studentid=2)
    questionlist=Question_Exam_Bridge.objects.filter(exam__exam_name=exam)
    total_mark = 0
    out_of_mark=0
    #print(questionlist[0].question)
    questionobj=questionlist[0].question
    new_list=[]
    optionlist=Question_Option.objects.filter(question__question=questionobj)
    for option in optionlist:
        new_list.append(option)
    if request.method=="GET":
        context={"Question":questionobj,"Options":new_list}
        return render(request,template_name,context)
    elif request.method=="POST":
        current_question=request.POST.get('question')
        current_question=current_question.lstrip().rstrip()
        questionobj=Question_Master.objects.get(question=current_question)
        selected_option=request.POST.get('opt')
        selected_optionobj=Question_Option.objects.get(option=selected_option)
        selected_answerobj=Questions_Answer_bridge.objects.get(qebridge_id=questionobj.question_id)
        answer_sheetmodel=Answer_Sheet()
        answer_sheetmodel.exam_date=exam_date
        answer_sheetmodel.studentid=studentobj
        answer_sheetmodel.examid=examobj
        answer_sheetmodel.questionid=questionobj
        answer_sheetmodel.student_answerid=selected_optionobj
        answer_sheetmodel.correct_answerid=selected_answerobj
        marks_dict=Question_Exam_Bridge.objects.filter(question=questionobj,exam=examobj).values('marks_to_add','marks_to_deduct')
        #print(marks_dict)
        out_of_mark = out_of_mark + marks_dict[0]['marks_to_add']

        if selected_optionobj.option == selected_answerobj.answer.option:
            answer_sheetmodel.correct_answer= True
            answer_sheetmodel.marks=marks_dict[0]['marks_to_add']
        else:
            answer_sheetmodel.correct_answer= False
            answer_sheetmodel.marks=marks_dict[0]['marks_to_deduct']
        answrsheetmodel_qryset=Answer_Sheet.objects.filter(exam_date=exam_date ,examid=examobj , studentid=studentobj)
        #print(answer_sheetmodel.marks)
        if len(answrsheetmodel_qryset) == 0:
            answer_sheetmodel.sl_no=1
        else:
            answer_sheetmodel.sl_no=len(answrsheetmodel_qryset)+1
        
        answer_sheetmodel.save()

        insert_into_studentflag(answer_sheetmodel)

        new_list=[]
        question_examlist= Question_Exam_Bridge.objects.filter(exam=examobj).values_list('question__question')
        #print(question_examlist)
        
        fromanswer_sheetlist= Answer_Sheet.objects.filter(examid=examobj).values_list('questionid__question')
        #print(fromanswer_sheetlist)
        remaining_questionlist=question_examlist.difference(fromanswer_sheetlist)
        #print(remaining_questionlist)
        #print(len(remaining_questionlist))
        if len(remaining_questionlist) > 0:
            question = remaining_questionlist[0][0]
            questionobj=Question_Master.objects.get(question=question)
        
            optionlist=Question_Option.objects.filter(question__question=questionobj)
            for option in optionlist:
                new_list.append(option)
        else:
            template_name="onlineexamapp/exam_mark.html"
            question ='Exam Ended'
            total_correctanswer = Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,correct_answer=True).aggregate(to_add=Sum('marks'))
            total_wronganswer = Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,correct_answer=False).aggregate(to_deduct=Sum('marks'))
            #print(total_correctanswer)
            #print(total_wronganswer)
            if total_correctanswer['to_add'] == None:
                total_mark = 0 - total_wronganswer['to_deduct']
            elif total_wronganswer['to_deduct'] == None:
                total_mark = total_correctanswer['to_add'] - 0
            else:
                total_mark = total_correctanswer['to_add'] - total_wronganswer['to_deduct']
            #print(total_mark)
            new_list=[]
            mark = total_mark
            out_of_mark=Question_Exam_Bridge.objects.filter(exam=examobj).aggregate(Sum('marks_to_add'))
            print(out_of_mark)
   
            context={"mark":total_mark,"total":out_of_mark['marks_to_add__sum']} 
            return render(request,template_name,context)

        
        context={"Question":question,"Options":new_list}
        return render(request,template_name,context)'''

def exam_papermodified2(request):
    template_name="onlineexamapp/exam_paper.html"
    exam='Reserve Bank of India Exam'
    exam_date='2022-04-01'
    examobj=Exam.objects.get(exam_name=exam)
    studentobj=Student.objects.get(studentid=2)
    questionlist=Question_Exam_Bridge.objects.filter(exam__exam_name=exam)
    total_mark = 0
    out_of_mark=0
    #print(questionlist[0].question)
    questionobj=questionlist[0].question
    new_list=[]
    optionlist=Question_Option.objects.filter(question__question=questionobj)
    for option in optionlist:
        new_list.append(option)
    if request.method=="GET":
        context={"Question":questionobj,"Options":new_list}
        return render(request,template_name,context)
    elif request.method=="POST":
        current_question=request.POST.get('question')
        current_question=current_question.lstrip().rstrip()
        questionobj=Question_Master.objects.get(question=current_question)
        
        selected_option=request.POST.get('opt')
        selected_optionobj=Question_Option.objects.get(option=selected_option)
        selected_answerobj=Questions_Answer_bridge.objects.get(qebridge_id=questionobj.question_id)
        answer_sheetmodel=Answer_Sheet()
        answer_sheetmodel.exam_date=exam_date
        answer_sheetmodel.studentid=studentobj
        answer_sheetmodel.examid=examobj
        answer_sheetmodel.questionid=questionobj
        answer_sheetmodel.student_answerid=selected_optionobj
        answer_sheetmodel.correct_answerid=selected_answerobj
        marks_dict=Question_Exam_Bridge.objects.filter(question=questionobj,exam=examobj).values('marks_to_add','marks_to_deduct')
        #print(marks_dict)
        out_of_mark = out_of_mark + marks_dict[0]['marks_to_add']
        #check the answer is correct or not to add the marks/deduct the marks
        if selected_optionobj.option == selected_answerobj.answer.option:
            answer_sheetmodel.correct_answer= True
            answer_sheetmodel.marks=marks_dict[0]['marks_to_add']
        else:
            answer_sheetmodel.correct_answer= False
            answer_sheetmodel.marks=marks_dict[0]['marks_to_deduct']
        answrsheetmodel_qryset=Answer_Sheet.objects.filter(exam_date=exam_date ,examid=examobj , studentid=studentobj)
        #print(answer_sheetmodel.marks)
        if len(answrsheetmodel_qryset) == 0:
            answer_sheetmodel.sl_no=1
        else:
            answer_sheetmodel.sl_no=len(answrsheetmodel_qryset)+1

        answer_sheetmodel.save()
        
        # create a corresponding flag accroding to the question difficulty level 
        #dboperations

        insert_into_studentflag(answer_sheetmodel) 
        new_list=[]
        #question_examlist= Question_Exam_Bridge.objects.filter(exam=examobj).values_list('question__question')
        #fromanswer_sheetlist= Answer_Sheet.objects.filter(examid=examobj).values_list('questionid__question')
        #remaining_questionlist=question_examlist.difference(fromanswer_sheetlist)

# get the exam key values(total no of questions, no of easy questions etc from settings.py)
        exam_variable_dict=settings.CUSTOM_VALUES[0]
        exam_constant_dict=exam_variable_dict['exam_constants']
        total_questions=exam_constant_dict.get("TOTAL_QUESTIONS")
        total_easy_question=exam_constant_dict.get("EASY_QN")
        total_medium_question=exam_constant_dict.get("MEDIUM_QN")
        total_difficult_question=exam_constant_dict.get("HARD_QN")

        attempted_question_count=Student_Exam_Flag.objects.filter(studentid=studentobj,examid=examobj).aggregate(total_attempted=Sum('count_attempted_questions')) 
        # check the whether reach the maximumum no of question in the exam, if it reaches display the result
        if attempted_question_count['total_attempted'] < total_questions:
            if questionobj.question_difficulty_level == "Easy":
                no_attempted_e=Student_Exam_Flag.objects.filter(studentid=studentobj,examid=examobj,level="E").values_list('count_attempted_questions')
                # check the no of flag table with difficulty level "E", if the it is 1 (the student still answering the first level of easy questions only) 
                if len(no_attempted_e) == 1:
                    #if no_attempted_e['count_attempted_questions'] < total_easy_question:
                    if no_attempted_e[0][0] < total_easy_question:
                        questionobj,new_list=get_next_easyqn_and_options(studentobj,examobj)

                    #elif no_attempted_e['count_attempted_questions'] == total_easy_question:
                    # check it reaches the maximum no of easy questions and of yes, then need to find all the answers are correct.
                    elif no_attempted_e[0][0] == total_easy_question:
                        # find any wrong answer in the answerlist
                        answerlist= Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,correct_answer=False)
                        if len(answerlist) == 0:
                            questionlist=Question_Exam_Bridge.objects.filter(exam__exam_name=exam,question__question_difficulty_level="Medium")
                            questionobj=questionlist[0].question
                            optionlist=Question_Option.objects.filter(question__question=questionobj)
                            for option in optionlist:
                                new_list.append(option)
                            # give him his first Medium question
                            
                        else:
                            #if no_attempted_e['count_attempted_questions'] < total_easy_question:
                            # found there is a wrong answer in the answerlist so giving the next easy question

                            questionobj,new_list=get_next_easyqn_and_options(studentobj,examobj)

                            
                            
                    #elif no_attempted_e['count_attempted_questions'] > total_easy_question:
                    elif no_attempted_e[0][0] > total_easy_question:
                        # the no of attempted qn  exceeds max no of easy question, so we need to check the answers are correct continuesly for 5.
                        # if the condition fails give again the easy question. 

                        latest_false_answerobj= Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,correct_answer=False,questionid__question_difficulty_level="Easy").last()
                        latest_false_answer_slno=latest_false_answerobj.sl_no
                        last_answer_slnoobj=Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,questionid__question_difficulty_level="Easy").last()
                        last_answer_slno=last_answer_slnoobj.sl_no

                        if last_answer_slno - latest_false_answer_slno == total_easy_question:
                            # give him his first Medium question
                            questionlist=Question_Exam_Bridge.objects.filter(exam__exam_name=exam,question__question_difficulty_level="Medium")
                            questionobj=questionlist[0].question
                            optionlist=Question_Option.objects.filter(question__question=questionobj)
                            for option in optionlist:
                                new_list.append(option) 
                            
                        else:
                            #if no_attempted_e['count_attempted_questions'] < total_easy_question:
                            # repeat the set of codes
                            questionobj,new_list=get_next_easyqn_and_options(studentobj,examobj)

                            
                else:
                    # check the answer is correct or not , if correct give next Medium qn
                    # if the current answer is wrong, then give the next Easy qn
                    if Answer_Sheet.objects.get(questionid=questionobj).correct_answer == True:
                        #print("I'm in easy again !!")
                        questionobjectlist = Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,questionid__question_difficulty_level="Medium").values_list('questionid__question')
                        questionlist_qn_exam=Question_Exam_Bridge.objects.filter(exam=examobj,question__question_difficulty_level="Medium").values_list('question__question')
                        next_questionlist=questionlist_qn_exam.difference(questionobjectlist)
                        question = next_questionlist[0][0]
                        questionobj=Question_Master.objects.get(question=question)
                        optionlist=Question_Option.objects.filter(question__question=questionobj)
                        for option in optionlist:
                            new_list.append(option)
                    else:

                        questionobj,new_list=get_next_easyqn_and_options(studentobj,examobj)     

            elif questionobj.question_difficulty_level == "Medium":

                if Answer_Sheet.objects.get(questionid=questionobj).correct_answer == False:
                    if len(Student_Exam_Flag.objects.filter(studentid=studentobj,examid=examobj,level="D")) == 0:
                        questionobj,new_list=get_next_easyqn_and_options(studentobj,examobj)
                    else:
                        questionobj,new_list=get_next_mediumqn_and_options(studentobj,examobj)

                else:
                    no_attempted_m=Student_Exam_Flag.objects.filter(studentid=studentobj,examid=examobj,level="M").values_list('count_attempted_questions')
                    if len(no_attempted_m) == 1:
                    # check if no of attempted medium question is less than the total_medium_question(3)
                        if no_attempted_m[0][0] < total_medium_question:
                            questionobj,new_list=get_next_mediumqn_and_options(studentobj,examobj)
                        elif no_attempted_m[0][0] == total_medium_question:
                            
                            answerlist= Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,correct_answer=False)
                            if len(answerlist) == 0:
                                questionlist=Question_Exam_Bridge.objects.filter(exam__exam_name=exam,question__question_difficulty_level="Difficult")
                                questionobj=questionlist[0].question
                                optionlist=Question_Option.objects.filter(question__question=questionobj)
                                for option in optionlist:
                                    new_list.append(option)
                            else:
                                
                                questionobj,new_list=get_next_mediumqn_and_options(studentobj,examobj)

                        elif no_attempted_m[0][0] > total_medium_question:
                            #print("I'M HERE IN MEDIUM greater")

                            latest_false_answerobj= Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,correct_answer=False).last()
                            latest_false_answer_slno=latest_false_answerobj.sl_no
                            print(latest_false_answer_slno)
                            last_answer_slnoobj=Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,questionid__question_difficulty_level="Medium").last()
                            last_answer_slno=last_answer_slnoobj.sl_no
                            print(last_answer_slno)
                            if last_answer_slno - latest_false_answer_slno > total_medium_question:
                            # give him his first Difficult question
                                questionlist=Question_Exam_Bridge.objects.filter(exam__exam_name=exam,question__question_difficulty_level="Difficult")
                                questionobj=questionlist[0].question
                                optionlist=Question_Option.objects.filter(question__question=questionobj)
                                for option in optionlist:
                                    new_list.append(option) 
                            else:
                                questionobj,new_list=get_next_mediumqn_and_options(studentobj,examobj)
                    else:
                        if Answer_Sheet.objects.get(questionid=questionobj).correct_answer == True:
                            # to check the student ever gone to D level after succefully completed level M
                            if len(Student_Exam_Flag.objects.filter(studentid=studentobj,examid=examobj,level="D"))==0:
                                
                                no_attempted_m=Student_Exam_Flag.objects.filter(studentid=studentobj,examid=examobj,level="M").values_list('count_attempted_questions')
                                if no_attempted_m[0][0] < total_medium_question:
                                    questionobj,new_list=get_next_mediumqn_and_options(studentobj,examobj)
                                
                                else:
                                    questionobj,new_list=get_next_mediumqn_and_options(studentobj,examobj)
                            else:
                                questionobjectlist = Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,questionid__question_difficulty_level="Difficult").values_list('questionid__question')
                                questionlist_qn_exam=Question_Exam_Bridge.objects.filter(exam=examobj,question__question_difficulty_level="Difficult").values_list('question__question')
                                next_questionlist=questionlist_qn_exam.difference(questionobjectlist)
                                question = next_questionlist[0][0]
                                questionobj=Question_Master.objects.get(question=question)
                                optionlist=Question_Option.objects.filter(question__question=questionobj)
                                for option in optionlist:
                                    new_list.append(option)
                        else:
                            questionobj,new_list=get_next_easyqn_and_options(studentobj,examobj)
#in difficult level , only want to check the answer if itis right give the next diiicult qn and not give the mdeium qn 
            elif questionobj.question_difficulty_level == "Difficult":
                if Answer_Sheet.objects.get(questionid=questionobj).correct_answer == False:
                    questionobj,new_list=get_next_mediumqn_and_options(studentobj,examobj)
                else:
                    questionobj,new_list=get_next_difficultqn_and_options(studentobj,examobj)
    
        else:
            # display the result
            template_name="onlineexamapp/exam_mark.html"
            question ='Exam Ended'
            total_correctanswer = Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,correct_answer=True).aggregate(to_add=Sum('marks'))
            total_wronganswer = Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,correct_answer=False).aggregate(to_deduct=Sum('marks'))
            if total_correctanswer['to_add'] == None:
                total_mark = 0 - total_wronganswer['to_deduct']
            elif total_wronganswer['to_deduct'] == None:
                total_mark = total_correctanswer['to_add'] - 0
            else:
                total_mark = total_correctanswer['to_add'] - total_wronganswer['to_deduct']
            
            new_list=[]
            mark = total_mark
            each_emark=Question_Exam_Bridge.objects.filter(exam=examobj,question__question_difficulty_level="Easy").values_list('marks_to_add')
            total_emark=each_emark[0][0]*total_easy_question
            each_mmark=Question_Exam_Bridge.objects.filter(exam=examobj,question__question_difficulty_level="Medium").values_list('marks_to_add')
            total_mmark=each_mmark[0][0]*total_medium_question
            each_dmark=Question_Exam_Bridge.objects.filter(exam=examobj,question__question_difficulty_level="Difficult").values_list('marks_to_add')
            total_dmark=each_dmark[0][0]*(total_questions - (total_easy_question + total_medium_question))
            out_of_mark=total_emark+total_mmark+total_dmark

            result_details=detailed_result(studentobj,examobj)
            print(result_details)
            
            context={"mark":total_mark,"total":out_of_mark,"Result_Details":result_details}  
            return render(request,template_name,context)

        
        context={"Question":questionobj.question,"Options":new_list}
        return render(request,template_name,context)

def detailed_result(studentobj,examobj):
    result_details= Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj).values_list('studentid__studen_name','examid__exam_name','questionid__question','student_answerid__option','correct_answerid__answer__option','correct_answer','marks')
    return result_details

def questionform(request):
    template_name="onlineexamapp/question.html"
    questionform=question_master_modelform()
    if request.method=="GET":
        context={"Question":questionform}
        return render(request,template_name,context)
    elif request.method=="POST":
        questionform=question_master_modelform(request.POST)
        if questionform.is_valid():
            questionform.save()
        questionform=question_master_modelform()
        context={"Question":questionform}
        return render(request,template_name,context)

def question_examform(request):
    template_name="onlineexamapp/question_exam_bridge.html"
    question_examform=questionexam_bridge_modelform()
    if request.method=="GET":
        context={"QuestionExam":question_examform}
        return render(request,template_name,context)
    elif request.method=="POST":
        question_examform=questionexam_bridge_modelform(request.POST)
        if question_examform.is_valid():
            question_examform.save()
        question_examform=questionexam_bridge_modelform()
        context={"QuestionExam":question_examform}
        return render(request,template_name,context)

def question_optionform(request):
    template_name="onlineexamapp/question_option.html"
    question_optionform=questionoption_modelform()
    if request.method=="GET":
        context={"QuestionOption":question_optionform}
        return render(request, template_name,context)
    elif request.method=="POST":
        question_optionform=questionoption_modelform(request.POST)
        if question_optionform.is_valid():
            question_optionform.save()
        question_optionform=questionoption_modelform()
        context={"QuestionOption":question_optionform}
        return render(request, template_name,context)

def question_answerform(request):
    #print("hi")
    template_name="onlineexamapp/question_answer_bridge.html"
    question_answerform=questionanswer_bridgemodelform()
    #print(question_answerform)
    if request.method=="GET":
        context={"QuestionAnswer":question_answerform}
        return render(request,template_name,context)
    elif request.method=="POST":
        question_answerform=questionanswer_bridgemodelform(request.POST)
        if question_answerform.is_valid():
            question_answerform.save()
        question_answerform=questionanswer_bridgemodelform()
        context={"QuestionAnswer":question_answerform}
        return render(request,template_name,context)

'''def answer_sheetform(request):
    template_name="onlineexamapp/answer_sheetform.html"
    answer_sheetform=answersheet_modelform()
    if request.method=="GET":
        context={"AnswerSheet":answer_sheetform}
        return render(request,template_name,context)
    elif request.method=="POST":
        answer_sheetform=answersheet_modelform(request.POST)
        if answer_sheetform.is_valid():
            answer_sheetform.save()
        answer_sheetform=answersheet_modelform()
        context={"AnswerSheet":answer_sheetform}
        return render(request,template_name,context)'''

def student_exam_flagform(request):
    template_name="onlineexamapp/student_exam_flagform.html"
    student_exam_flagform=student_exam_flagmodelform()
    if request.method=="GET":
        context={"LevelFlag":student_exam_flagform}
        return render(request,template_name,context)
    elif request.method=="POST":
        student_exam_flagform=student_exam_flagmodelform(request.POST)
        if student_exam_flagform.is_valid():
            student_exam_flagform.save()
    student_exam_flagform=student_exam_flagmodelform()
    context={"LevelFlag":student_exam_flagform}
    return render(request,template_name,context)



'''def examlist(request):
    template_name="onlineexamapp/examlist.html"
    examlist=Exam.objects.all()
    if request.method=="GET":
        context={"ExamList":examlist}
        return render(request,template_name,context)
    return render(request,template_name,context)'''

def exam_edit(request,examid=None):
    template_name="onlineexamapp/examinfo.html"
    if request.method=="GET" and examid!=None:
        examinfomodel=Exam.objects.get(exam_id=examid)
        examinfomodelform=exam_modelform(instance=examinfomodel)
        context={"examinstance":examinfomodelform}
        return render(request,template_name,context)
    elif request.method=="POST" and examid!=None:
        examinfomodel=Exam.objects.get(exam_id=examid)
        examinfomodelform=exam_modelform(request.POST,instance=examinfomodel)
        context={"examinstance":examinfomodelform}
        if examinfomodelform.is_valid():
            examinfomodelform.save()
            return render(request,template_name,context)
    return render(request,template_name,context)

def change_to_dictionary(examinfomodelform):
    exam_dict=[item for item in examinfomodelform]
    dict_to_return={}
    '''for exam_info in exam_dict:
        examname=exam_info.exam_name
        examcode=exam_info.exam_code
        examcat=exam_info.exam_is_cat
        examduration=exam_info.exam_duration
        examquestions=exam_info.exam_no_questions
        exammark=exam_info.exam_cut_of_mark
        examlevel=exam_info.exam_level
        examtime=exam_info.exam_time
        examdate=exam_info.exam_date
        examyear=exam_info.exam_year
        examtype=exam_info.exam_type
        new_dict={"examname":examname,"examcode":examcode,"examcat":examcat,"examduration":examduration,"examquestions":examquestions,
        "exammark":exammark,"examlevel":examlevel,"examtime":examtime,"examtime":examtime,"examdate":examdate,"examyear":examyear,"examtype":examtype}
        dict_to_return[exam_info.exam_id]=new_dict'''
    dict_to_return=exam_dict
    #print(dict_to_return)
    return dict_to_return

'''def examsearchpagination(request):
    template_name="onlineexamapp/examsearchpagination.html"
    if request.method=="GET":
        examid=request.GET.get('examid')
        print(examid)
        examinfomodel=Exam.objects.filter(exam_id=examid).values()
        examselect=Exam.objects.get(exam_id=examid)
        examinfomodelform=exam_modelform(instance=examselect)
        #print(examinfomodelform)
        context={"examinstance":examinfomodelform}
        new_list=change_to_dictionary(examinfomodel)
        return JsonResponse(new_list,safe=False)
        #return render(request,template_name,context)'''


def change_to_dictionary_exam(examlist):
    exam_dict=[item for item in examlist]
    dict_to_return={}
    for exam_info in exam_dict:
        examid=exam_info.exam_id
        examname=exam_info.exam_name
        examcode=exam_info.exam_code
        examcat=exam_info.exam_is_cat
        examduration=exam_info.exam_duration
        examquestion=exam_info.exam_no_questions
        exammark=exam_info.exam_cut_of_mark
        examlevel=exam_info.exam_level
        examtime=exam_info.exam_time
        examdate=exam_info.exam_date
        examyear=exam_info.exam_year
        examtype=exam_info.exam_type
        new_dict={'examid':examid,'examname':examname,'examcode':examcode,'examcat':examcat,'examduration':examduration,'examquestion':examquestion,'exammark':exammark,'examlevel':examlevel,
        'examtime':examtime,'examdate':examdate,'examyear':examyear,'examtype':examtype}
        dict_to_return[exam_info.exam_id]=new_dict
    return dict_to_return

'''def examsearchinfo(request):
    template_name="onlineexamapp/examlist.html"
    query=Q()
    if request.method=="GET":
        page_num=request.GET.get('page',1)
        examname=request.GET.get('examname','')
        examdate=request.GET.get('examcode','')
        intpage_num=int(page_num)
        start_num=(intpage_num-1)*2
        end_num=start_num+2
        if examname!='':
            query&=Q(exam_name__contains=examname)
        if examdate!='':
            query&=Q(exam_date__contains=examdate)
        if query!='(AND:)':
            examlist=Exam.objects.filter(query).order_by('exam_name')
            total_count=examlist.count()
            examlist=examlist[start_num:end_num]
        else:
            examlist=Exam.objects.all().order_by('exam_name')
    new_examlist=change_to_dictionary_exam(examlist)
    new_examlist['total_count']={'queryset_count':total_count}
    return JsonResponse(new_examlist,safe=False)'''

def centerlist(request):
    template_name="onlineexamapp/centerlist.html"
    centerlist=Center.objects.all()
    if request.method=="GET":
        context={"CenterList":centerlist}
        return render(request,template_name,context)
    return render(request,template_name,context)
def center_edit(request,centerid=None):
    template_name="onlineexamapp/centerinfo.html"
    if request.method=="GET" and centerid!=None:
        centerinfomodel=Center.objects.get(center_id=centerid)
        centerinfomodelform=center_modelform(instance=centerinfomodel)
        context={"centerinstance":centerinfomodelform}
        return render(request,template_name,context)
    elif request.method=="POST" and centerid!=None:
        centerinfomodel=Center.objects.get(center_id=centerid)
        centerinfomodelform=center_modelform(request.POST,instance=centerinfomodel)
        if centerinfomodelform.is_valid():
            centerinfomodelform.save()
            centerinfomodelform=center_modelform()
            context={"centerinstance":centerinfomodelform}
            return render(request,template_name,context)
    centerinfomodelform=center_modelform()
    context={"centerinstance":centerinfomodelform}
    return render(request,template_name,context)
'''def subjectlist(request):
    template_name="onlineexamapp/subjectlist.html"
    subjectlist=Subject.objects.all()
    if request.method=="GET":
        context={"SubjectList":subjectlist}
        return render(request,template_name,context)
    return render(request,template_name,context)'''
def subject_edit(request,subjectid=None):
    template_name="onlineexamapp/subjectinfo.html"
    if request.method=="GET" and subjectid!=None:
        subjectmodel=Subject.objects.get(subject_id=subjectid)
        subjectmodelform=subject_modelform(instance=subjectmodel)
        context={"subjectinstance":subjectmodelform}
        return render(request,template_name,context)
    elif request.method=="POST" and subjectid!=None:
        subjectmodel=Subject.objects.get(subject_id=subjectid)
        subjectmodelform=subject_modelform(request.POST,instance=subjectmodel)
        if subjectmodelform.is_valid():
            subjectmodelform.save()
            subjectmodelform=subject_modelform()
            context={"subjectinstance":subjectmodelform}
            return render(request,template_name,context)
    subjectmodelform=subject_modelform()
    context={"subjectinstance":subjectmodelform}
    return render(request,template_name,context)
def examsubject_edit(request,es_id=None):
    template_name="onlineexamapp/examsubjectinfo.html"
    if request.method=="GET" and es_id!=None:
        examsubjectmodel=Exam_Subject_Bridge.objects.get(esbridge_id=es_id)
        examsubjectmodelform=examsubject_bridge_modelform(instance=examsubjectmodel)
        context={"examsubjectinstance":examsubjectmodelform}
        return render(request,template_name,context)
    elif request.method=="POST" and es_id!=None:
        examsubjectmodel=Exam_Subject_Bridge.objects.get(esbridge_id=es_id)
        examsubjectmodelform=examsubject_bridge_modelform(request.POST,instance=examsubjectmodel)
        if examsubjectmodelform.is_valid():
            examsubjectmodelform.save()
            examsubjectmodelform=examsubject_bridge_modelform()
            context={"examsubjectinstance":examsubjectmodelform}
            return render(request,template_name,context)
    examsubjectmodelform=examsubject_bridge_modelform()
    context={"examsubjectinstance":examsubjectmodelform}
    return render(request,template_name,context)

def examlistpagination(request):
    template_name="onlineexamapp/examlistpagination.html"
    if request.method=="GET":
        query=Q()
        page_num=request.GET.get('page',1)
        examname=request.GET.get('examname','')
        examdate=request.GET.get('examdate','')
        if examname!="":
            query &=Q(exam_name__contains=examname)
        if examdate!="":
            query &=Q(exam_date__contains=examdate)
        if query!='(AND: )':
            examlist=Exam.objects.filter(query).order_by('exam_name')
        else:
            examlist=Exam.objects.all().order_by('exam_name')
        paginator=Paginator(examlist,2)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        context={"page_obj":page_obj,"examname":examname,"examdate":examdate}
    return render(request,template_name,context)
def subjectlistpagination(request):
    template_name="onlineexamapp/subjectlistpagination.html"
    if request.method=="GET":
        query=Q()
        page_num=request.GET.get('page',1)
        subject=request.GET.get('subject','')
        category=request.GET.get('category','')
        if subject!='':
            query &=Q(subject_name__contains=subject)
        if category!='':
            query &=Q(subject_category__contains=category)
        if query!='(AND: )':
            subjectlist=Subject.objects.filter(query).order_by('subject_name')
        else:
            subjectlist=Subject.objects.all().order_by('subject_name')
        paginator=Paginator(subjectlist,2)
        page_number=request.GET.get('page',1)
        page_obj=paginator.get_page(page_number)
        context={"page_obj":page_obj,"subject":subject,"category":category}
    return render(request,template_name,context)
def examsubject_bridgelist(request):
    template_name="onlineexamapp/examsubject_bridgelist.html"
    if request.method=="GET":
        query=Q()
        page_num=request.GET.get('page',1)
        exam=request.GET.get('exam','')
        subject=request.GET.get('subject','')
        if exam!='':
            query &=Q(exam__contians=exam)
        if subject !='':
            query &=Q(subject__contains=subject)
        if query !='(AND: )':
            examsubjectlist=Exam_Subject_Bridge.objects.filter(query).order_by('exam')
        else:
            examsubjectlist=Exam_Subject_Bridge.objects.all().order_by('exam')
        paginator=Paginator(examsubjectlist,2)
        page_number=request.GET.get('page',1)
        page_obj=paginator.get_page(page_number)
        context={"page_obj":page_obj,"exam":exam,"subject":subject}
    return render(request,template_name,context)
def question_edit(request,questionid=None):
    template_name="onlineexamapp/questioninfo.html"
    if request.method=="GET" and questionid!=None:
        questionsubjectmodel=Question_Master.objects.get(question_id=questionid)
        questionsubjectmodelform=question_master_modelform(instance=questionsubjectmodel)
        context={"questionsubjectinstance":questionsubjectmodelform}
        return render(request,template_name,context)
    elif request.method=="POST" and questionid!=None:
        questionsubjectmodel=Question_Master.objects.get(question_id=questionid)
        questionsubjectmodelform=question_master_modelform(request.POST,instance=questionsubjectmodel)
        if questionsubjectmodelform.is_valid():
            questionsubjectmodelform.save()
            questionsubjectmodelform=question_master_modelform()
            context={"questionsubjectinstance":questionsubjectmodelform}
            return render(request,template_name,context)
    questionsubjectmodelform=question_master_modelform()
    context={"questionsubjectinstance":questionsubjectmodelform}
    return render(request,template_name,context)

def questionlist(request):
    template_name="onlineexamapp/questionlist.html"
    if request.method=="GET":
        query=Q()
        page_num=request.GET.get('page',1)
        question=request.GET.get('question','')
        level=request.GET.get('level','')
        q_subject=request.GET.get('q_subject','')
        if question!='':
            query &=Q(question__contains=question)
        if level!='':
            query &=Q(question_difficulty_level__contains=level)
        if q_subject!='':
            query &=Q(question_subject__contains=q_subject)
        if query!='(AND: )':
            questionlist=Question_Master.objects.filter(query).order_by('question')
        else:
            questionlist=Question_Master.objects.all().order_by('question')
        paginator=Paginator(questionlist,3)
        page_number=request.GET.get('page',1)
        page_obj=paginator.get_page(page_number)
        #print(page_obj)
        context={"page_obj":page_obj,"Question":question,"Level":level,"Q_Subject":q_subject}
    return render(request,template_name,context)

def questionexam_bridgeedit(request,qebridgeid=None):
    template_name="onlineexamapp/questionexaminfo.html"
    if request.method=="GET" and qebridgeid!=None:
        questionexammodel=Question_Exam_Bridge.objects.get(qebridge_id=qebridgeid)
        questionexammodelform=questionexam_bridge_modelform(instance=questionexammodel)
        context={"questionexaminstance":questionexammodelform}
        return render(request,template_name,context)
    elif request.method=="POST" and qebridgeid!=None:
        questionexammodel=Question_Exam_Bridge.objects.get(qebridge_id=qebridgeid)
        questionexammodelform=questionexam_bridge_modelform(request.POST,instance=questionexammodel)
        if questionexammodelform.is_valid():
            questionexammodelform.save()
            questionexammodelform=questionexam_bridge_modelform()
            context={"questionexaminstance":questionexammodelform}
            return render(request,template_name,context)
    questionexammodelform=questionexam_bridge_modelform()
    context={"questionexaminstance":questionexammodelform}
    return render(request,template_name,context)

def questionexam_bridgelist(request):
    template_name="onlineexamapp/questionexam_bridgelist.html"
    if request.method=="GET":
        query=Q()
        page_num=request.GET.get('page',1)
        exam=request.GET.get('exam','')
        question=request.GET.get('question','')
        if exam !='':
            query &=Q(exam__exam_name__contains=exam)
        if question !='':
            query &=Q(question__question__contains=question)
        if query !='(AND: )':
            questionexamlist=Question_Exam_Bridge.objects.filter(query).order_by('exam')
        else:
            questionexamlist=Question_Exam_Bridge.objects.all().order_by('exam')
        paginator=Paginator(questionexamlist,2)
        page_number=request.GET.get('page',1)
        page_obj=paginator.get_page(page_number)
        context={"page_obj":page_obj,"exam":exam,"question":question}
    return render(request,template_name,context)

def questionoption_edit(request,questionid=None):
    template_name="onlineexamapp/questionoptioninfo.html"
    if request.method=="GET" and questionid !=None:
        questionoptionmodel=Question_Option.objects.get(question=questionid)
        questionoptionmodelform=questionoption_modelform(instance=questionoptionmodel)
        context={"questionoptioninstance":questionoptionmodelform}
        return render(request,template_name,context)
    elif request.method=="POST" and questionid !=None:
        questionoptionmodel=Question_Option.objects.get(question=questionid)
        questionoptionmodelform=questionoption_modelform(request.POST,instance=questionoptionmodel)
        if questionoptionmodelform.is_valid():
            questionoptionmodelform.save()
            questionoptionmodelform=questionoption_modelform()
            context={"questionoptioninstance":questionoptionmodelform}
            return render(request,template_name,context)
    questionoptionmodelform=questionoption_modelform()
    context={"questionoptioninstance":questionoptionmodelform}
    return render(request,template_name,context)      

def question_optionlist(request):
    template_name="onlineexamapp/question_optionlist1.html"
    if request.method=="GET":
        
        query=Q()
        page_num=request.GET.get('page',1)
        question=request.GET.get('question','')
        no_option=request.GET.get('option','')
        if question !='':
            query &=Q(question__question__contains=question)
        if no_option !='':
            query &=Q(max_no_option__contains=no_option)
        if query !='(AND: )':
            question_optionlist=Question_Option.objects.filter(query).order_by('question')
        else:
            question_optionlist=Question_Option.objects.all().order_by('question')
        print(question_optionlist)
        paginator=Paginator(question_optionlist,6)
        page_number=request.GET.get('page',1)
        page_obj=paginator.get_page(page_number)
        #context={"page_obj":page_obj,"question":question,"option":no_option}
        context={"page_obj":page_obj,"question":question_optionlist,"optionlist":no_option}
        return render(request,template_name,context)

def questionanswer_edit(request,qabridgeid=None):
    template_name="onlineexamapp/questionanswerinfo.html"
    if request.method== "GET" and qabridgeid !=None:
        questionanswermodel=Questions_Answer_bridge.objects.get(qabridge_id=qabridgeid)
        questionanswermodelform=questionanswer_bridgemodelform(instance=questionanswermodel)
        context={"questionanswerinstance":questionanswermodelform}
        return render(request,template_name,context)
    elif request.method=="POST" and qabridgeid !=None:
        questionanswermodel=Questions_Answer_bridge.objects.get(qabridge_id=qabridgeid)
        questionanswermodelform=questionanswer_bridgemodelform(request.POST,instance=questionanswermodel)
        if questionanswermodelform.is_valid():
            questionanswermodelform.save()
            questionanswermodelform=questionanswer_bridgemodelform()
            context={"questionanswerinstance":questionanswermodelform}
            return render(request,template_name,context)
    questionanswermodelform=questionanswer_bridgemodelform()
    context={"questionanswerinstance":questionanswermodelform}
    return render(request,template_name,context)

def qexam_answerbridge_list(request):
    template_name="onlineexamapp/exam_answerbridge_list.html"
    if request.method=="GET":
        query=Q()
        page_num=request.GET.get('page',1)
        exam=request.GET.get('exam','')
        print(exam)
        answer=request.GET.get('answer','')
        if exam != '':
            query &=Q(qebridge_id__exam__exam_name__contains=exam)
        if answer != '':
            query &=Q(option__option__contains=answer)
        if query != '(AND: )':
            exam_answer_bridgelist=Questions_Answer_bridge.objects.filter(query)
        else:
            exam_answer_bridgelist=Questions_Answer_bridge.objects.all()
        #print(exam_answer_bridgelist)
        paginator=Paginator(exam_answer_bridgelist,2)
        page_number=request.GET.get('page',1)
        page_obj=paginator.get_page(page_number)
        context={"page_obj":page_obj,"exam":exam,"answer":answer}
        return render(request,template_name,context)



'''studentobj=Student.objects.get(studen_name='Nevaeh')
    examobj=Exam.objects.get(exam_name='Reserve Bank of India Exam')
    #print(examobj)
    qeinstances=Question_Exam_Bridge.objects.filter(exam=examobj)
    #print(qeinstances)
    for instance in qeinstances:
        print(instance)
    Question=qeinstances[0].question
    optionlist=Question_Option.objects.filter(question=Question)
    Listofoptions=optionlist
    #print(Listofoptions)
        #exam_paperform=exam_paper_modelform(instance=instance)
        #print(exam_paperform)
    
    #print(exam_paperform)'''










        











    

# Create your views here.

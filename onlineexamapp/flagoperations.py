from onlineexamapp.models import Student_Exam_Flag,Question_Master,Answer_Sheet,Question_Exam_Bridge,Question_Option


def get_next_easyqn_and_options(studentobj,examobj):
    new_list=[]
    questionobjectlist = Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,questionid__question_difficulty_level="Easy").values_list('questionid')
    questionlist_qn_exam=Question_Exam_Bridge.objects.filter(exam=examobj,question__question_difficulty_level="Easy").values_list('question')
    next_questionlist=questionlist_qn_exam.difference(questionobjectlist)
    #print(next_questionlist)
    question = next_questionlist[0][0]
    #print("question",question)
    questionobj=Question_Master.objects.get(question_id=question)
    optionlist=Question_Option.objects.filter(question__question=questionobj)
    for option in optionlist:
        new_list.append(option)
    return questionobj,new_list

def get_next_mediumqn_and_options(studentobj,examobj):
    new_list=[]
    questionobjectlist = Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,questionid__question_difficulty_level="Medium").values_list('questionid')
    questionlist_qn_exam = Question_Exam_Bridge.objects.filter(exam=examobj,question__question_difficulty_level="Medium").values_list('question')
    next_questionlist=questionlist_qn_exam.difference(questionobjectlist)
    #print(next_questionlist)
    question = next_questionlist[0][0]
    #print("question",question)
    questionobj=Question_Master.objects.get(question_id=question)
    optionlist=Question_Option.objects.filter(question__question=questionobj)
    for option in optionlist:
        new_list.append(option)
    return questionobj,new_list

def get_next_difficultqn_and_options(studentobj,examobj):
    new_list=[]
    questionobjectlist = Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,questionid__question_difficulty_level="Difficult").values_list('questionid')
    questionlist_qn_exam = Question_Exam_Bridge.objects.filter(exam=examobj,question__question_difficulty_level="Difficult").values_list('question')
    next_questionlist=questionlist_qn_exam.difference(questionobjectlist)
    #print('next_questionlist', next_questionlist)
    question = next_questionlist[0][0]
    #print("question",question)
    questionobj=Question_Master.objects.get(question_id=question)
    optionlist=Question_Option.objects.filter(question__question=questionobj)
    for option in optionlist:
        new_list.append(option)
    return questionobj,new_list

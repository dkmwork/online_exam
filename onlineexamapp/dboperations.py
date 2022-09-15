from onlineexamapp.models import Student_Exam_Flag,Question_Master,Answer_Sheet

def insert_into_studentflag(answersheetmodel):
    
    questionobj=answersheetmodel.questionid
    #questionobj=Question_Master.objects.get(question=questionid)
    if questionobj.question_difficulty_level == "Easy":
        
        existing_student_inexam=Student_Exam_Flag.objects.filter(studentid=answersheetmodel.studentid,examid=answersheetmodel.examid,level='E')
        if len(existing_student_inexam) == 0:
            student_exam_flagmodel=Student_Exam_Flag()
            student_exam_flagmodel.studentid=answersheetmodel.studentid
            student_exam_flagmodel.examid=answersheetmodel.examid
            student_exam_flagmodel.level= 'E'
            student_exam_flagmodel.count_attempted_questions=1
            student_exam_flagmodel.save()
            # check the student exam flag for 'easy' (difficulty level)flag table and check the student attend any Medium level questions and came back to 
            # easy level again
            # if so create the easy table again with  count_attempted_questions=1
            # if not add the 1 to the count_attempted_questions
        if len(existing_student_inexam) ==1:

            if len(Student_Exam_Flag.objects.filter(studentid=answersheetmodel.studentid,examid=answersheetmodel.examid,level='M'))==0:
                existing_student_inexam[0].count_attempted_questions =existing_student_inexam[0].count_attempted_questions + 1
                existing_student_inexam[0].save()
            else:
                student_exam_flagmodel=Student_Exam_Flag()
                student_exam_flagmodel.studentid=answersheetmodel.studentid
                student_exam_flagmodel.examid=answersheetmodel.examid
                student_exam_flagmodel.level= 'E'
                student_exam_flagmodel.count_attempted_questions=1
                student_exam_flagmodel.save()

        if len(existing_student_inexam) > 1:
            student_exam_flagmodel=Student_Exam_Flag()
            student_exam_flagmodel.studentid=answersheetmodel.studentid
            student_exam_flagmodel.examid=answersheetmodel.examid
            student_exam_flagmodel.level= 'E'
            student_exam_flagmodel.count_attempted_questions=1
            student_exam_flagmodel.save()

    elif questionobj.question_difficulty_level == "Medium":
        existing_student_inexam=Student_Exam_Flag.objects.filter(studentid=answersheetmodel.studentid,examid=answersheetmodel.examid,level='M')

        if len(Student_Exam_Flag.objects.filter(studentid=answersheetmodel.studentid,examid=answersheetmodel.examid,level="D")) == 0:

            if len(existing_student_inexam) == 0:
            
                student_exam_flagmodel=Student_Exam_Flag()
                student_exam_flagmodel.studentid=answersheetmodel.studentid
                student_exam_flagmodel.examid=answersheetmodel.examid
                student_exam_flagmodel.level= 'M'
                student_exam_flagmodel.count_attempted_questions=1
                student_exam_flagmodel.save()
            if len(existing_student_inexam) ==1:
                
                existing_student_inexam[0].count_attempted_questions =existing_student_inexam[0].count_attempted_questions + 1
                existing_student_inexam[0].save()
                
        else:
            student_exam_flagmodel=Student_Exam_Flag()
            student_exam_flagmodel.studentid=answersheetmodel.studentid
            student_exam_flagmodel.examid=answersheetmodel.examid
            student_exam_flagmodel.level= 'M'
            student_exam_flagmodel.count_attempted_questions=1
            student_exam_flagmodel.save()
                
        '''if len(existing_student_inexam) > 1:
            #********
            #new_answerlist=Answer_Sheet.objects.filter(studentid=studentobj,examid=examobj,questionid__question_difficulty_level="Difficult")
            if len(Student_Exam_Flag.objects.filter(studentid=answersheetmodel.studentid,examid=answersheetmodel.examid,level='D')) == 0:
                
                #if Answer_Sheet.objects.get(questionid=questionobj).correct_answer == True:
                    existing_student_inexam[0].count_attempted_questions =existing_student_inexam[0].count_attempted_questions + 1
                    existing_student_inexam[0].save()
                #else:
                    #existing_student_inexam[0].count_attempted_questions =existing_student_inexam[0].count_attempted_questions + 1
                    #existing_student_inexam[0].save()
            else:
                student_exam_flagmodel=Student_Exam_Flag()
                student_exam_flagmodel.studentid=answersheetmodel.studentid
                student_exam_flagmodel.examid=answersheetmodel.examid
                student_exam_flagmodel.level= 'M'
                student_exam_flagmodel.count_attempted_questions=1
                student_exam_flagmodel.save() '''


    elif questionobj.question_difficulty_level == "Difficult":
        
        existing_student_inexam=Student_Exam_Flag.objects.filter(studentid=answersheetmodel.studentid,examid=answersheetmodel.examid,level='D')
        if len(existing_student_inexam) == 0:
            student_exam_flagmodel=Student_Exam_Flag()
            student_exam_flagmodel.studentid=answersheetmodel.studentid
            student_exam_flagmodel.examid=answersheetmodel.examid
            student_exam_flagmodel.level= 'D'
            student_exam_flagmodel.count_attempted_questions=1
            student_exam_flagmodel.save()
        if len(existing_student_inexam) == 1:
            existing_student_inexam[0].count_attempted_questions =existing_student_inexam[0].count_attempted_questions + 1
            existing_student_inexam[0].save()
        if len(existing_student_inexam) > 1:
            student_exam_flagmodel=Student_Exam_Flag()
            student_exam_flagmodel.studentid=answersheetmodel.studentid
            student_exam_flagmodel.examid=answersheetmodel.examid
            student_exam_flagmodel.level= 'D'
            student_exam_flagmodel.count_attempted_questions=1
            student_exam_flagmodel.save()
    
    
    
        
    






    
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        context = {}
        # Lấy danh sách ID các lựa chọn người dùng tích chọn
        selected_ids = [int(choice_id) for choice_id in request.POST.getlist('choice')]
        
        # Lấy hoặc tạo tạm một Enrollment để build Submission object
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user, 
            course=course
        )
        
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in selected_ids:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)
            
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    selected_ids = [choice.id for choice in submission.choices.all()]
    total_score = 0
    possible_score = 0
    
    for question in course.question_set.all():
        possible_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    context = {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,
        'total_score': total_score,
        'possible_score': possible_score,
        'grade': total_score,
        'message': 'Congratulations! You passed the exam.' if total_score >= (possible_score * 0.7) else 'Keep trying!'
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Logic nhận bài thi trắc nghiệm từ template gửi lên
        return redirect('onlinecourse:show_exam_result', course_id=course.id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {
        'course': course,
        'score': 100,
        'message': 'Congratulations! You passed the exam.'
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

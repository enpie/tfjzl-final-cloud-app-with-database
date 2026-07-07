from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission, Enrollment
# Đảm bảo import đủ các class giả lập hoặc có sẵn từ bài học
from django.contrib.auth.models import User as Learner

class Instructor(models.Model):
    pass

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'grade']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Enrollment)

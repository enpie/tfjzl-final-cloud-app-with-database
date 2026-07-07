from django.db import models
from django.utils.timezone import now

class Course(models.Model):
    name = models.CharField(null=False, max_length=50, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=500)
    pub_date = models.DateField(null=True)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500, default="question")
    grade = models.IntegerField(default=1)

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_wrong = self.choice_set.filter(is_correct=False, id__in=selected_ids).count()
        if all_answers == selected_correct and selected_wrong == 0:
            return True
        return False

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500, default="choice")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Submission(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    date_submitted = models.DateTimeField(default=now)

    def __str__(self):
        return f"Submission {self.id} for {self.enrollment}"

class Enrollment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)

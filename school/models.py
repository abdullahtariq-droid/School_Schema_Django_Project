from django.db import models
from django.utils import timezone


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=50, default='superadmin')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AdminActionLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)
    table_name = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)
    record_id = models.IntegerField()

    def __str__(self):
        return f"{self.admin} - {self.action_type} on {self.table_name}"


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        Admin, on_delete=models.SET_NULL, null=True, related_name='subjects')

    def __str__(self):
        return self.subject_name


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='teachers')

    class Meta:
        unique_together = ('teacher', 'subject')

    def __str__(self):
        return f"{self.teacher.first_name} {self.teacher.last_name} teaches {self.subject.subject_name}"


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=50)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="classes")

    def __str__(self):
        return self.class_name


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrollments")
    class_assigned = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="enrollments")
    date_enrolled = models.DateField()

    def __str__(self):
        return f"{self.student} -> {self.class_assigned}"


class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    class_assigned = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='exams')
    created_by = models.ForeignKey(
        Admin, on_delete=models.SET_NULL, null=True, related_name='exams')

    def __str__(self):
        return self.name


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default='New Quiz')
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    created_by = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name='quizzes')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()

    def __str__(self):
        return self.question_text


class QuizOption(models.Model):
    question = models.ForeignKey(
        QuizQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class QuizSubmission(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='quiz_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.quiz.title}"


class QuizAnswer(models.Model):
    submission = models.ForeignKey(
        QuizSubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(
        QuizOption, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Answer to {self.question.question_text}"


# -----------------------------
# Proxy Models
# -----------------------------

class MaleStudent(Student):
    class Meta:
        proxy = True
        ordering = ['first_name']

    def is_male(self):
        return self.gender.lower() == 'male'


class SeniorTeacher(Teacher):
    class Meta:
        proxy = True
        ordering = ['-first_name']

    def senior_title(self):
        return f"Sr. {self.first_name} {self.last_name}"


class LatestQuiz(Quiz):
    class Meta:
        proxy = True
        ordering = ['-date_created']

    def recent(self):
        return self.date_created

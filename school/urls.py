from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminViewSet,
    AdminActionLogViewSet,
    StudentViewSet,
    TeacherViewSet,
    TeacherSubjectViewSet,
    ClassViewSet,
    EnrollmentViewSet,
    ExamViewSet,
    QuizViewSet,
    QuizQuestionViewSet,
    QuizOptionViewSet,
    QuizSubmissionViewSet,
    QuizAnswerViewSet,
    MaleStudentViewSet,
    SeniorTeacherViewSet,
    LatestQuizViewSet
)
router = DefaultRouter()
router.register(r'admins', AdminViewSet)
router.register(r'admin-action-logs', AdminActionLogViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'teacher-subjects', TeacherSubjectViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'quiz-questions', QuizQuestionViewSet)
router.register(r'quiz-options', QuizOptionViewSet)
router.register(r'quiz-submissions', QuizSubmissionViewSet)
router.register(r'quiz-answers', QuizAnswerViewSet)
router.register(r'male-student', MaleStudentViewSet, basename='male-student')
router.register(r'senior-teachers', SeniorTeacherViewSet,
                basename='senior-teachers')
router.register(r'latest-quiz', LatestQuizViewSet, basename='latest-quiz')

urlpatterns = [
    path('', include(router.urls)),
]


from django.urls import reverse
from django.shortcuts import redirect
from rest_framework import viewsets
from .models import Admin, AdminActionLog, Student, Teacher, Subject, TeacherSubject, Class, Enrollment, Exam, Quiz, QuizQuestion, QuizOption, QuizSubmission, QuizAnswer, SeniorTeacher, MaleStudent, LatestQuiz
from .serializers import (
    AdminSerializer,
    AdminActionLogSerializer,
    StudentSerializer, StudentCreateUpdateSerializer,
    TeacherSerializer, TeacherCreateUpdateSerializer,
    TeacherSubjectSerializer, TeacherSubjectCreateUpdateSerializer,
    ClassSerializer, ClassCreateUpdateSerializer,
    EnrollmentSerializer, EnrollmentCreateUpdateSerializer,
    ExamSerializer, ExamCreateUpdateSerializer,
    QuizSerializer, QuizCreateUpdateSerializer,
    QuizQuestionSerializer,
    QuizOptionSerializer,
    QuizSubmissionSerializer,
    QuizAnswerSerializer,
    MaleStudentSerializer,
    SeniorTeacherSerializer,
    LatestQuizSerializer,
)
# from .serializers import LatestQuizSerializer
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer


class TemplateViewSetMixin:
    """
    Adds Jinja2/HTML rendering to any ViewSet automatically.
    Requires you to set `template_name` in the subclass.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        context_name = self.queryset.model.__name__.lower() + 's'  # e.g. 'students'
        print(serializer.data)  # Debug print
        return Response({context_name: serializer.data}, template_name=self.template_name)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data}, template_name=self.template_name)


class BaseViewSet(viewsets.ModelViewSet):
    """
    A base class that allows specifying different serializers for read/write operations.
    """

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return self.create_update_serializer or self.serializer_class
        return self.serializer_class


class AdminViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    # same as default, no write restrictions
    create_update_serializer = AdminSerializer
    template_name = 'admin.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        admins = Admin.objects.all()
        return Response({'admins': admins}, template_name=self.template_name)


class AdminActionLogViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = AdminActionLog.objects.all()
    serializer_class = AdminActionLogSerializer
    create_update_serializer = AdminActionLogSerializer
    template_name = 'adminlogs.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]


class StudentViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    create_update_serializer = StudentCreateUpdateSerializer
    template_name = 'student_list.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        logs = AdminActionLog.objects.all()
        admins = Admin.objects.all()
        return Response({'logs': logs, 'admins': admins}, template_name=self.template_name)


class TeacherViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    create_update_serializer = TeacherCreateUpdateSerializer
    template_name = 'teacher_list.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]


class TeacherSubjectViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer
    create_update_serializer = TeacherSubjectCreateUpdateSerializer
    template_name = 'teacher_subject_list.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]


class ClassViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    create_update_serializer = ClassCreateUpdateSerializer
    template_name = 'class.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        classes = self.get_queryset()
        serializer = self.get_serializer(classes, many=True)
        return Response({'classes': serializer.data})


class EnrollmentViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    create_update_serializer = EnrollmentCreateUpdateSerializer
    template_name = 'enrollment.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        enrollments = self.get_queryset()
        students = Student.objects.all()
        classes = Class.objects.all()
        serializer = self.get_serializer(enrollments, many=True)
        return Response({
            'enrollments': serializer.data,
            'students': students,
            'classes': classes
        })


class ExamViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    create_update_serializer = ExamCreateUpdateSerializer
    template_name = 'exam.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        exams = Exam.objects.all()
        classes = Class.objects.all()
        admins = Admin.objects.all()
        return Response({
            'exams': exams,
            'classes': classes,
            'admins': admins
        }, template_name=self.template_name)


class QuizViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    create_update_serializer = QuizCreateUpdateSerializer
    template_name = 'quiz.html'
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        quizzes = Quiz.objects.select_related('subject', 'created_by').all()
        subjects = Subject.objects.all()
        teachers = Teacher.objects.all()
        serializer = self.get_serializer(quizzes, many=True)
        return Response({
            'quizzes': quizzes,
            'subjects': subjects,
            'teachers': teachers
        }, template_name=self.template_name)

    def create(self, request, *args, **kwargs):
        print(f"Creating a new quiz...{request.POST}")
        serializer = QuizCreateUpdateSerializer(data=request.POST)

        if serializer.is_valid():
            print("Validated data:", serializer.validated_data)  # ✅ Use this
            serializer.save()
            # Redirect to the quiz list page after successful creation
            return redirect(reverse('quiz-list'))  # Use your URL name
        else:
            print("Errors:", serializer.errors)
            quizzes = Quiz.objects.all()
            subjects = Subject.objects.all()
            teachers = Teacher.objects.all()
            quizzes_serializer = self.get_serializer(quizzes, many=True)
            print(quizzes_serializer.data)
            return Response({
                'quizzes': quizzes_serializer.data,
                'subjects': subjects,
                'teachers': teachers,
                'errors': serializer.errors
            }, template_name=self.template_name)


class QuizQuestionViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer
    create_update_serializer = QuizQuestionSerializer
    template_name = 'quizquestion.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        questions = QuizQuestion.objects.select_related('quiz').all()
        quizzes = Quiz.objects.all()
        return Response({
            'questions': questions,
            'quizzes': quizzes
        }, template_name=self.template_name)

    def create(self, request, *args, **kwargs):
        serializer = self.create_update_serializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect(request.path)  # adjust URL name
        else:
            questions = QuizQuestion.objects.select_related('quiz').all()
            quizzes = Quiz.objects.all()
            return Response({
                'questions': questions,
                'quizzes': quizzes,
                'errors': serializer.errors
            }, template_name=self.template_name)


class QuizOptionViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = QuizOption.objects.all()
    serializer_class = QuizOptionSerializer
    create_update_serializer = QuizOptionSerializer
    template_name = 'quizoption.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        options = QuizOption.objects.all()
        questions = QuizQuestion.objects.all()
        return Response({
            'options': options,
            'questions': questions
        }, template_name=self.template_name)


class QuizSubmissionViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    create_update_serializer = QuizSubmissionSerializer

    template_name = 'quizsubmission.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        submissions = QuizSubmission.objects.all()
        quizzes = Quiz.objects.all()
        students = Student.objects.all()
        return Response({
            'submissions': submissions,
            'quizzes': quizzes,
            'students': students
        }, template_name=self.template_name)


class QuizAnswerViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = QuizAnswer.objects.all()
    serializer_class = QuizAnswerSerializer
    create_update_serializer = QuizAnswerSerializer
    template_name = 'quizanswer.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        answers = QuizAnswer.objects.all()
        submissions = QuizSubmission.objects.all()
        questions = QuizQuestion.objects.all()
        options = QuizOption.objects.all()
        return Response({
            'answers': answers,
            'submissions': submissions,
            'questions': questions,
            'options': options
        }, template_name=self.template_name)


class MaleStudentViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = MaleStudent.objects.all()
    serializer_class = MaleStudentSerializer
    create_update_serializer = MaleStudentSerializer
    template_name = 'malestudent.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]


class SeniorTeacherViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = SeniorTeacher.objects.all()
    serializer_class = SeniorTeacherSerializer
    create_update_serializer = SeniorTeacherSerializer
    template_name = 'seniorteacher.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]


class LatestQuizViewSet(TemplateViewSetMixin, BaseViewSet):
    queryset = Quiz.objects.order_by('-date_created')[:1]
    serializer_class = LatestQuizSerializer
    create_update_serializer = LatestQuizSerializer
    template_name = 'latestquizview.html'
    # <--- Force template rendering only
    renderer_classes = [TemplateHTMLRenderer]

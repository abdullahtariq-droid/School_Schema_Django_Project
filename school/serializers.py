from rest_framework import serializers
from .models import (
    Admin, AdminActionLog, Student, Teacher, Subject, TeacherSubject,
    Class, Enrollment, Exam, Quiz, QuizQuestion, QuizOption, QuizSubmission, QuizAnswer,
    MaleStudent, SeniorTeacher, LatestQuiz
)


# ---- Base Serializer ----


class BaseSerializer(serializers.ModelSerializer):
    """Common behavior for all serializers."""
    created_by = serializers.StringRelatedField(
        read_only=True)  # Show admin name, not ID

    class Meta:
        abstract = True

# ---- Admin and AdminActionLog ----


class AdminSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Admin
        fields = ['admin_id', 'first_name',
                  'last_name', 'email', 'phone', 'role']


class AdminActionLogSerializer(BaseSerializer):
    admin = serializers.StringRelatedField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = AdminActionLog
        fields = ['log_id', 'admin', 'action_type',
                  'table_name', 'time_stamp', 'record_id']


# ---- Student ----
class StudentSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Student
        fields = ['student_id', 'first_name',
                  'last_name', 'gender', 'phone', 'created_by']


class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=Admin.objects.all())

    class Meta:
        model = Student
        fields = ['student_id', 'first_name',
                  'last_name', 'gender', 'phone', 'created_by']
        read_only_fields = ['student_id']


# ---- Teacher ----
class TeacherSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Teacher
        fields = ['teacher_id', 'first_name', 'last_name', 'gender', 'phone']


class TeacherCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'first_name', 'last_name', 'gender', 'phone']
        read_only_fields = ['teacher_id']


# ---- TeacherSubject ----
class TeacherSubjectSerializer(BaseSerializer):
    teacher = serializers.StringRelatedField(read_only=True)
    subject = serializers.StringRelatedField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = TeacherSubject
        fields = ['id', 'teacher', 'subject']


class TeacherSubjectCreateUpdateSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all())
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all())

    class Meta:
        model = TeacherSubject
        fields = ['id', 'teacher', 'subject']


# ---- Class ----
class ClassSerializer(BaseSerializer):
    teacher = serializers.StringRelatedField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Class
        fields = ['class_id', 'class_name', 'teacher']


class ClassCreateUpdateSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all())

    class Meta:
        model = Class
        fields = ['class_id', 'class_name', 'teacher']
        read_only_fields = ['class_id']


# ---- Enrollment ----
class EnrollmentSerializer(BaseSerializer):
    student = serializers.StringRelatedField(read_only=True)
    class_assigned = serializers.StringRelatedField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Enrollment
        fields = ['enrollment_id', 'student',
                  'class_assigned', 'date_enrolled']


class EnrollmentCreateUpdateSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all())
    class_assigned = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all())

    class Meta:
        model = Enrollment
        fields = ['enrollment_id', 'student',
                  'class_assigned', 'date_enrolled']
        read_only_fields = ['enrollment_id']


# ---- Exam ----
class ExamSerializer(BaseSerializer):
    class_assigned = serializers.StringRelatedField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Exam
        fields = ['exam_id', 'name', 'date', 'class_assigned', 'created_by']


class ExamCreateUpdateSerializer(serializers.ModelSerializer):
    class_assigned = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=Admin.objects.all())

    class Meta:
        model = Exam
        fields = ['exam_id', 'name', 'date', 'class_assigned', 'created_by']
        read_only_fields = ['exam_id']


# ---- Quiz and its related models ----
class QuizSerializer(BaseSerializer):
    subject = serializers.StringRelatedField(
        source='subject.subject_name', read_only=True)
    created_by = serializers.StringRelatedField(
        source='created_by.get_full_name', read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Quiz
        fields = ['quiz_id', 'title', 'subject', 'created_by', 'date_created']


class QuizCreateUpdateSerializer(serializers.ModelSerializer):
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all())

    class Meta:
        model = Quiz
        fields = ['quiz_id', 'title', 'subject', 'created_by', 'date_created']
        read_only_fields = ['quiz_id', 'date_created']


class QuizQuestionSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())

    class Meta():
        model = QuizQuestion
        fields = ['id', 'quiz', 'question_text']


class QuizOptionSerializer(BaseSerializer):
    question = serializers.StringRelatedField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = QuizOption
        fields = ['id', 'question', 'option_text', 'is_correct']


class QuizSubmissionSerializer(BaseSerializer):
    quiz = serializers.StringRelatedField(read_only=True)
    student = serializers.StringRelatedField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = QuizSubmission
        fields = ['id', 'quiz', 'student', 'submitted_at', 'score']


class QuizAnswerSerializer(BaseSerializer):
    submission = serializers.StringRelatedField(read_only=True)
    question = serializers.StringRelatedField(read_only=True)
    selected_option = serializers.StringRelatedField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = QuizAnswer
        fields = ['id', 'submission', 'question', 'selected_option']


class MaleStudentSerializer(StudentSerializer):
    is_male = serializers.SerializerMethodField()

    class Meta(StudentSerializer.Meta):
        model = MaleStudent
        fields = StudentSerializer.Meta.fields + ['is_male']

    def get_is_male(self, obj):
        return obj.is_male()


class SeniorTeacherSerializer(TeacherSerializer):
    senior_title = serializers.SerializerMethodField()

    class Meta(TeacherSerializer.Meta):
        model = SeniorTeacher
        fields = TeacherSerializer.Meta.fields + ['senior_title']

    def get_senior_title(self, obj):
        return obj.senior_title()


class LatestQuizSerializer(QuizSerializer):
    recent = serializers.SerializerMethodField()

    class Meta(QuizSerializer.Meta):
        model = LatestQuiz
        fields = QuizSerializer.Meta.fields + ['recent']

    def get_recent(self, obj):
        return obj.recent()

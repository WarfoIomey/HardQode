from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course, Lesson
from users.models import Subscription, CustomUser, Balance


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        queryset = Lesson.objects.filter(product_id=self.kwargs.get('course_id'))
        return queryset


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """
    def get_queryset(self):
        if self.request.user.is_authenticated:
            list_course = Subscription.objects.filter(user_id=self.request.user.id).values('courses_id')
            queryset = Course.objects.exclude(id__in=list_course)
            return queryset
        else:
            queryset = Course.objects.all()
            return queryset
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""
        # TODO
        if Subscription.objects.filter(user_id=request.user.id, courses_id=pk).exists():
            data = [{
                'message': 'Курс уже оплачен'
            }]
        else:
            balance_user = Balance.objects.filter(user_id=request.user.id).values()
            price_course = Course.objects.filter(id=pk).values()
            if balance_user[0]['score'] >= price_course[0]['price']:
                Subscription(user_id=request.user.id, courses_id=pk).save()
                new_balance = balance_user[0]['score'] - price_course[0]['price']
                Balance.objects.filter(user_id=request.user.id).update(score=new_balance)
                data = Subscription.objects.filter(user_id=request.user.id, courses_id=pk).values()
            else:
                data = [{
                    'message': 'На вашем балансе недостаточно средств'
                }]
        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )

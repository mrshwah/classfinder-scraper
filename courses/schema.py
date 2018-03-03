import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from courses.models import Course, RoomDayAndTime


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class RoomDayAndTimeType(DjangoObjectType):
    class Meta:
        model = RoomDayAndTime


class Query(graphene.ObjectType):
    courses = graphene.List(CourseType, subject=graphene.String())
    room_day_and_times = graphene.List(RoomDayAndTimeType)

    def resolve_courses(self, info, subject=None, **kwargs):
        query = Course.objects.all()

        if subject:
            filter = (
                Q(subject_id__icontains=subject)
            )
            query = query.filter(filter)

        return query

    def resolve_room_day_and_time(self, info, **kwargs):
        return RoomDayAndTime.objects.all()

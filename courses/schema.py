import graphene
from graphene_django import DjangoObjectType

from courses.models import Course, RoomDayAndTime
from courses.services import RequestedCourse, create_schedules


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class ScheduleType(graphene.ObjectType):
    courses = graphene.List(CourseType)


class RoomDayAndTimeType(DjangoObjectType):
    class Meta:
        model = RoomDayAndTime


class CourseListInput(graphene.InputObjectType):
    course_titles = graphene.List(graphene.String)


class Query(graphene.ObjectType):
    courses = graphene.List(CourseType, unique_title=graphene.Boolean())
    room_day_and_times = graphene.List(RoomDayAndTimeType)

    def resolve_courses(self, info, unique_title=False, **kwargs):
        query = Course.objects.all()

        if unique_title:
            query = query.distinct('title')

        return query

    def resolve_room_day_and_time(self, info, **kwargs):
        return RoomDayAndTime.objects.all()


class MakeSchedule(graphene.Mutation):
    schedules = graphene.List(ScheduleType)

    class Arguments:
        course_input = CourseListInput(required=True)

    def mutate(self, info, course_input):
        requested_courses = []
        for title in course_input.course_titles:
            requested_courses.append(RequestedCourse(title))
        schedules = [ScheduleType(courses=courses) for courses in create_schedules(requested_courses)]
        return MakeSchedule(schedules=schedules)


class Mutation:
    make_schedule = MakeSchedule.Field()

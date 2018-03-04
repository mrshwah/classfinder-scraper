import graphene
from graphene_django import DjangoObjectType

from courses.models import Course, RoomDayAndTime
from courses.services import RequestedCourse, create_schedule


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class RoomDayAndTimeType(DjangoObjectType):
    class Meta:
        model = RoomDayAndTime


class CourseInput(graphene.InputObjectType):
    title = graphene.String()


class CourseListInput(graphene.InputObjectType):
    courses = graphene.List(CourseInput)


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
    schedule = graphene.List(CourseType)

    class Arguments:
        course_input = CourseListInput(required=True)

    def mutate(self, info, course_input):
        requested_courses = []
        for course in course_input.courses:
            requested_courses.append(RequestedCourse(course.title))
        schedule = create_schedule(requested_courses)
        return MakeSchedule(schedule=schedule)


class Mutation:
    make_schedule = MakeSchedule.Field()

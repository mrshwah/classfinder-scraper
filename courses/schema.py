import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from courses.models import Course


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class Query(graphene.ObjectType):
    courses = graphene.List(CourseType, subject=graphene.String())

    def resolve_courses(self, info, subject=None, **kwargs):
        query = Course.objects.all()

        if subject:
            filter = (
                Q(subject_id__icontains=subject)
            )
            query = query.filter(filter)

        return query

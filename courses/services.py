from courses.models import Course


class RequestedCourse:
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return 'Title = {}, Rank = {}'.format(self.title, self.rank)


class CourseTree:
    def __init__(self, course):
        self.course = course
        self.children = []

    def add(self, courses):
        self.children.append(courses)


def create_tree(tree, possible_courses):
    if 0 == len(possible_courses):
        return tree

    for section in possible_courses[0]:
        section_tree = CourseTree(section)
        section_tree = create_tree(section_tree, possible_courses[1:])
        tree.add(section_tree)
    return tree


def build_schedules(node):
    if len(node.children) == 0:
        return [node.course]
    all_schedules = []
    for child in node.children:
        sub_schedules = build_schedules(child)
        if node.course == 'Top':
            return sub_schedules
        if not sub_schedules:
            continue
        if type(sub_schedules[0]) == Course:
            if check_conflicts(sub_schedules[0], node.course):
                sub_schedules.append(node.course)
            else:
                continue
            all_schedules.append(sub_schedules)
        else:
            for schedule in sub_schedules:
                fits = False
                for course in schedule:
                    if not check_conflicts(course, node.course):
                        break
                    fits = True
                if fits:
                    schedule.append(node.course)
                else:
                    continue
            all_schedules += sub_schedules
    return all_schedules


def check_conflicts(course_1, course_2):
    """
    Checks for course conflicts. If there are none, returns True.
    :param course_1:
    :param course_2:
    :return:
    """
    section_fits = True
    for time_1 in course_1.room_day_and_time.all():
        # check if course begins during existing course
        for time_2 in course_2.room_day_and_time.all():
            if time_1.day != time_2.day:
                break
            if time_1.begin <= time_2.begin and time_2.end <= time_1.end:
                section_fits = False
                break
            if time_1.begin <= time_2.end <= time_1.end:
                section_fits = False
                break
    return section_fits


def create_schedules(requested_courses):
    for course in requested_courses:
        print(course.title)
        print(len(Course.objects.filter(title=course.title)))
    possible_courses = [list(Course.objects.filter(title=course.title)) for course in requested_courses]

    course_tree = CourseTree('Top')
    course_tree = create_tree(course_tree, possible_courses)

    schedules = build_schedules(course_tree)
    schedules = list(filter(lambda x: len(x) == len(requested_courses), schedules))
    return schedules

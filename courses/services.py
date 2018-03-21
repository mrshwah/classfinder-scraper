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


def create_schedule(requested_courses):
    possible_courses = [list(Course.objects.filter(title=course.title)) for course in requested_courses]

    course_tree = CourseTree('Top')
    course_tree = create_tree(course_tree, possible_courses)
    course_schedule = possible_courses[0]

    return course_schedule
    '''
    for course in possibilities:  # Iterate through different courses
        for section in course:  # Iterate through individual sections of each course
            section_fits = True
            for existing in course_schedule:  # Iterate through the current schedule, what we have so far
                for time in existing.room_day_and_time.all():
                    # check if course begins during existing course
                    for section_time in section.room_day_and_time.all():
                        if time.day != section_time.day:
                            break
                        if time.begin <= section_time.begin and time.end >= section_time.end:
                            section_fits = False
                            break
                        if time.begin <= section_time.end and time.end >= section_time.end:
                            section_fits = False
                            break

            if section_fits:
                course_schedule.append(section)  # if we make it through every course in our schedule
                break  # with no conflicts, add it to schedule and move to next

    return course_schedule
    '''
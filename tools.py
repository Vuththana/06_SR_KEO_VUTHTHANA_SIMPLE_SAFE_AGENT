from schemas import SearchCourseInput, CheckScheduleInput, RegisterCourseInput

COURSES = [
    {
        "id": 1,
        "name": "Spring Boot Advanced",
        "description": "Advanced Spring Boot development"
    },
    {
        "id": 2,
        "name": "AI Engineering",
        "description": "AI Engineering and Local LLM"
    },
    {
        "id": 3,
        "name": "Korean Language",
        "description": "Korean language course"
    },
    {
        "id": 4,
        "name": "Database Systems",
        "description": "Database design and SQL"
    }
]

SCHEDULES = {
    1: {
        "day": "Monday",
        "start_time": "1:30 PM",
        "end_time": "5:00 PM"
    },
    2: {
        "day": "Tuesday",
        "start_time": "10:00 AM",
        "end_time": "12:00 PM"
    },
    3: {
        "day": "Monday - Friday",
        "start_time": "8:00 AM",
        "end_time": "10:00 AM"
    },
    4: {
        "day": "Wednesday",
        "start_time": "1:30 PM",
        "end_time": "5:00 PM"
    }
}

def search_course(input_data: SearchCourseInput):
    keyword = input_data.keyword.lower()

    results = []

    for course in COURSES:
        if (
            keyword in course["name"].lower()
            or keyword in course["description"].lower()
        ):
            results.append(course)

    return {
        "success": True,
        "courses": results
    }

USERS = {
    1: {
        "name": "Keo Vuththana",
        "role": "student"
    },
    2: {
        "name": "Goros",
        "role": "admin"
    }
}

def check_schedule(input_data: CheckScheduleInput):
    course_id = input_data.course_id

    if course_id not in SCHEDULES:
        return {
            "success": False,
            "message": "Course schedule not found"
        }

    return {
        "success": True,
        "course_id": course_id,
        "schedule": SCHEDULES[course_id]
    }

REGISTRATIONS = []

def register_course(input_data: RegisterCourseInput):
    course_id = input_data.course_id
    user_id = input_data.user_id

    # Check if user exists
    user = USERS.get(user_id)

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    # Permission check
    if user["role"] != "admin":
        return {
            "success": False,
            "message": "Permission denied: only admin can register a course"
        }

    # Check if course exists
    course = next(
        (course for course in COURSES if course["id"] == course_id),
        None
    )

    if not course:
        return {
            "success": False,
            "message": "Course not found"
        }

    # Register course
    REGISTRATIONS.append({
        "user_id": user_id,
        "course_id": course_id
    })

    return {
        "success": True,
        "message": f"Successfully registered for {course['name']}"
    }
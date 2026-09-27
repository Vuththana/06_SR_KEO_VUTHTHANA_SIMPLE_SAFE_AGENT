from pydantic import BaseModel, Field

class SearchCourseInput(BaseModel):
    keyword: str = Field(
        min_length=1,
        description="Keyword to search for a course"
    )

class CheckScheduleInput(BaseModel):
    course_id: int = Field(
        gt=0,
        description="ID of the course to check"
    )

class RegisterCourseInput(BaseModel):
    course_id: int = Field(
        gt=0,
        description="ID of the course to register"
    )

    user_id: int = Field(
        gt=0,
        description="ID of the user registering for the course"
    )
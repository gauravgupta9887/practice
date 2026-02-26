from fastapi import BackgroundTasks, FastAPI
from typing import Optional
from pydantic import BaseModel
import time
import asyncio

app = FastAPI()


@app.get('/')
def root():
    return {"message": "Hello World"}


@app.get("/courses/{course_name}")
def read_course(course_name):
    return {'course_name': course_name}


@app.get("/course-id/{course_id}")
def read_course_id(course_id: int):
    return {"course_id": course_id}


course_items = [{"course_name": "Python"}, {"course_name": "NodeJS"},
                {"course_name": "Machine Learning"}]


@app.get("/courses/")
def read_courses(start: int = 0, end: int = len(course_items)):
    return course_items[start: start + end]
# You can also use the other operations instead of GET:


@app.get("/course/{course_id}")
def read_course_by_id(course_id: int, q: Optional[str] = None):
    if q is not None:
        return {"course_name": course_items[course_id], "q": q}
    return {"course_name": course_items[course_id]}

# pydantics example


class Course(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    author: Optional[str] = None


@app.post("/courses/")
def create_course(course: Course):
    return course


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post('/send-notification/{email}')
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="send_  \
                              notification")
    return {"message": "Notification sent in the background"}


@app.get("/home")
async def home():
    tasks = []
    start = time.time()
    for i in range(2):
        tasks.append(asyncio.create_task(func1()))
        tasks.append(asyncio.create_task(func2()))
    response = await asyncio.gather(*tasks)
    end = time.time()
    return {"response": response, "time_taken": (end - start)}


async def func1():
    await asyncio.sleep(2)
    return "Func1() Completed"


async def func2():
    await asyncio.sleep(1)
    return "Func2() Completed"
# @app.post() can be used if you want the client application to access the
#  route in a POST manner.
# @app.put() can be used if you want the client application to access the
#  route in a PUT manner.
# @app.delete() can be used if you want the client application to access the
#  route in a DELETE manner.
# There are four more operation types which could also be used.
# They are @app.options(), @app.head(), @app.patch(), and @app.trace().

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_course_id(course_code):
    ## define params
    API_HOST = os.getenv("API_HOST")
    endpoint = "/courses"
    url = API_HOST + endpoint
    
    ## make https request
    r = requests.get(url=url, 
                    headers={"Authorization": "Bearer " + os.getenv("API_TOKEN")},
                    params={"enrollment_state": "active"})
    
    ## check response
    course_list = r.json()
    for course in course_list:
        if course["course_code"] == course_code:
            return course["id"]
    raise ValueError("Course not found")


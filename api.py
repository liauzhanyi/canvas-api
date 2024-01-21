import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_HOST = os.getenv("API_HOST")

def get_course_id(course_code):
    ## define params
    endpoint = "/courses"
    url = API_HOST + endpoint
    
    ## make https request
    r = requests.get(url=url, 
                    headers={"Authorization": "Bearer " + os.getenv("API_TOKEN")},
                    params={"enrollment_state": "active"})
    
    ## check response
    course_list = r.json()
    for course in course_list:
        if course["course_code"].lower() == course_code.lower():
            return course["id"]
    
    ## if course not found
    raise ValueError("Course not found")

def list_all_folders(course_id):
    ## define params
    endpoint = f"/courses/{course_id}/folders"
    url = API_HOST + endpoint
    
    ## make https request
    r = requests.get(url=url, 
                    headers={"Authorization": "Bearer " + os.getenv("API_TOKEN")})
    
    ## check response
    if r.status_code != 200:
        raise Exception(f"Error {r.status_code}: {r.reason}")

    ## parse response
    folder_list = r.json()

    return folder_list

def list_files(course_id):
    ## define params
    endpoint = f"/courses/{course_id}/files"
    url = API_HOST + endpoint
    
    ## make https request
    r = requests.get(url=url, 
                    headers={"Authorization": "Bearer " + os.getenv("API_TOKEN")},
                    params={"sort" : "updated_at", 
                            "order" : "desc"})
    
    ## check response
    if r.status_code != 200:
        raise Exception(f"Error {r.status_code}: {r.reason}")
    
    ## parse response
    file_list = r.json()

    return file_list

import requests
import os
from urllib.request import urlretrieve
from dotenv import load_dotenv
from utils import refresh_cache
from datetime import datetime

load_dotenv()
API_HOST = os.getenv("API_HOST")
cache = refresh_cache()

def get_request(url, headers, params=None):
    r = requests.get(url=url, headers=headers, params=params)
    
    ## check response
    if r.status_code != 200:
        raise Exception(f"Error {r.status_code}: {r.reason} initial request failed")
    
    response = r.json()
    
    ## handle api pagination
    while "next" in r.links:
        r = requests.get(url=r.links["next"]["url"], headers=headers, params=params)
        
        ## check response
        if r.status_code != 200:
            raise Exception(f"Error {r.status_code}: {r.reason} subsequent request failed")
        
        response.extend(r.json())
    
    return response

def get_course_id(course_code):
    key = f"{course_code}_id"
    id = cache.read(key)
    
    if id:
        return id
    
    ## if id not in cache, request from api
    print("Course id not found in cache, requesting from api...")
    ## define params
    endpoint = "/courses"
    url = API_HOST + endpoint
    
    ## make https request
    course_list = get_request(url=url, 
                    headers={"Authorization": "Bearer " + os.getenv("API_TOKEN")},
                    params={"enrollment_state": "active"})
    
    ## check response
    for course in course_list:
        if course["course_code"].lower() == course_code.lower():
            ## update cache
            id = course["id"]
            cache.update(key, id)
            cache.store()
            return id

    ## if id not in cache or api == course not found, raise error
    raise ValueError("Course not found")

def list_all_folders(course_id):
    ## define params
    endpoint = f"/courses/{course_id}/folders"
    url = API_HOST + endpoint
    
    ## make https request
    folder_list = get_request(url=url, 
                    headers={"Authorization": "Bearer " + os.getenv("API_TOKEN")})

    return folder_list

def list_files(course_id):
    ## define params
    endpoint = f"/courses/{course_id}/files"
    url = API_HOST + endpoint
    
    ## make https request
    files = get_request(url=url, 
                    headers={"Authorization": "Bearer " + os.getenv("API_TOKEN")},
                    params={"sort" : "updated_at", 
                            "order" : "desc",
                            "per_page" : 50})

    return files

def download_course_files(courses):
    last_update = cache.read("last_update")
    
    ## if last_update not in cache, set to long time ago 1970-01-01 should suffice
    if not last_update:
        last_update = datetime(1970, 1, 1)

    for course in courses:
        id = get_course_id(course)
        files = list_files(id)
        
        ## download file if file is updated after last updated datetime
        for file in files:
            if datetime.fromisoformat(file["updated_at"][:-1]) >= last_update:
                url = file["url"]
                fname = file["display_name"]
                urlretrieve(
                    url, 
                    os.path.join(os.getenv("ROOT"), os.getenv("NEW_FILES_FOLDER"), fname)
                    )
    
    cache.update("last_update", datetime.now())
    cache.store()
    return 200
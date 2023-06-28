import pymongo
import jobbkk
import jobdb
import jobthai
from pythainlp import word_tokenize
import re
from datetime import datetime, date


def remove_special_characters_and_word(lst):
    pattern = r"[^a-zA-Z\s\u0E00-\u0E7F]"
    special_characters = [re.sub(pattern, "", item) for item in lst]
    filtered_list = ["".join(elem.split()) for elem in special_characters]
    words = []
    for i in list(filter(None, filtered_list)):
        if i != " ":
            i.replace(" ", "")
            words.append(i)
    return words


client = pymongo.MongoClient("localhost",27017)
db = client.job

for x in range(1, jobbkk.get_all_page()):
    try:
        for c in jobbkk.get_job_url(x):
            get_job = jobbkk.get_job_detail(c)
            get_job["create_datetime"] = datetime.now()
            result = db.job.insert_one(get_job)
            print(result.acknowledged)

    except:
        pass


for x in range(1, jobdb.get_all_page()):
    try:
        for c in jobdb.get_job_id(x):
            get_job = jobdb.get_job_detail(c)
            get_job["create_datetime"] = datetime.now()
            db.job.insert_one(get_job)
    except:
        pass


for x in range(1, jobthai.get_all_page()):
    try:
        for c in jobthai.get_job_id(x):
            get_job = jobthai.get_job_detail(c)
            get_job["create_datetime"] = datetime.now()
            db.job.insert_one(get_job)
    except:
        pass

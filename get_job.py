from utils import check_region, save_report, report_template
import pymongo
from datetime import datetime

def process_job(input_date):
    client = pymongo.MongoClient("localhost",27017)
    db = client.job
    query = {
        "$expr": {
            "$eq": [
                {"$dateToString": {"format": "%m", "date": "$create_datetime"}},
                {"$dateToString": {"format": "%m", "date": input_date}},
            ]
        }
    }
    job_setting = [i for i in db.group_word.find(query)]
    job = []
    for i in job_setting[:]:
        key = []
        for c in i["keyword"]:
            key.append({c: {"frequency": 0}})
        i["keyword"] = key
        job.append(i)
    report = report_template(job)
    query = {
        "$expr": {
            "$eq": [
                {"$dateToString": {"format": "%Y-%m-%d", "date": "$create_datetime"}},
                {"$dateToString": {"format": "%Y-%m-%d", "date": input_date}},
            ]
        }
    }
    get_all_job = db.job.find(query)
    for get_job in get_all_job:
        for i in job:
            for index, j in enumerate(i["keyword"]):
                job_detail = str(get_job["job_detail"]).lower()
                if list(j.keys())[0] in job_detail:
                    region = check_region(get_job["job_address"])
                    i["keyword"][index][list(j.keys())[0]]["frequency"] = i["keyword"][
                        index
                    ][list(j.keys())[0]]["frequency"] + job_detail.count(
                        list(j.keys())[0]
                    )
                    save_report(
                        report,
                        i,
                        get_job,
                        "job_salary",
                        "salary_count",
                        "salary_sum",
                        "salary",
                        "job_count",
                        region,
                    )
                    break
    db.report.insert_one(report.copy())
    db.keyword.insert_one({"keyword": job[:]})
    return [report.copy(), {"keyword": job[:]}, job_setting[:]]


############
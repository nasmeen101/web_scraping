import requests
from bs4 import BeautifulSoup
import json
import re


def format_number_commas(data):
    try:
        return "{:,.2f}".format(float(data))
    except:
        return ""


def remove_html_tags(text):
    clean_text = re.sub("<[^>]*>", "", text)
    return clean_text


def remove_special_characters(text):
    clean_text = text.replace("\xa0", " ")
    return clean_text


def get_job_id(page=1):
    url = f"https://th.jobsdb.com/th/th/jobs/%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B9%84%E0%B8%AD%E0%B8%97%E0%B8%B5/{page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    job_id = []
    for div in soup.find_all("div", attrs={"data-search-sol-meta": True}):
        data = json.loads(str(div).split("'")[1])
        job_id.append(data["jobId"].split("-")[3])
    return job_id


def get_job_detail(job_id):
    url = "https://xapi.supercharge-srp.co/job-search/graphql?country=th&isSmartSearch=true"
    payload = json.dumps(
        {
            "query": "query getJobDetail($jobId: String, $locale: String, $country: String, $candidateId: ID, $solVisitorId: String, $flight: String) {\n  jobDetail(\n    jobId: $jobId\n    locale: $locale\n    country: $country\n    candidateId: $candidateId\n    solVisitorId: $solVisitorId\n    flight: $flight\n  ) {\n    id\n    pageUrl\n    jobTitleSlug\n    applyUrl {\n      url\n      isExternal\n    }\n    isExpired\n    isConfidential\n    isClassified\n    accountNum\n    advertisementId\n    subAccount\n    showMoreJobs\n    adType\n    header {\n      banner {\n        bannerUrls {\n          large\n        }\n      }\n      salary {\n        max\n        min\n        type\n        extraInfo\n        currency\n        isVisible\n      }\n      logoUrls {\n        small\n        medium\n        large\n        normal\n      }\n      jobTitle\n      company {\n        name\n        url\n        slug\n        advertiserId\n      }\n      review {\n        rating\n        numberOfReviewer\n      }\n      expiration\n      postedDate\n      postedAt\n      isInternship\n    }\n    companyDetail {\n      companyWebsite\n      companySnapshot {\n        avgProcessTime\n        registrationNo\n        employmentAgencyPersonnelNumber\n        employmentAgencyNumber\n        telephoneNumber\n        workingHours\n        website\n        facebook\n        size\n        dressCode\n        nearbyLocations\n      }\n      companyOverview {\n        html\n      }\n      videoUrl\n      companyPhotos {\n        caption\n        url\n      }\n    }\n    jobDetail {\n      summary\n      jobDescription {\n        html\n      }\n      jobRequirement {\n        careerLevel\n        yearsOfExperience\n        qualification\n        fieldOfStudy\n        industryValue {\n          value\n          label\n        }\n        skills\n        employmentType\n        languages\n        postedDate\n        closingDate\n        jobFunctionValue {\n          code\n          name\n          children {\n            code\n            name\n          }\n        }\n        benefits\n      }\n      whyJoinUs\n    }\n    location {\n      location\n      locationId\n      omnitureLocationId\n    }\n    sourceCountry\n  }\n}\n",
            "variables": {
                "jobId": job_id,
                "country": "th",
                "locale": "th",
                "candidateId": "",
            },
        }
    )
    headers = {
        "authority": "xapi.supercharge-srp.co",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://th.jobsdb.com",
        "referer": "https://th.jobsdb.com/",
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    resp = requests.request("POST", url, headers=headers, data=payload).json()
    plain_text = remove_html_tags(
        resp["data"]["jobDetail"]["jobDetail"]["jobDescription"]["html"]
    )
    clean_text = remove_special_characters(plain_text)
    return {
        "job_type": resp["data"]["jobDetail"]["jobDetail"]["jobRequirement"][
            "employmentType"
        ],
        "job_address": resp["data"]["jobDetail"]["location"][0]["location"],
        "job_salary": f'{format_number_commas(resp["data"]["jobDetail"]["header"]["salary"]["min"])} - {format_number_commas(resp["data"]["jobDetail"]["header"]["salary"]["max"])}',
        "job_title": resp["data"]["jobDetail"]["header"]["jobTitle"],
        "job_detail": clean_text,
        "job_url": resp["data"]["jobDetail"]["pageUrl"],
    }


def get_all_page():
    url = "https://th.jobsdb.com/th/th/jobs/%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B9%84%E0%B8%AD%E0%B8%97%E0%B8%B5/1"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    page = soup.find_all("strong", {"class": "y44q7i3"})[1]
    page = int(str(page.text).split("-")[1])
    return page


# print(get_job_id())
# print(get_job_detail("300003002876834"))

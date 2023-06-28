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
    url = "https://api.jobthai.com/v1/graphql"
    payload = json.dumps(
        {
            "variables": {
                "searchJobsFilter": {
                    "subjobtype": "146,132,149,140,150",
                    "l": "th",
                    "page": page,
                },
                "orderBy": "RELEVANCE_SEARCH",
                "staticDataVersion": {},
            },
            "query": "query ($searchJobsFilter: JobsSearchFilter, $orderBy: JobOrderBy, $staticDataVersion: StaticDataVersion) {\n  searchJobs(\n    filter: $searchJobsFilter\n    orderBy: $orderBy\n    staticDataVersion: $staticDataVersion\n  ) {\n    data {\n      total\n      data {\n        id\n        companyID\n        jobTitle\n        companyName\n        companyLogo\n        province {\n          id\n          name\n        }\n        district {\n          id\n          name\n        }\n        industrial {\n          id\n          name\n        }\n        disabledPerson {\n          id\n          name\n        }\n        country {\n          id\n          name\n        }\n        transitStations {\n          id\n          distance\n          type\n          name\n        }\n        isTopCompany\n        workLocation\n        salary\n        urgent {\n          id\n          name\n        }\n        jobType {\n          id\n          name\n        }\n        province {\n          id\n          name\n        }\n        region {\n          id\n          name\n        }\n        tags\n        updatedAt\n      }\n    }\n  }\n}\n",
        }
    )
    headers = {
        "authority": "api.jobthai.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "client-name": "jobthai-upgrade-web",
        "clientid": "NlnJk4E3pLR2TBGu930OQXJAiy9mJ7sWpZ8w8RAq",
        "content-type": "application/json",
        "cookie": "_gid=GA1.2.1888536833.1681766467; _fbp=fb.1.1681766467510.403495477; _ga_F84QES3RXH=GS1.1.1681766467.1.1.1681766543.60.0.0; _ga=GA1.2.1941984487.1681766467; _gat_UA-7749907-18=1",
        "dnt": "1",
        "event-page": "job-list",
        "event-section": "search-button",
        "guest-id": "",
        "lang": "th",
        "origin": "https://www.jobthai.com",
        "referer": "https://www.jobthai.com/",
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "timestamp": "2023-04-17T21:22:24.163Z",
        "tn-user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "user": "null",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "user-agent-client": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    job_id = []
    for i in response["data"]["searchJobs"]["data"]["data"]:
        job_id.append(i["id"])
    return job_id


def get_job_detail(job_id):
    url = "https://api.jobthai.com/v1/graphql"
    payload = json.dumps(
        {
            "variables": {
                "id": job_id,
                "l": "th",
                "isJobbuffer": False,
                "staticDataVersion": {},
            },
            "query": "query ($id: Int!, $l: Language, $isJobbuffer: Boolean, $staticDataVersion: StaticDataVersion) {\n  getJobRawData(\n    id: $id\n    l: $l\n    isJobbuffer: $isJobbuffer\n    staticDataVersion: $staticDataVersion\n  ) {\n    data {\n      _id\n      title\n      company {\n        _id\n        name\n        logo\n        website\n        businessType {\n          id\n          name\n        }\n        pictures\n        detail\n        benefit\n        specialContent {\n          intro {\n            header {\n              th\n              en\n            }\n            headerPlatform {\n              desktop {\n                th\n                en\n              }\n              app {\n                th\n                en\n              }\n              mobile {\n                th\n                en\n              }\n            }\n            descriptionPlatform {\n              desktop\n              app\n              mobile\n            }\n            videos {\n              id\n              videoPath {\n                desktop\n                app\n                mobile\n              }\n              thumnailPath {\n                desktop\n                app\n                mobile\n              }\n            }\n            videosDesktop {\n              id\n              videosPath\n              thumnailPath\n            }\n            images {\n              id\n              imagePath {\n                desktop\n                app\n                mobile\n              }\n              thumnailPath {\n                desktop\n                app\n                mobile\n              }\n            }\n            imagesDesktop {\n              id\n              imagePath\n              thumnailPath\n            }\n            imagesApp {\n              id\n              imagePath\n              thumnailPath\n            }\n            imagesMobile {\n              id\n              imagePath\n              thumnailPath\n            }\n          }\n          blogs {\n            header {\n              th\n              en\n            }\n            headerPlatform {\n              desktop {\n                th\n                en\n              }\n              app {\n                th\n                en\n              }\n              mobile {\n                th\n                en\n              }\n            }\n            data {\n              id\n              imagePath {\n                desktop\n                app\n                mobile\n              }\n              title\n              description\n              url\n              desktop {\n                title\n                description\n                url\n              }\n            }\n            dataDesktop {\n              id\n              title\n              description\n              url\n              imagePath\n            }\n          }\n          getConnected {\n            headerPlatform {\n              desktop {\n                th\n                en\n              }\n            }\n            descriptionPlatform {\n              desktop\n            }\n            imagesDesktop {\n              id\n              imagePath\n              thumnailPath\n            }\n          }\n        }\n        contact {\n          name\n          tel\n          fax\n          lineID\n          emails\n          location {\n            address\n            map\n            direction\n            latitude\n            longitude\n            province {\n              id\n              name\n            }\n            district {\n              id\n              name\n            }\n            subdistrict {\n              id\n              name\n            }\n            country {\n              id\n              name\n            }\n            industrialName\n            zipcode\n          }\n        }\n      }\n      properties\n      benefit\n      applyMethod\n      description\n      workLocation {\n        address\n        country {\n          name\n        }\n        province {\n          id\n          name\n        }\n        district {\n          id\n          name\n        }\n        subdistrict {\n          name\n        }\n        industrial {\n          id\n          name\n        }\n        industrialName\n        latitude\n        longitude\n        map\n        direction\n      }\n      numberOfPosition\n      contact {\n        name\n        tel\n        location {\n          address\n          province {\n            id\n            name\n          }\n          province {\n            id\n            name\n          }\n          district {\n            name\n          }\n          subdistrict {\n            name\n          }\n          industrialName\n          country {\n            name\n          }\n          zipcode\n        }\n        lineID\n        fax\n        emails\n      }\n      disabledPerson {\n        id\n        name\n      }\n      englishApply\n      salary\n      urgent {\n        id\n        name\n      }\n      transitStations {\n        id\n        type\n        distance\n        name\n        routes {\n          id\n          name\n        }\n      }\n      busRoutes {\n        id\n        routes {\n          id\n          distance\n        }\n      }\n      jobType {\n        id\n        name\n      }\n      subjobType {\n        id\n        name\n      }\n      businessType {\n        id\n        name\n      }\n      updatedAt\n      website\n      applyExternalLink\n      hiddenApplyButton\n      tags\n      employmentType\n    }\n  }\n}\n",
        }
    )
    headers = {
        "authority": "api.jobthai.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "client-name": "jobthai-upgrade-web",
        "clientid": "NlnJk4E3pLR2TBGu930OQXJAiy9mJ7sWpZ8w8RAq",
        "content-type": "application/json",
        "cookie": "_gid=GA1.2.1888536833.1681766467; _fbp=fb.1.1681766467510.403495477; __gads=ID=266e37f1e01b6d4e-22214c9b36df0064:T=1681766544:RT=1681766544:S=ALNI_MacbkyIhsEQiusprQ_s41g6M8r12Q; __gpi=UID=00000bf7840e93be:T=1681766544:RT=1681766544:S=ALNI_MZoAj919C-XQQapMAt1LN2ou2frAQ; connect.sid=s%3A_Rr5FCBqC6zxAQtznlv7L3lPlffFyiXe.kJQoUCKj0oKUFDToIdyC7R%2FcENSEeQWlRNr3ACtKUxI; _ga_F84QES3RXH=GS1.1.1681766467.1.1.1681766749.60.0.0; _ga=GA1.2.1941984487.1681766467; _gat_UA-7749907-18=1",
        "dnt": "1",
        "guest-id": "168176662068661257497262a83d10e5c2e4e",
        "lang": "th",
        "origin": "https://www.jobthai.com",
        "page": "jobDetail",
        "referer": "https://www.jobthai.com/",
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "timestamp": "2023-04-17T21:25:49.781Z",
        "tn-user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "user": "null",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "user-agent-client": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }

    resp = requests.request("POST", url, headers=headers, data=payload).json()
    return {
        "job_type": resp["data"]["getJobRawData"]["data"]["employmentType"],
        "job_address": resp["data"]["getJobRawData"]["data"]["workLocation"][
            "province"
        ]["name"],
        "job_salary": " ".join(
            str(resp["data"]["getJobRawData"]["data"]["salary"]).split(" ")[:3]
        ),
        "job_title": resp["data"]["getJobRawData"]["data"]["title"],
        "job_detail": str(resp["data"]["getJobRawData"]["data"]["description"]).replace(
            "\r\n", " "
        ),
        "job_url": f"https://www.jobthai.com/th/company/job/{job_id}",
    }


def get_all_page():
    url = "https://www.jobthai.com/th/jobs"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    page = soup.find_all("span", {"id": "count-position"})[0]
    page = int(str(page.text).split(" ")[2].replace(",", ""))
    return int(page / 20)


# print(get_all_page())
# print(get_job_detail(""))
# print(get_job_id(1))

from bs4 import BeautifulSoup
import requests


def get_job_url(page=1):
    url = requests.get(
        f"https://www.jobbkk.com/%E0%B8%AB%E0%B8%B2%E0%B8%87%E0%B8%B2%E0%B8%99/%E0%B9%84%E0%B8%AD%E0%B8%97%E0%B8%B5/{page}"
    )
    soup = BeautifulSoup(url.content, "html.parser", from_encoding="utf-8")
    data = soup.find_all("a", {"class": "positon-work"})
    job_url = []
    for i in data:
        if i.has_attr("href"):
            if "detailurgent" not in i["href"]:
                job_url.append(i["href"])
    return job_url


def get_all_page():
    url = requests.get(
        f"https://www.jobbkk.com/%E0%B8%AB%E0%B8%B2%E0%B8%87%E0%B8%B2%E0%B8%99/%E0%B9%84%E0%B8%AD%E0%B8%97%E0%B8%B5"
    )
    soup = BeautifulSoup(url.content, "html.parser", from_encoding="utf-8")
    data = soup.find_all(
        "li", {"class": "col-md-4 col-sm-4 col-xs-6 search-job-number"}
    )
    page = str(data[0].text).strip()
    page = str(page).split(" ")
    return int(int(str(page[-2]).replace(",", "")) / 25)


def get_job_detail(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser", from_encoding="utf-8")
    data = soup.find_all("div", {"class": "col-md-8 col-sm-8 col-xs-6"})
    job_title = str(data[0].text).strip()
    data = soup.find_all(
        "div", {"class": "col-md-12 col-sm-12 col-xs-12 margin-bottom"}
    )
    job_head_detail = {}
    for i in data[2]:
        if i.text != "\n":
            t = str(i.text.strip()).split(":")
            if len(t) > 1:
                key = t[0].replace(" ", "")
                value = t[1].strip()
                if key == "รูปแบบงาน":
                    job_head_detail["job_type"] = value
                if key == "สถานที่ปฏิบัติงาน":
                    job_head_detail["job_address"] = value.split("(")[0]
                if key == "เงินเดือน(บาท)":
                    job_head_detail["job_salary"] = value
    job_detail = []
    for i in data[3]:
        if i.text != "\n":
            if i.text != "หน้าที่ความรับผิดชอบ":
                t = str(i.text).split("•")
                for x in t:
                    if x != "":
                        job_detail.append(x.strip())
    job_head_detail["job_title"] = job_title
    job_head_detail["job_detail"] = " | ".join(job_detail)
    job_head_detail["job_url"] = url
    return job_head_detail


# print(get_job_url(page=2))
# print(get_all_page())
# print(get_job_detail("https://www.jobbkk.com/jobs/detail/207873/1142209"))

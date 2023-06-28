def check_region(province):
    regions = {
        "north": [
            "เชียงใหม่",
            "แม่ฮ่องสอน",
            "เชียงราย",
            "ลำพูน",
            "ลำปาง",
            "พะเยา",
            "แพร่",
            "น่าน",
            "อุตรดิตถ์",
            "ตาก",
            "สุโขทัย",
            "พิษณุโลก",
            "กำแพงเพชร",
            "เพชรบูรณ์",
            "พิจิตร",
        ],
        "northeast": [
            "กาฬสินธุ์",
            "ขอนแก่น",
            "ชัยภูมิ",
            "นครพนม",
            "นครราชสีมา",
            "บุรีรัมย์",
            "มหาสารคาม",
            "มุกดาหาร",
            "ยโสธร",
            "ร้อยเอ็ด",
            "เลย",
            "ศรีสะเกษ",
            "สกลนคร",
            "สุรินทร์",
            "หนองคาย",
            "หนองบัวลำภู",
            "อุดรธานี",
            "อุบลราชธานี",
            "อำนาจเจริญ",
        ],
        "central": [
            "กรุงเทพมหานคร",
            "อุทัยธานี",
            "ชัยนาท",
            "นครสวรรค์",
            "นนทบุรี",
            "ปทุมธานี",
            "พระนครศรีอยุธยา",
            "ลพบุรี",
            "สมุทรปราการ",
            "สมุทรสงคราม",
            "สมุทรสาคร",
            "สระบุรี",
            "สิงห์บุรี",
            "อ่างทอง",
        ],
        "east": [
            "ชลบุรี",
            "ระยอง",
            "จันทบุรี",
            "ตราด",
            "นครนายก",
            "ฉะเชิงเทรา",
            "ปราจีนบุรี",
            "สระแก้ว",
        ],
        "western": [
            "กาญจนบุรี",
            "ประจวบคีรีขันธ์",
            "สุพรรณบุรี",
            "เพชรบุรี",
            "นครปฐม",
            "ราชบุรี",
        ],
        "south": [
            "กระบี่",
            "ชุมพร",
            "ตรัง",
            "นครศรีธรรมราช",
            "นราธิวาส",
            "ปัตตานี",
            "พังงา",
            "พัทลุง",
            "ภูเก็ต",
            "ยะลา",
            "ระนอง",
            "สงขลา",
            "สตูล",
            "สุราษฎร์ธานี",
        ],
    }

    for region, provinces in regions.items():
        if province in provinces:
            return region
    return ""


def save_report(
    report, i, get_job, job_salary, salary_count, salary_sum, salary, job_count, region
):
    try:
        salary_job = (
            str(get_job[job_salary]).replace(",", "").replace(" ", "").split("-")
        )
        salary_job = float(salary_job[0]) + float(salary_job[1]) / 2
        report[i["job"]][salary_count] = report[i["job"]][salary_count] + 1
        report[i["job"]][salary_sum] = report[i["job"]][salary_sum] + salary_job
        report[i["job"]][salary] = round(
            report[i["job"]][salary_sum] / report[i["job"]][salary_count], 2
        )
        report[i["job"]][job_count] = report[i["job"]][job_count] + 1
        report[i["job"]][region + "_count"] = report[i["job"]][region + "_count"] + 1

        report[i["job"]]["north"] = round(
            report[i["job"]]["north_count"] * 100 / report[i["job"]][job_count], 2
        )
        report[i["job"]]["northeast"] = round(
            report[i["job"]]["northeast_count"] * 100 / report[i["job"]][job_count], 2
        )
        report[i["job"]]["central"] = round(
            report[i["job"]]["central_count"] * 100 / report[i["job"]][job_count], 2
        )
        report[i["job"]]["east"] = round(
            report[i["job"]]["east_count"] * 100 / report[i["job"]][job_count], 2
        )
        report[i["job"]]["south"] = round(
            report[i["job"]]["south_count"] * 100 / report[i["job"]][job_count], 2
        )
    except:
        pass


def report_template(job):
    report = {}
    for i in job:
        report[i["job"]] = {
            "job_count": 0,
            "salary": 0,
            "salary_count": 0,
            "salary_sum": 0,
            "north": 0,
            "northeast": 0,
            "central": 0,
            "east": 0,
            "western": 0,
            "south": 0,
            "north_count": 0,
            "northeast_count": 0,
            "central_count": 0,
            "east_count": 0,
            "western_count": 0,
            "south_count": 0,
        }
    return report

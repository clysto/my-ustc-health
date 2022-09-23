import logging
import re
from datetime import datetime, timedelta, timezone

import requests


class LeaveReporter:
    def __init__(self, session: requests.Session) -> None:
        self.session = session
        # 东八区
        self.cst = timezone(timedelta(hours=8))

    def report(self):
        form = {"return_college[]": "先研院", "reason": "出校", "t": 4}
        result = self.session.get("https://weixine.ustc.edu.cn/2020/apply/daliy/i?t=4")
        token = re.findall(r"name=\"_token\" value=\"(.+)\"", result.text)[0]
        time_now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
        time_now = time_now_utc.astimezone(self.cst)
        form["start_date"] = datetime.strftime(time_now, "%Y-%m-%d %H:%M:%S")
        form["end_date"] = datetime.strftime(time_now, "%Y-%m-%d 23:59:59")
        form["_token"] = token
        logging.info("开始出校申请")
        result = self.session.post(
            "https://weixine.ustc.edu.cn/2020/apply/daliy/ipost",
            data=form,
            headers={
                "content-type": "application/x-www-form-urlencoded",
            },
        )
        return result.status_code == 200

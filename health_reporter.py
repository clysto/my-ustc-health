import logging
import re

import requests
from bs4 import BeautifulSoup


class HealthReporter:
    def __init__(self, session: requests.Session) -> None:
        self.session = session

    def report(self, health_info: dict):
        result = self.session.get("https://weixine.ustc.edu.cn/2020")

        token = re.findall(r"name=\"_token\" value=\"(.+)\"", result.text)[0]
        health_info["_token"] = token

        logging.info("开始上报健康信息")

        result = self.session.post(
            "http://weixine.ustc.edu.cn/2020/daliy_report",
            data=health_info,
            headers={
                "content-type": "application/x-www-form-urlencoded",
            },
        )
        # 判断是否成功
        soup = BeautifulSoup(result.text, "html.parser")
        msg = soup.select_one(".flash-message p").find(text=True).strip()
        match = re.findall(r"上报成功", msg)
        logging.info(msg)
        if len(match) == 0:
            return False
        else:
            return True

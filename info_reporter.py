import json
import logging
import re
import subprocess

import requests


class InfoReporter:
    def __init__(self, session: requests.Session) -> None:
        self.session = session

    def gen_image(self):
        p = subprocess.Popen(
            ["./image"],
            cwd="./image",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        p.communicate()

    def report(self):
        result = self.session.get("https://weixine.ustc.edu.cn/2020/upload/xcm")

        match = re.finditer(r"_token:\s+'(.+)'", result.text)
        token = next(match)[1]
        match = re.finditer(r"'gid':\s+'(.+)'", result.text)
        gid = next(match)[1]
        match = re.finditer(r"'sign':\s+'(.+)'", result.text)
        sign = next(match)[1]

        # 生成截图
        logging.info("生成行程码")
        self.gen_image()

        files = {
            "file": open("image/a.png", "rb"),
        }

        data = {
            "_token": token,
            "gid": gid,
            "sign": sign,
            "t": 1,
            "id": "WU_FILE_0",
        }

        logging.info("上传行程码")
        result = self.session.post(
            "https://weixine.ustc.edu.cn/2020img/api/upload_for_student",
            files=files,
            data=data,
        )

        status = json.loads(result.text)

        if status["status"] is False:
            logging.error("上传行程码失败")
            logging.info(status["message"])
            return False

        logging.info(status["message"])
        return True

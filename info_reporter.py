import logging
import re
import json
import subprocess

import requests

from ustc_credential import UstcCredential


class InfoReporter:
    def __init__(self, credential: UstcCredential) -> None:
        self.credential = credential

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
        session = requests.Session()
        logging.info("使用学号和密码登陆")
        try:
            result = self.credential.login(
                session,
                "https://weixine.ustc.edu.cn/2020/upload/xcm",
                "https://weixine.ustc.edu.cn/2020/caslogin",
                "https://weixine.ustc.edu.cn/2020/upload/xcm",
            )
        except Exception as err:
            logging.error(err)
            return
        logging.info("登陆成功")

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
        result = session.post(
            "https://weixine.ustc.edu.cn/2020img/api/upload_for_student",
            files=files,
            data=data,
        )

        status = json.loads(result.text)

        if status["status"] is False:
            logging.error("上传行程码失败")

        logging.info(status["message"])

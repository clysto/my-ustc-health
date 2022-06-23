#!/usr/bin/env python3

import argparse
import configparser
import logging

import requests

from health_reporter import HealthReporter
from info_reporter import InfoReporter
from ustc_credential import UstcCredential

FORMAT = "%(asctime)s  %(levelname)-8s  %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


def parse_config(config_file):
    # 读取配置文件
    logging.info(f"读取配置文件 {config_file}")
    config = configparser.ConfigParser()
    config.read(config_file)
    if "credential" not in config:
        raise Exception("配置文件缺少 credential 部分")
    if "health" not in config:
        raise Exception("配置文件缺少 health 部分")
    if "student_id" not in config["credential"]:
        raise Exception("配置文件缺少 student_id")
    if "password" not in config["credential"]:
        raise Exception("配置文件缺少 password")
    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="USTC 健康自动上报")
    parser.add_argument("--config", help="配置文件路径", default="config.ini")
    args = parser.parse_args()

    # 解析配置文件
    try:
        config = parse_config(args.config)
    except Exception as err:
        logging.error(err)
        exit(-1)

    # 读取学号和密码
    student_id = config["credential"]["student_id"]
    password = config["credential"]["password"]

    credential = UstcCredential(student_id, password)

    # 开始登录
    session = requests.Session()
    logging.info("使用学号和密码登陆")
    try:
        result = credential.login(
            session,
            "https://weixine.ustc.edu.cn/2020",
            "https://weixine.ustc.edu.cn/2020/caslogin",
            "https://weixine.ustc.edu.cn/2020/home",
        )
    except Exception as err:
        logging.error("登录失败", err)
        exit(-1)
    logging.info("登录成功")

    health_reporter = HealthReporter(session)
    info_reporter = InfoReporter(session)

    health_try_cout = 5
    while health_try_cout > 0:
        # 读取上报信息
        health_info = dict(config["health"])
        # 信息上报
        if health_reporter.report(health_info):
            break
        health_try_cout -= 1

    info_try_count = 5
    while info_try_count > 0:
        # 上传健康信息
        if info_reporter.report():
            break
        info_try_count -= 1

    if health_try_cout == 0 or info_try_count == 0:
        exit(-1)
    else:
        exit(0)

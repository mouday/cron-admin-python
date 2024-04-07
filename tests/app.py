# -*- coding: utf-8 -*-
"""
@File    : app.py
@Date    : 2024-04-04
"""
import logging
# pip install requests flask
import time

from flask import Flask

from cron_runner import CronRunner, CronAdminContext

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

app = Flask(__name__)

# 配置
runner = CronRunner(app)
runner.set_host('http://127.0.0.1:8082')


# 模拟耗时任务
@runner.add_task_decorator('run_job')
def run_job(ctx: CronAdminContext):
    ctx.log("data: {}".format(ctx))

    time.sleep(5)

    ctx.log('run_job complete')


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)

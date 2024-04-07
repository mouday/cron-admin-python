# -*- coding: utf-8 -*-
"""
@File    : context.py
@Date    : 2024-04-07
"""
import requests

from cron_runner import config


class CronAdminContext(object):
    def __init__(self, host, data):
        self.host = host or config.DEFAULT_CRON_ADMIN_HOST
        self.data = data
        self.logs = []

    def log(self, msg):
        self.logs.append(msg)

    @property
    def task_log_id(self):
        return self.data['taskLogId']

    def report(self, err):
        data = {
            'taskLogId': self.task_log_id,
            'status': 4 if err else 3,
            'text': '\n'.join(self.logs),
        }

        res = requests.post(self.host + config.API_REPORT_TASK_STATUS, json=data)

        if not res.ok:
            res.raise_for_status()

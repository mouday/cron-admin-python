# -*- coding: utf-8 -*-
"""
@File    : core.py
@Date    : 2024-04-07
"""

import traceback
from concurrent.futures import ThreadPoolExecutor

from flask import request, jsonify

from cron_runner import config, context

executor = ThreadPoolExecutor()


def run_task_wrap(func):
    def run_task(ctx):
        err = None

        try:
            func(ctx)
        except Exception as e:
            err = traceback.format_exc()
            ctx.log(err)

        ctx.report(err)

    return run_task


class CronRunner(object):
    def __init__(self, app):
        self.app = app
        self.tasks = {}
        self.host = None
        # auto
        self.register_router()

    def register_router(self):
        self.app.add_url_rule(rule=config.API_START_TASK, endpoint=None, view_func=self.start_task, methods=['POST'])

    def start_task(self):
        data = request.get_json()
        task_name = request.args.get('task_name')
        ctx = context.CronAdminContext(self.host, data)
        task_func = self.tasks[task_name]

        executor.submit(run_task_wrap(task_func), ctx)

        return jsonify({'msg': 'success', 'data': None, 'code': 0})

    def add_task(self, name, func):
        self.tasks[name] = func

    def add_task_decorator(self, name):
        this = self

        def inner(func):
            this.add_task(name, func)

        return inner

    def set_host(self, host):
        self.host = host

# -*- coding:utf-8 -*-

import datetime
import pyperclip
from string import Template
from collections import defaultdict


class Job:

    def __init__(self):
        pass

    @staticmethod
    def write_week_report():
        # 获取本周起始日期
        today = datetime.date.today()
        week_start = today - datetime.timedelta(days=today.weekday())
        # 周五 5-1-w
        week_end = today + datetime.timedelta(days=4 - today.weekday())
        # 获取下周起始日期
        next_start = week_start + datetime.timedelta(days=7)
        next_end = week_end + datetime.timedelta(days=7)

        template = Template("""
| 项目 | 总结 | 时间 |
| :---- | :---- | :----: |
$summary

- - -
## 下周重点工作

| 项目 | 任务 | 时间 |
| :---- | :---- | :----: |
$plan
""")
        summary = defaultdict(lambda: {})
        summary['project1'] = {
            "name": "信审平台",
            "content": ['完成多语言切换', '所有订单列表、借贷订单管理添加用户ID、订单ID/借据ID筛选'],
        }
        summary['project2'] = {
            "name": "投资人平台",
            "content": ['完成多语言切换', '所有订单列表、借贷订单管理添加用户ID、订单ID/借据ID筛选'],
        }
        summary['project3'] = {
            "name": "业务后台",
            "content": ['修改2.1测试bug', '完成闪屏、底部tab配置功能的开发', '添加操作日志埋点'],
        }
        plan = defaultdict(lambda: {})
        plan['project1'] = {
            "name": "业务平台",
            "content": ['完成多语言词条整理', '提交场测'],
        }
        plan['project2'] = {
            "name": "信审平台",
            "content": ['完成多语言切换'],
        }
        plan['project3'] = {
            "name": "投资人平台",
            "content": ['自测2.1功能模块，并修复测试bug'],
        }

        week_start = week_start.strftime('%Y.%m.%d')
        week_end = week_end.strftime('%Y.%m.%d')
        duration = week_start + "-" + week_end
        summary_list = []
        for (key, value) in summary.items():
            summary_tmp = Template('| $project | $content | $duration  |')
            content = [str(key + 1) + '、' + item for (key, item) in enumerate(value['content'])]
            tmp = summary_tmp.substitute(project=value['name'], content="<br>".join(content),
                                         duration=duration)
            summary_list.append(tmp)

        next_start = next_start.strftime('%Y.%m.%d')
        next_end = next_end.strftime('%Y.%m.%d')
        next_duration = next_start + "-" + next_end
        plan_list = []
        for (key, value) in plan.items():
            summary_tmp = Template('| $project | $content | $duration  |')
            content = [str(key + 1) + '、' + item for (key, item) in enumerate(value['content'])]
            tmp = summary_tmp.substitute(project=value['name'], content="<br>".join(content),
                                         duration=next_duration)
            plan_list.append(tmp)

        report = template.substitute(summary="\n".join(summary_list), plan="\n".join(plan_list))
        # 复制到剪贴板
        pyperclip.copy(report)
        print(report)


def main():
    # job = Job()
    Job.write_week_report()


if __name__ == '__main__':
    main()

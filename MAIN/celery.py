from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmdb.settings.local')
# 实例化
# app = Celery('celeryPro', include=['message.tasks'])
# app = Celery('celeryPro', backend='redis://127.0.0.1:6379/1')
app = Celery('cmdb')

# namespace='CELERY'作用是允许你在Django配置文件中对Celery进行配置
# 但所有Celery配置项必须以CELERY开头，防止冲突
app.config_from_object('celery_config', namespace='CELERY')
# app.config_from_object(config, namespace='CELERY')
# 自动从Django的已注册app中发现任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request:{0!r}'.format(self.request))
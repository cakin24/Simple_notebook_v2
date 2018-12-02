# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^topics/$', views.topics, name='topics'),
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    
    # 用于添加新主题的网页
    # 该URL 模式将请求交给视图函数 new_topic()
    url(r'^new_topic/$', views.new_topic, name='new_topic'),

    # 用于添加新条目的页面
    # 这个 URL 模式与形式为 http://localhost:8000/new_entry/ id / 的 URL 匹配，其中 id  是一个与主题 ID 匹配的数字。
    # 代码 (?P<topic_id>\d+) 捕获一个数字值，并将其存储在变量 topic_id 中。
    # 请求的 URL 与这个模式匹配时， Django 将请求和主题 ID 发送给函数 new_entry() 。
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    
    # 用于编辑条目的页面
    # 在 URL （如 http://localhost:8000/edit_entry/1/ ）中传递的 ID 存储在形参 entry_id 中。
    # 这个 URL 模式将预期匹配的请求发送给视图函数 edit_entry()
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry,
        name='edit_entry'),
]

'''定义learning_logs的URL模式'''
from django.urls import path, re_path
from . import views

# 声明app_name，防止项目中path语句报错
app_name = 'learning_logs'

urlpatterns = [
    # 主页
    # re_path(r'^$', views.index, name='index'),与下句等价
    path('', views.index, name='index'),

    # 显示所有的主题
    # re_path(r'^topics/$', views.topics, name='topics'),与下句等价
    path('topics/', views.topics, name='topics' ),

    # 特定主题的详细页面
    re_path('topics/(?P<topic_id>\d+)/', views.topic, name='topic'),

    # 用于添加新主题的网页
    path('new_topic/', views.new_topic, name='new_topic'),

    # 用于添加新条目的页面
    re_path('new_entry/(?P<topic_id>\d+)/', views.new_entry, name='new_entry'),

    # 用于编辑条目的页面
    re_path('edit_entry/(?P<entry_id>\d+)/', views.edit_entry, name='edit_entry'),

    # 用于显示个人所有的主题
    path('my_topics/', views.my_topics, name='my_topics'),

    # 用于删除自有条目的页面
    re_path('delete_entry/(?P<entry_id>\d+)/', views.delete_entry, name='delete_entry'),

    # 用于删除自有主题的页面
    re_path('delete_topic/(?P<topic_id>\d+)/', views.delete_topic, name='delete_topic'),

]
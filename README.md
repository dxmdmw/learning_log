# learning_log
Create a Learning Log Website
# 使用Django开发LearningLog项目
>以下是我在学习《Python编程：从入门到实践》一书时开发LearningLog项目的学习笔记。搭建好的网站在：https://evilgenius.herokuapp.com/。
-------------------------------------------
2018.11.5更新：
优化了网站显示页面，增加「站点精选」导航栏。
1. 网站首页
![网站首页预览](http://pic.yupoo.com/dxmdmw/1ac87f23/380b0544.jpg)
2. 网站截图
![网站截图1](http://pic.yupoo.com/dxmdmw/e62aacf5/3a509ef7.jpg)
![网站截图2](http://pic.yupoo.com/dxmdmw/160deb9c/139fa97b.jpg)
![网站截图3](http://pic.yupoo.com/dxmdmw/6b6f91b7/bd88df50.jpg)


-------------------------------------------
2018.10.26更新：
1. 未登录用户现在可以查看「公开」的主题和条目。
2. 支持markdown编辑模式！感谢Django-mdeditor，django-markdown-deux！
-------------------------------------------
## 1. 建立项目
### 1.1 制定规范
- 以规范的范式描述项目目标、功能、外观、用户界面

编写一个名为「学习笔记」的Web应用程序，让用户能够记录感兴趣的主题，并在学习每个主题的过程中添加日志条目。「学习笔记」的主页对这个网站进行描述，并邀请用户注册或登录。用户登录后，就可创建新主题、添加新条目以及阅读既有的条目。

--------------------------------
## 2. 建立虚拟环境
### 2.1 新建目录「learning_log」
### 2.2 终端切换到此目录，创建虚拟环境

```py
learning_log> python -m venv 11_env
```
如遇到Python版本低或系统未正确设置，无法使用模块venv，可安装virtualenv包：
```py
> pip install --user virtualenv
```
然后在终端切换到目录learning_log，并创建虚拟环境：
```py
>learning_log> virtualenv 11_env
```
### 2.3 激活虚拟环境
```py
>learning_log>11_env\Scripts\activate
```
### 2.4 安装Django
    (11_env)learning_log> pip install Django
    
### 2.5 在Django中创建项目
```py
(11_env)learning_log> django-admin startproject learning_log .
```
注意命令末尾的句点，它让新项目使用合适的目录结构，这样开发完成后可轻松地将应用程序部署到服务器。

目录learning_log会包含4个文件:
- \_\_init__.py
- settings.py ：指定Django如何与系统交互以及如何管理项目，开发过程中会在其中修改与添加。
- urls.py：告诉Django应创建哪些网页来响应浏览器请求。
- wsgi.py：帮助Django提供它创建的文件。web server gateway interface（Web服务器网关接口）。

### 2.6 创建数据库
```py
(11_env)learning_log>python manage.py migrate
```
### 2.7 运行并查看项目
```py
(11_env)learning_log> python manage.py runserver
```
浏览器地址输入：http://localhost:8000/ 或
http://127.0.0.1:8000/
如果出现错误消息，改为runserver 8001端口往上测试到可用端口为止
-----------------------------------
## 3. 创建应用程序
	(11_env)learning_log> python manage.py startapp learning_logs
这一步会创建：
· models.py
· admin.py
· views.py
###	3.1 定义模型
用户需要在学习笔记中创建多主题，输入的每个条目都与特定主题相连，条目以文本方式显示。还要存储每个条目的时间戳，以便告诉用户条目创建时间。

模型告诉Django如何处理应用程序中存储的数据。模型=类，包含属性和方法。
```py
from django.db import models

class Topic(models.Model):
    '''用户学习的主题'''
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text
```
###	3.2 激活模型
通过learning_log>settings.py告诉Django哪些应用程序安装在项目中。
打开learning_log>settings.py：
```py
--snip--
INSTALLED_APPS = [
    --snip--
    
    # 我的应用程序
    'learning_logs',
]
--snip--
```
###	3.3 修改数据库，使能储存新模型
    (11_env)learning_logs> python manage.py makemigrations learning_logs
    
###	3.4 应用迁移
    (11_env)learning_logs>python manage.py migrate

------------------------------------
## 4. Django管理网站
###	4.1 创建超级用户
	(11_env)learning_logs>python manage.py createsuperuser
###	4.2 向管理网站注册模型
通过learning_logs>admin.py向管理网站注册Topic:
```py
from django.contrib import admin

# 导入要注册的模型Topic
from learning_logs.models import Topic

# 让Django通过管理网站管理模型
admin.site.register(Topic)
```
-------------------------
## 5. 完善应用程序
###	5.1 定义模型Entry
为用户添加的条目定义模型，多条目可关联到同一主题。
###	5.2 迁移模型Entry
	(11_env)learning_log> python manage.py makemigrations learning_logs
    (11_env)learning_log> python manage.py migrate
###	5.3 向管理网站注册模型Entry
修改 admin.py，使用

    admin.site.register(Entry)
-----------------------------------------
## 6. Django shell 
使用交互式终端测试项目和排除其故障。
###	6.1 启动一个Python解释器
	(11_env)learning_log> python manage.py shell
###	6.2  导入模块learning_logs.models中的模型Topic
	from learning_logs.models import Topic
###	6.3 使用方法Topic.objects.all()获取模型Topic的所有实例
	Topic.objects.all()
###	6.4 遍历返回的查询集（queryset）
```py
topics = Topic.objects.all()
for topic in topics:
    print(topic.id, topic)
```
###	6.5 知道对象的ID后，就可获取该对象并查看其属性
```py
t = Topic.objects.get(id=1)
t.text

t.date_added

# 通过外键获取数据，使用相关模型的小写名称+下划线+set
t.entry_set.all() 
```
###	6.6 小结

在简单的shell环境中排除故障币网页文件中容易得多，需要熟悉Django语法，ctrl+z 后回车退出。

----------------------------------------
## 7. 创建网页：学习笔记主页
###	7.1 映射URL
URL模式让Django知道如何将浏览器请求与网站URL匹配，以确定返回哪个网页，每个URL被映射到特定的视图。

1. 项目主文件夹learning_log中的urls.py：
```py
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls)),

# 我们需要包含learning_logs的URL
    path('', include('learning_logs.urls', namespace='learning_logs')),
]
```
2. 在应用文件夹learning_logs中创建另一个urls.py文件：
```py
'''定义learning_logs的URL模式'''

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
]
```
###	7.2 编写视图
视图函数获取并处理网页所需的数据，通常调用一个模板生成浏览器能理解的网页。
1. 应用learning_logs中的views.py
```py
from django.shortcuts import render

def index(request):
    '''学习笔记的主页'''
    return render(request, 'learning_logs/index.html')
```

URL请求与定义的模式匹配时，Django将在文件views.py中查找函数index()，再将请求对象传递给这个视图函数。这里向函数render()提供了两个实参：原始请求对象以及一个可用于创建网页的模板。

###	7.3 编写模板
模板定义网页的结构，网页被请求时，Django将填入相关的数据。

在文件夹learning_logs中新建一个文件夹templates，在templates中再新建一个文件夹learning_logs。在最里面的文件夹learning_logs中，新建一个文件index.html，内容如下：
```html
<p>Learning Log</p>
<p>Learning Log helps you keep track of your learning, for any topic you're learning about.</p>
```
-------------------------------------
## 8. 创建其他网页
###	8.1 父模板
在index.html所在目录创建base.html，顶端标题通用：设置为到主页的链接
```html
<p>
  <a href="{% url 'learning_logs:index' %}>Learning Log</a>
</p>

{% block content %}{% endblock content %}
```
###	8.2 重新编写index.html
继承base.html：
```html
{% extends "learning_logs/base.html" %}

{% block content %}
  <p>Learning Log helps you keep track of your learning, for any topic you're learning about.</p>
{% endblock content %}
```
###	8.3 显示所有主题的页面
####		8.3.1 补充learning_logs/urls.py中的url
```py
'''定义learning_logs的URL模式'''

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),

    # 显示所有的主题
    path('topics/', views.topics, name='topics'),
]
```
####		8.3.2 补充views.py中的topics函数
```py
from django.shortcuts import render
from .models import Topic

def index(request):
    '''学习笔记的主页'''
    return render(request, 'learning_logs/index.html')

def topics(request):
    '''显示所有的主题'''
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
```
####		8.3.3 创建topics.html

在index.html所在的目录中创建topics.html：
```html
{% extends 'learning_logs/base.html' %}

{% block content %}
  
  <p>Topics</p>

  <ul>
    {% for topic in topics %}
      <li>{{ topic }}</li>
    {% empty %}
      <li>No topics have been added yet.</li>
    {% endfor %}
  </ul>

{% endblock content %}
```
####		8.3.4 补充父模板base.html中的topics链接
```html
<p>
  <a href="{% url 'learning_logs:index' %}">Learning Log</a> - <a href="{% url 'learning_logs:topics' %}">Topics</a>
</p>

{% block content %}{% endblock content %}
```
###	8.4 显示特定主题中条目的页面
####		8.4.1 补充learning_logs/urls.py中的url
```py
'''定义learning_logs的URL模式'''

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),

    # 显示所有的主题
    path('topics/', views.topics, name='topics'),

    # 显示特定主题的所有条目
    re_path('topics/(?P<topic_id>\d+)/', views.topic, name='topic'),
]
```
####		8.4.2 补充views.py中的topic函数
```py
from django.shortcuts import render
from .models import Topic

def index(request):
    '''学习笔记的主页'''
    return render(request, 'learning_logs/index.html')

def topics(request):
    '''显示所有的主题'''
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    '''显示特定主题的所有条目'''
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
```
####		8.4.3 创建topic.html
```html
{% extends 'learning_logs/base.html' %}

{% block content %}

  <p>Topic: {{ topic }}</p>

  <p>Entries:</p>
  <ul>
  {% for entry in entries %}
    <li>
      <p>{{ entry.date_added|date:'M d, Y H:i' }}</p>
      <p>{{ entry.text|linebreaks }}</p>
    </li>
  {% empty %}
    <li>
      There are no entries for this topic yet.
    </li>
  {% endfor %}
  </ul>

{% endblock content %}
```
####		8.4.4 补充设置topics.html中的主题链接
```html
{% extends 'learning_logs/base.html' %}

{% block content %}
  
  <p>Topics</p>

  <ul>
    {% for topic in topics %}
      <li>
        <a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>
      </li>
    {% empty %}
      <li>No topics have been added yet.</li>
    {% endfor %}
  </ul>

{% endblock content %}
```
------------------------------------------
## 9. 用户账户
###	9.1 让用户能够输入数据
####		9.1.1 用于添加新主题的表单
Django中创建表单最简单方式是使用ModelForm
步骤：在 models.py所在目录创建 forms.py
```py
from django import forms
from .models import Topic

class TopicForm(forms.ModelForm):
    class Meta:
		model =Topic 
		fields = [ 'text' ]
		labels = { 'text' : ''}
```
####		9.1.2 补充URL模式new_topic
当用户要添加新主题时，将切换到http://localhost:8000/new_topic/
下面是网页new_topic的URL模式，我们将其添加到learning_logs/urls.py中：
```py
--snip--
urlpatterns = [
		--snip--
		# 用于添加新主题的网页
		path('new_topic/', views.new_topic, name='new_topic'),
	]
```
#这个URL模式将请求交给视图函数new_topic()，接下来我们编写这个函数
####		9.1.3 补充视图函数new_topic()
函数new_topic()处理两种情形：刚进入new_topic网页（显示一个空表单）；对提交的表单数据进行处理，并将用户重定向到网页topics。

views.py如下：
```py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Topic
from .forms import TopicForm

def index(request):
    '''学习笔记的主页'''
    return render(request, 'learning_logs/index.html')

def topics(request):
    '''显示所有的主题'''
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    '''显示特定主题的所有条目'''
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
	'''添加新主题'''
	if request.method != 'POST':
		# 未提交数据，创建一个新表单
		form = TopicForm()
	else:
		# POST提交的数据，对数据进行处理
		form = TopicForm(request.POST)		
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))

	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)
```
####		9.1.4 模板new_topic
创建新模板new_topic.html，用于显示我们刚创建的表单。
```html
{% extends "learning_logs/base.html" %}

{% block content %}
  <p>Add a new topic:</p>

  <form action="{% url 'learning_logs:new_topic' %}" method='post'>
    {% csrf_token %}
    {{ form.as_p }}
    <button name="submit">add topic</button>
  </form> 
{% endblock content %}
```
####		9.1.5 topics.html补充链接到页面new_topic
topics.html：
```html
{% extends 'learning_logs/base.html' %}

{% block content %}
  
  <p>Topics</p>

  <ul>
    {% for topic in topics %}
      <li>
        <a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>
      </li>
    {% empty %}
      <li>No topics have been added yet.</li>
    {% endfor %}
  </ul>

  <a href="{% url 'learning_logs:new_topic' %}">Add a new topic:</a>

{% endblock content %}
```
###	9.2 添加新条目
####		9.2.1 补充用于添加新条目的表单
forms.py：
```py
from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
		model =Topic 
		fields = [ 'text' ]
		labels = { 'text' : ''}

class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ['text']
		labels = {'text' : ''}
		widgets = {'text': forms.Textarea(attrs={'cols': 80})}
```
####		9.2.2 补充URL模式new_entry
用于添加新条目的页面的URL模式中，需要包含实参topic_id，因为条目必须与特定的主题相关联。在learning_logs/urls.py中：
```py
--snip--
urlpatterns = [
		--snip--
		# 用于添加新条目的网页
		re_path('new_entry/?P<topic_id>\d+)/', views.new_entry, name='new_entry'),
	]
```
这个URL模式http://localhost:8000/new_entry/id//的URL匹配，其中id是一个与主题ID匹配的数字。代码
> (?P<topic_id>\d+)

捕获一个数字值并存储在topic_id中，请求的URL与这个模式匹配时，Django将请求和主题ID发送给函数new_entry()。
####		9.2.3 补充视图函数new_entry()
views.py：
```py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Topic
from .forms import TopicForm, EntryForm

--snip--
def new_entry(request, topic_id):
	'''在特定的主题中添加新条目'''
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		# 未提交数据，创建一个空表单
		form = EntryForm()
	else:
		# POST提交的数据，对数据进行处理
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))

	context = {'topic':topic, 'form':form}
	return render(request, 'learning_logs/new_entry.html', context)
```
####		9.2.4 模板new_entry
创建新模板new_entry.html，用于显示我们刚创建的表单。

new_entry.html：
```html
{% extends "learning_logs/base.html" %}

{% block content %}

  <p><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a></p>

  <p>Add a new entry:</p>
  <form action="{% url 'learning_logs:new_entry' topic.id %}" method='post'>
    {% csrf_token %}
    {{ form.as_p }}
    <button name="submit">add entry</button>
  </form> 

{% endblock content %}
```
####		9.2.5 topic.html补充链接到页面new_entry
topic.html：
```html
{% extends 'learning_logs/base.html' %}

{% block content %}

  <p>Topic: {{ topic }}</p>

  <p>Entries:</p>
  <p>
    <a href="{% url 'learning_logs:new_entry' topic.id %}">add new entry</a>
  </p>
  <ul>
  {% for entry in entries %}
    <li>
      <p>{{ entry.date_added|date:'M d, Y H:i' }}</p>
      <p>{{ entry.text|linebreaks }}</p>
    </li>
  {% empty %}
    <li>
      There are no entries for this topic yet.
    </li>
  {% endfor %}
  </ul>

{% endblock content %}
```
###	9.3 编辑条目
####		9.3.1 URL模式edit_entry
这个页面的URL需要传递要编辑的条目的ID。修改后的learning_logs/urls.py如下：
```py
--snip--
urlpatterns = [
	--snip--
	# 用于编辑条目的页面
	re_path('edit_entry/(?P<entry_id>\d+)/', views.edit_entry, name='edit_entry'),
]	
```
####		9.3.2 补充视图函数edit_entry()
views.py：
```py
--snip--
from .models import Topic, Entry

def edit_entry(request, entry_id):
	'''编辑既有条目'''
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic

	if request.method != 'POST':
		# 初次请求，使用当前条目填充表单
		form = EntryForm(instance=entry)
	else:
		# POST提交的数据，对数据进行处理
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)
```
####		9.3.3 模板edit_entry.html
```html
{% extends 'learning_logs/base.html' %}

{% block content %}
  <p><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a></p>

  <p>Edit entry:</p>

  <form action="{% url 'learning_logs:edit_entry' entry.id %}" method='POST'>
    {% csrf_token %}
    {{ form.as_p }}
    <button name="submit">save changes</button>
  </form>

{% endblock content %}
```
####		9.3.4 topic.html链接到页面edit_entry.html
topic.html：
```html
{% extends 'learning_logs/base.html' %}

{% block content %}

  <p>Topic: {{ topic }}</p>

  <p>Entries:</p>
  <p>
    <a href="{% url 'learning_logs:new_entry' topic.id %}">add new entry</a>
  </p>
  <ul>
  {% for entry in entries %}
    <li>
      <p>{{ entry.date_added|date:'M d, Y H:i' }}</p>
      <p>{{ entry.text|linebreaks }}</p>
      <p>
        <a href="{% url 'learning_logs:edit_entry' entry.id %}">edit entry</a>
      </p>
    </li>
  {% empty %}
    <li>
      There are no entries for this topic yet.
    </li>
  {% endfor %}
  </ul>

{% endblock content %}
```
--------------------------------
## 10. 创建用户账户
###	10.1 应用程序users

####		10.1.1创建应用程序
    (11_env)learning_log> python manage.py startapp users
####		10.1.2 将应用程序users添加到settings.py中
打开learning_log>settings.py：
```py
--snip--
INSTALLED_APPS = [
    --snip--
    
    # 我的应用程序
    ‘learning_logs',
    'users',
]
--snip--
```
####		10.1.3 包含应用程序users的URL
在项目根目录中的urls.py中修改：
```py
urlpatterns = [
--snip--
    path('users/', include('users.urls', namespace='users')),
]
```
###	10.2 登录页面
####		10.2.1 在learning_log/users/中，新建 urls.py
我们将使用Django提供的默认登录视图，登录页面的URL模式与URL http://localhost:8000/users/login/ 匹配：

urls.py：
```py
'''为应用程序users定义URL模式'''

from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'users/login.html'), name='login'),
]
app_name = 'users'
```
####		10.2.2 模板login.html
用户请求登录页面时，Django将使用默认视图，但我们依然需要为这个页面提供模板。为此在目录learning_log/users/中，创建templates/users的目录。其中创建login.html:
```html
{% extends 'learning_logs/base.html' %}

{% block content %}
  {% if form.errors %}
  <p>Your username and password didn't match. Please try again</p>
  {% endif %}

  <form method="post" action="{% url 'users:login' %}">
  {% csrf_token %}
  {{ form.as_p }}

  <button name="submit">login</button>
  <input type="hidden" name="next" value="{% url learning_logs/index %}" />
  </form>

{% endblock content %}
```
####		10.2.3 在base.html添加链接到登录页面
在base.html中添加到登录页面的链接，让所有页面都包含它。用户已登录时，我们不想显示这个链接，因此将它嵌套在一个{% if %}标签中。

base.html：
```html
<p>
  <a href="{% url 'learning_logs:index' %}">Learning Log</a> - 
  <a href="{% url 'learning_logs:topics %}">Topics</a> -
  {% if uesr.is_authenticated %}
    Hello, {{ user.username }}.
  {% else %}
    <a href="{% url 'users:login' %}">log in</a>
  {% endif %}
</p>

{% block content %}{% endblock content %}
```
###	10.3 注销
####		10.3.1 注销URL
下面的代码为注销定义了URL模式，该模式与URL http://localhost:8000/users/logout 匹配。

修改后的users/urls.py如下：
```py
--snip--
urlpatterns = [
    # 登录页面
    --snip--
	# 注销
    path('logout/', views.logout_view, name='logout'),
]
```
####		10.3.2 视图函数logout_view()
users/views.py：
```py
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import logout

def logout_view(request):
	'''注销用户'''
	logout(request)
	return HttpResponseRedirect(reverse('learning_logs:index'))
```
####		10.3.3 在base.html添加链接到注销页面
base.html：
```html
<p>
  <a href="{% url 'learning_logs:index' %}">Learning Log</a> - 
  <a href="{% url 'learning_logs:topics %}">Topics</a> -
  {% if uesr.is_authenticated %}
    Hello, {{ user.username }}.
    <a href="{% url 'users:logout' %}">log out</a>
  {% else %}
    <a href="{% url 'users:login' %}">log in</a>
  {% endif %}
</p>

{% block content %}{% endblock content %}
```
###	10.4 注册页面
####		10.4.1 注册页面的URL模式
users/urls.py：
```py
--snip--
urlpatterns = [
    # 登录页面
    --snip--
	# 注销
    path('logout/', views.logout_view, name='logout'),
    # 注册页面
	path('register', views.register, name='register'),
]
```
####		10.4.2 视图函数register()
users/views.py：
```py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import logout

def logout_view(request):
	'''注销用户'''
	logout(request)
	return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    '''注册新用户'''
	if request.method != 'POST':
		# 显示空的注册表单
		form = UserCreationForm()
	else:
		# 处理填写好的表单
		form = UserCreationForm(data=request.POST)

		if form.is_valid():
			new_user = form.save()
			# 让用户自动登录，再重定向到主页
			authenticated_user = authenticate(username=new_uesr.username, password=request.POST['password1'])
			login(request, authenticated_user)
			return HttpResponseRedirect(reverse('learning_logs:index'))

		context = {'form':form}
		return render(request, 'users/register.html', context)
```
####		10.4.3 模板register.html
```html
{% extends 'learning_logs/base.html' %}

{% block content %}
	
  <form action="{% url 'users:register' %}" method="POST">
	{% csrf_token %}
	{{ form.as_p }}
	
	<button name="submit">register</button>
	<input type="hidden" name="next" value="{% url 'learning_logs:index' %}"/>
	</form>
	
{% endblock content %}
```
####		10.4.4 在base.html中添加链接到注册页面
base.html：
```html
<p>
  <a href="{% url 'learning_logs:index' %}">Learning Log</a> - 
  <a href="{% url 'learning_logs:topics %}">Topics</a> -
  {% if uesr.is_authenticated %}
    Hello, {{ user.username }}.
    <a href="{% url 'users:logout' %}">log out</a>
  {% else %}
	<a href="{% url 'users:register' %}">register</a> - 
    <a href="{% url 'users:login' %}">log in</a>
  {% endif %}
</p>

{% block content %}{% endblock content %}
```
###	10.5 让用户拥有自己的数据

####		10.5.1 使用@login_required限制访问

#####			10.5.1.1 限制对topics页面的访问

示例：
限制对topics页面的访问，每个主题都归特定用户所有，因此应只允许已登录的用户请求topics页面。为此在learning_logs/view.py中添加如下代码：
```py
--snip--
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
--snip--

@login_required
def topic(request):
	'''显示所有主题'''
	--snip--
```

要实现未登录用户的重定向至登录页面，需要修改 settings.py：
```py
'''
项目learning_log的Django设置
--snip--

# 我的设置
LOGIN_URL = '/users/login/'
```
#####			10.5.1.2 全面限制

先全面限制，再确定哪些页面不需要限制，会更安全。

在学习笔记项目中，我们将不限制对主页、注册页面和注销页面的访问，并限制对其它页面的访问。

对learning_logs/views.py中除index()外的每个视图都应用装饰器@login_required
####		10.5.2 将数据关联到用户
只需将最高层的数据关联到用户，这样更低层的数据将自动关联到用户。在学习笔记项目中，应用程序的最高层数据是主题，所有条目都与特定主题相关联。

在模型Topic中添加一个关联到用户的外键，之后必须对数据库进行迁移，最后对部分视图进行修改，使其只显示与当前登陆的用户相关联的数据。

#####			10.5.2.1 修改模型Topic
models.py：
```py
from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
	'''用户要学习的主题'''
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		'''返回模型的字符串表示'''
		return self.text

class Entry(models.Model):
	--snip--
```
#####			10.5.2.2 确定当前有哪些用户
迁移数据库时，Django将对数据库进行修改，使其能够存储主题和用户之间的关联。最简单的办法是将所有主题都关联到同一个用户，如超级用户。为此需要知道该用户ID。
为此，启动一个shell会话：
```sh
(11_env)learning_logs>python manage.py shell
>>>from django.contrib.auth.models import User
>>>for user in User.objects.all():
...			print(user.username, user.id)
```

#####			10.5.2.3 迁移数据库
1：
```sh
(11_env)learning_logs>python manage.py makemigrations learning_logs
1
1
```
2：
```sh
(11_env)learning_logs>python manage.py migrate
```
可在shell会话中验证迁移是否符合预期
```sh
(11_env)learning_logs>python manage.py shell
>>>from learning_logs.models import Topic:
>>>for topic in Topic.objects.all():
...        print(topic, topic.owner)
```

你也可以重置数据库，执行命令python manage.py flush。但这样做必须重新创建超级用户，且原来的数据都将丢失。


####		10.5.3 只允许用户访问自己的主题

在views.py中，对函数topics()作如下修改：
```py
--snip--
@login_required
def topics(request):
	'''显示所有的主题'''
	topics = Topic.objects.filters(owner=request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)
--snip--
```
用户登录后，request对象将有一个user属性，这个属性存储了有关该用户的信息。代码
```
Topic.objects.filter(owner=request.user).order_by('date_added')
```
让Django只从数据库获取owner属性为当前用户的Topic对象。
####		10.5.4 保护用户的主题
views.py：
```py
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
--snip--

@login_required
def topic(request, topic_id):
	'''现实单个主题及其所有的条目'''
	topic = Topic.objects.get(id=topic_id)
	# 确认请求的主题属于当前用户
	if topic.owner != request.user:
		raise Http404
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)
--snip--
```
####		10.5.5 保护页面edit_entry
views.py
```py
--snip--
@login_required
def edit_entry(request, entry_id):
	'''编辑既有条目'''
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if topic.owner != request.user:
		raise Http404
	
	if request.method != 'POST':
		'''初次请求，使用当前条目的内容填充表单'''
		--snip--
```
####		10.5.6 将新主题关联到当前用户
当前，用户添加新主题的页面并没有将新主题关联到特定用户，如果你尝试添加新主题，将看到错误消息IntergrityError，指出learning_logs_topic.user_id不能为NULL。Django的意思是创建新主题时你必须指定其owner字段的值。

由于我们可以通过request对象获悉当前用户，因此做如下修复：

views.py：
```py
--snip--
@login_required
def new_topic(request):
	'''添加新主题'''
	if request.method != 'POST':
		# 没有提交的数据，创建一个空表单
		form = TopicForm()
	else:
		# POST提交的数据，对数据进行处理
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect('learning_logs:topics'))

	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)
--snip--
```
--------------------------
## 11 设置应用程序的样式并对其进行部署
###	11.1 设置项目「学习笔记」的样式
####		11.1.1 应用程序django-bootstrap3
为安装django-bootstrap3，在活动的虚拟环境中执行如下命令：
    
    (11_env)learning_log> pip install django-bootstrap3

接下来，在settings.py的INSTALLED_APPS中添加如下代码，在项目中包含应用程序django-bootstrap3：

settings.py：
```py
--snip--
INSTALLED_APPS = [
		--snip--
		'django.contrib.staticfiles',
		
		# 第三方应用程序
		'bootstrap3',

		# 我的应用程序
		’learning_logs',
		'users',
]
--snip--
```

我们需要让django-bootstrap3包含jQuery，这是一个JavaScript库，让你能够使用bootstrap模板提供的一些交互式元素。请在settings.py的末尾添加如下代码：

settings.py：
```py
--snip--
# 我的设置
LOGIN_URL = '/users/login/'

# django-bootstrap3的设置
BOOTSTRAP3 = {
		'include_jquery': True,
}
```
####		11.1.2 使用Bootstrap来设置项目「学习笔记」的样式
Bootstrap基本上就是一个大型的样式设置工具集，它还提供了大量的模板，要查看可访问http://getbootstrap.com/，单击Getting Started，至Examples部分，找到Navbars，我们将使用模板Static top navbar，它提供了简单的顶部导航条、页面标题和用于放置页面内容的容器。

####		11.1.3 修改base.html
#####			11.1.3.1 定义HTML头部
在文件中定义HTML头部，使得显示「学习笔记」的每个页面时，浏览器标题栏都显示这个网站的名称。我们还将添加一些在模板中使用Bootstrap所需的信息。

删除base.html的全部代码，并输入以下代码：

base.html：
```html
{% load bootstrap3 %}

<!DOCTYPE html>
<html lang="en">
  <head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">

	<title>Learning Log</title>

	{% bootstrap_css %}
	{% bootstrap_javascript %}

  </head>
```
#####			11.1.3.2 定义导航栏

```html
--snip--
  </head>

  <body>
  
    <!--Static navbar-->
    <nav class="navbar navbar-default navbar-static-top">
      <div class="container">

          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            </button>
            <a class="navbar-brand" href="{% url 'learning_logs:index' %}">Learning Log</a>
          </div>

          <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
              <li><a href="{% url 'learning_logs:topics' %}">Topics</a></li>
            </ul>

            <ul class="nav navbar-nav navbar-right">
              {% if user.is_authenticated %}
                <li><a>Hello, {{ user.username }}.</a></li>
                <li><a href="{% url 'users:logout' %}">log out</a></li>
              {% else %}
                <li><a href="{% url 'users:register' %}">register</a></li>
                <li><a href="{% url 'users:login' %}">log in</a></li>
              {% endif %}
            </ul>
          </div><!--/.nav-collapse -->

      </div>
    </nav>
```
#####			11.1.3.3 定义页面的主要部分
```html
--snip--
    </nav>

    <div class="container">

      <div class="page-header">  
        {% block header %}{% endblock header %}
      </div>
      <div>
        {% block content %}{% endblock content %}
      </div>
    </div><!-- /container -->

  </body>
</html>
```
####		11.1.4 使用jumbotron设置主页的样式
下面来使用新定义的header块及另一个名为jumbotron「超大屏幕」的Bootstrap元素修改主页。它通常用于在主页中呈现项目的简要描述。

index.html：
```html
{% extends "learning_logs/base.html" %}

{% block header %}
  <div class='jumbotron'>
    <h1>Track your learning.</h1>
  </div>
{% endblock header %}

{% block content %}
  <h2>
	<a href="{% url 'users:register' %}">Register an account</a> to make your own Learning Log, and list the topics you're learning about.
  </h2>
  <h2>
	Whenever you learn something new about a topic, make an entry summarizing what you've learned.
  </h2>
{% endblock content %}
```
####		11.1.5 设置登录页面的样式
login.html：
```html
{% extends 'learning_logs:base.html' %}
{% load bootstrap3 %}

{% block header %}
  <h2>Log in to your account.</h2>
{% endblock header %}

{% block content %}
  
  <form method="POST" action="{% url 'users:login' %}" class="form">
	{% csrf_token %}
	{% bootstrap_form form %}

	{% buttons %}
	  <button name="submit" class="btn btn-primary">log in</button>
	{% endbuttons %}

	<input type="hidden" name="next" value="{% url 'learning_logs:index' %}" />
  </form>

{% endblock content %}
```
####		11.1.6 设置new_topic页面的样式
new_topic.html：
```html
{% extends 'learning_logs/base.html' %}
{% load bootstrap3 %}

{% block header %}
  <h2>Add a new topic:<h2>
{% endblock header %}

{% block content %}
  
  <form method="POST" action="{% url 'learning_logs:new_topic' %}" class="form">

	{% csrf_token %}
	{% bootstrap_form form %}

	{% buttons %}
	  <button name="submit" class="btn btn-primary">add topic</button>
	{% endbuttons %}
  
  </form>

{% endblock content %}
```
####		11.1.7设置topics页面的样式
topics.html：
```html
{% extends "learning_logs/base.html" %}

{% block header %}
  <h1>Topics</h1>
{% endblock header %}

{% block content %}

  <ul>
	{% for topic in topics %}
	  <li>
	    <h3>	
		  <a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>
		</h3>
	  </li>
	{% empty %}
	  <li>No topics have been added yet.</li>
	{% endfor %}
  </ul>

  <h3><a href="{% url 'learning_logs:new_topic' %}">Add new topic</h3>

{% endblock content %}
```
####		11.1.8 设置topic页面的样式
topic页面包含的内容比其他大部分页面都多，因此需要做的样式设置工作要多些。我们将使用Bootstrap面板（panel）来突出每个条目。面板是一个带预定义样式div，非常适合用于显示主题的条目：

topic.html：
```html
{% extends 'learning_logs/base.html' %}

{% block header %}
  <h2>{{ topic }}</h2>
{% endblock header %}

{% block content %}
  <p>
    <a href="{% url 'learning_logs:new_entry' topic.id %}">add new entry</a>
  </p>
  
  {% for entry in entries %}
    <div class="panel panel-default">
      <div class="panel-heading">
        <h3>
          {{ entry.date_added|date:'M d, Y H:i' }}
          <small>
            <a href="{% url 'learning_logs:edit_entry' entry.id %}">edit entry</a>
          </small>
        </h3>
      </div>
      <div class="panel-body">
        {{ entry.text|linebreaks }}
      </div>
    </div><!-- panel -->
  {% empty %}
    <li>
      There are no entries for this topic yet.
    </li>
  {% endfor %}

{% endblock content %}
```
####		11.1.9 设置new_entry页面的样式
new_entry.html：
```html
{% extends "learning_logs/base.html" %}
{% load bootstrap3 %}

{% block header %}
  <h2>Add a new entry:</h2>
{% endblock header %}

{% block content %}
  <h3>
    <a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>
  </h3>

  <form action="{% url 'learning_logs:new_entry' topic.id %}" method="POST" class="form">
    {% csrf_token %}
    {% bootstrap_form form %}

    {% buttons %}
      <button name="submit" class="btn btn-primary">add entry</button>
    {% endbuttons %}
  </form>

{% endblock content %}
```
####		11.1.10 设置edit_entry页面的样式
edit_entry.html：
```html
{% extends "learning_logs/base.html" %}
{% load bootstrap3 %}

{% block header %}
  <h2>Edit entry:</h2>
{% endblock header %}

{% block content %}

  <h3><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a></h3>

  <form action="{% url 'learning_logs:edit_entry' entry.id %}" method="POST" class="form">
    {% csrf_token %}
    {% bootstrap_form form %}

    {% buttons %}
      <button name="submit" class="btn btn-primary">save changes</button>
    {% endbuttons %}
  </form>
  
{% endblock content %}
```
####		11.1.11 设置注册页面的样式
register.html：
```html
{% extends 'learning_logs/base.html' %}
{% load bootstrap3 %}

{% block header %}
  <h2>Register an account</h2>
{% endblock header %}

{% block content %}
  
  <form method="POST" action="{% url 'users:register' %}" class="form">
    {% csrf_token %}
    {% bootstrap_form form %}

    {% buttons %}
      <button name="submit" class="btn btn-primary">register</button>
      <input type="hidden" name="next" value="{% url 'learning_logs:index' %}"/>
    {% endbuttons %}
  </form>
  
{% endblock content %}
```
###	11.2 部署「学习笔记」
####		11.2.1 建立Heroku账户
####		11.2.2 部署Heroku时报错的解决方法
1. if代码做如下处理
cwd = os.getcwd()
if cwd == '/app' or cwd[:4] == '/tmp':

2. os.path.join(BASE_DIR, 'static') 语句需顶格

3. 部署前执行命令：heroku config:set DISABLE_COLLECTSTATIC=0
清空服务器的占位静态文件

4. 执行部署命令

源码
```py
# Heroku setting

cwd = os.getcwd()
if cwd == '/app' or cwd[:4] == '/tmp':

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost')
}
 # make request.is_secure() admit x-forwarded_Photo header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PHOTO', 'http')
 
 # support all host header
ALLOWED_HOSTS = ['*']
 
 # static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
os.path.join(BASE_DIR, 'static'),
)
```
####		11.2.3 项目「学习笔记」网址 https://evilgenius.herokuapp.com/
----------------------------------------------------
## 12 个人更新
###	12.1 未登录用户权限提升
####		12.1.1 对models.py中的Topic模型增加属性public
```py
--snip--

public=models.BooleanField(default=False)

--snip--
```
####		12.1.2 数据库迁移
```sh
(11_env)learning_log> python manage.py makemigrations learning_logs
(11_env)learning_log> python manage.py migrate
```
####		12.1.3 维护views.py
1. 取消topics函数的@login_required限制，并更新topics显示规则如下：
```py
--snip--
def topics(request):
	'''显示所有的主题'''
	topics = Topic.objects.filter(public=True).order_by('date_added')
	context = {'topics':topics}
--snip-
```

2. 取消topic函数的@login_required限制，并更新topic显示规则如下：
```py
--snip--
def topic(request, topic_id):
	'''显示公开的单个主题及其所有的条目'''
	topic = get_object_or_404(Topic, id=topic_id)
	# 确认请求的主题属性为public=True
	check_topic_public(topic, request)

	entries = topic.entry_set.order_by('-date_added')
--snip--
```	
####		12.1.4 topics页面增加topic.owner显示

topics.html：
```py
--snip--
{% block content %}

  <ul>
    {% for topic in topics %}
      <li>
        <h3>
          <a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a> <small>- {{ topic.owner }}</small>
        </h3>
--snip--
```
####		12.1.5 topic页面区分当前用户开关edit与add选项显示

topic.html：
```py
--snip--
{% block content %}
  <p>
    {% if topic.owner == user %}  
      <a href="{% url 'learning_logs:new_entry' topic.id %}">add new entry</a>
    {% endif %}
  </p>
  
  {% for entry in entries %}
    <div class="panel panel-default">
      <div class="panel-heading">
        <h3>
          {{ entry.date_added|date:'M d, Y H:i' }}
          {% if topic.owner == user %}  
            <small>
              <a href="{% url 'learning_logs:edit_entry' entry.id %}">edit entry</a>
            </small>
          {% endif %}
--snip--
```
###	12.2 私有topic维护

####		12.2.1 my_topics的URL模式

urls.py：
```py
--snip--
urlpatterns = [
--snip--
	# 用于显示个人所有的主题
    path('my_topics/', views.my_topics, name='my_topics'),
--snip
```
####		12.2.2 视图函数my_topics()

views.py：
```py
--snip--
@login_required
def my_topics(request):
    '''显示用户个人所有的主题'''

    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/my_topics.html', context)
--snip
```

注意这里，仅登陆限制+filter的参数不同，因此同样传递给topics.html用于显示my topics。


###	12.3 推送至Heroku
####		12.3.1 git add .
####		12.3.2 git commit -am "Unlogged users can view public now!"
####		12.3.3 git push heroku master

### 12.4 允许用户删除自己的主题和条目
1. 在模型Entry和模型Topic中分别增加BooleanField属性。

models.py:
```py
entry_hide = models.BooleanField(default=False)
```

```py
topic_hide = models.BooleanField(default=False)
```
2. 数据库迁移。
3. 设置URL模式

urls.py:
```py
# 用于删除自有条目的页面
re_path('delete_entry/(?P<entry_id>\d+)/', views.delete_entry, name='delete_entry'),

# 用于删除自有主题的页面
re_path('delete_topic/(?P<topic_id>\d+)/', views.delete_topic, name='delete_topic'),
```
4. 维护views.py
```py
--snip--
def topics(request):
    '''显示所有的主题'''

    topics = Topic.objects.filter(public=True, topic_hide=False).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    '''显示单个主题及其所有的条目'''
    topic = get_object_or_404(Topic, id=topic_id)
    # 确认请求的主题属于当前用户
    # check_topic_owner(topic, request)
    # 确认请求的主题属性为公开
    check_topic_public(topic, request)
    entries = topic.entry_set.filter(entry_hide=False).order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def delete_entry(request, entry_id):
    '''删除选定条目'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)
    entry.entry_hide = True
    entry.save()

    return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))

@login_required
def delete_topic(request, topic_id):
    '''删除选定主题'''
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)
    topic.topic_hide = True
    topic.save()
    
    return HttpResponseRedirect(reverse('learning_logs:my_topics'))
```
5. 增加页面my_topics.html优化用户跳转体验。
```py
{% if topic.owner == user %}  
  <small><a href="{% url 'learning_logs:delete_topic' topic.id %}" class="ex1" onclick="return confirm('永久删除此主题，请确认！');"> delete</a></small>
```
6. 在页面topic.html内增加删除选项
```py
{% if topic.owner == user %}  
  <small>
    &nbsp<a href="{% url 'learning_logs:edit_entry' entry.id %}">edit</a>&nbsp&nbsp
    <a href="{% url 'learning_logs:delete_entry' entry.id %}" class="ex1" onclick="return confirm('永久删除此条目，请确认！');"> delete</a>
  </small>
{% endif %}
```
### 12.5 支持markdown
####12.5.1 安装django-mdeditor
```sh
pip install django-mdeditor
```
在 settings 配置文件 INSTALLED_APPS 中添加 mdeditor:
```py
INSTALLED_APPS = [
    ...
    'mdeditor',
    ]
```
详细内容见：
https://segmentfault.com/a/1190000013671248
https://www.imooc.com/article/39656
感谢这两篇文章的作者。分别解决了Entry的text属性的markdown域，和html的markdown渲染，注意第二篇有符号错误，工具是可行的。
项目已更新。现在可以支持全局markdown格式了！

------------------------------------------
## 13 界面改版，增加「站点精选」导航，优化显示界面。
### 13.1 用在[ Bootstrap 3 教程](http://www.runoob.com/bootstrap/bootstrap-intro.html)里学到的BOOTSTRAP3 CSS 和 HTML知识对网站显示界面进行优化。
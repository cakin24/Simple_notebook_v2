# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404
        
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """ 添加新主题 """
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST 提交的数据 , 对数据进行处理
        # HttpResponseRedirect 类，用户提交主题后我们将使用这个类将用户重定向到网页 topics 。
        # 函数 reverse() 根据指定的 URL 模型确定 URL ，这意味着 Django将在页面被请求时生成 URL 。
        # 我们还导入了刚才创建的表单 TopicForm 。
        # 我们使用用户输入的数据（它们存储在 request.POST 中）创建一个 TopicForm 实例
        # 这样对象 form 将包含用户提交的信息。
        form = TopicForm(request.POST)
        # 函数 is_valid() 核实用户填写了所有必不可少的字段（表单字段默认都是必不可少的），
        # 且输入的数据与要求的字段类型一致（例如，字段 text 少于 200 个字符）。
        # 这种自动验证避免了我们去做大量的工作。
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            # 将表单中的数据写入数据库
            new_topic.save()
            # 使用 reverse() 获取页面 topics 的 URL ，并将其传递给 HttpResponseRedirect()
            # 后者将用户的浏览器重定向到页面 topics 。
            # 在页面 topics 中，用户将在主题列表中看到他刚输入的主题。
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """ 在特定的主题中添加新条目 """
    # 形参 topic_id ，用于存储从 URL 中获得的值。渲染页面以及处理表单数据时，都
    # 需要知道针对的是哪个主题，因此我们使用 topic_id 来获得正确的主题。
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # 未提交数据 , 创建一个空表单
        form = EntryForm()        
    else:
        # POST 提交的数据 , 对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 让 Django 创建一个新的条目对象，并将其存储到 new_entry 中，但不将它保存到数据库中。
            new_entry = form.save(commit=False)
            # 设置条目对象的属性 topic ，再将条目对象保存到数据库。
            new_entry.topic = topic
            new_entry.save()
            # 调用 reverse() 时，需要提供两个实参：要根据它来生成 URL 的 URL 模式的名称；
            # 列表 args ，其中包含要包含在 URL 中的所有实参。在这里，列表 args 只有一个元素 —— topic_id 。
            # 接下来，调用 HttpResponseRedirect() 将用户重定向到显示新增条目所属主题的页面，用户将在该页面的
            # 条目列表中看到新添加的条目。
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic_id]))
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

'''
页面 edit_entry 收到 GET 请求时， edit_entry() 将返回一个表单，让用户能够对条目进行编辑。
页面收到 POST 请求（条目文本经过修订）时，它将修改后的文本保存到数据库中
'''
@login_required
def edit_entry(request, entry_id):
    """ 我们获取用户要修改的条目对象，以及与该条目相关联的主题。在请求方法为 GET 时将执行的 if 代码块中，我们使用实
        参 instance=entry 创建一个 EntryForm 实例。
        这个实参让 Django 创建一个表单，并使用既有条目对象中的信息填充它。用户将看到既有的数据，并能够编辑它们。
        处理 POST 请求时，我们传递实参 instance=entry 和 data=request.POST ，让 Django 根据既有条目对象创建一个表单实例，
        并根据 request.POST 中的相关数据对其进行修改。然后，我们检查表单是否有效，如果有效，就调用 save() ，且不指定任何实参。
        接下来，我们重定向到显示条目所属主题的页面，用户将在其中看到其编辑的条目的新版本。"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST 提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic.id]))
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

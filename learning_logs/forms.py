# -*- coding: utf-8 -*-
# 导入模块 forms 以及要使用的模型 Topic,Entry
from django import forms

from .models import Topic, Entry

'''
定义了一个名为 TopicForm 的类，它继承了 forms.ModelForm
最简单的 ModelForm 版本只包含一个内嵌的 Meta 类，它告诉 Django 根据哪个模型创建表单，以及在表单中包含哪些字段。
根据模型 Topic 创建一个表单，该表单只包含字段 text
'''
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        # 让 Django 不要为字段 text 生成标签。
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        # 这里也给字段 'text' 指定了一个空标签
        labels = {'text': ''}
        # 通过设置属性 widgets ，可覆盖 Django 选择的默认小部件。
        # 通过让 Django 使用 forms.Textarea ，我们定制了字段 'text' 的输入小部件，将文本区域的宽度设置为 80 列，而不是默认的 40 列。
        # 这给用户提供了足够的空间，可以编写有意义的条目。
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

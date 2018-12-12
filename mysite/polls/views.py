

# Create your views here.


from django.http import HttpResponseRedirect
from django.shortcuts import  get_object_or_404,render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import  Choice,Question


#加载 polls/index.html 模板，并且向它传递一个上下文环境（context）。
# 这个上下文是一个字典，它将模板内的变量映射为 Python 对象。

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ 返回最近时间的五个问题 """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]



class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        过滤掉现在不应该被发布的投票。
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice  = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        #重新显示问题的投票表单
        return render(request,'polls/detail.html',{
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #成功处理之后POST数据之后,总是返回一个HttpResponseRedirect。防止因为用户点击了后退按钮而提交了两次。
    return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))



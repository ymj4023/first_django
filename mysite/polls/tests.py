from django.test import TestCase

# Create your tests here.
import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import  Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):

        """

        was_published_recently() 应该对 pub_date 字段值是将来的那些问题返回False。
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        """

        对于 pub_date 在一天以前的Question,was_published_recently() 应该返回False。

        """
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recently_question(self):
        """

        对于 pub_date 在一天之内的Question,was_published_recently() 应该返回True。
        """
        time =timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)


#封装了创建问题（questions）的流程，减少了重复代码。
def create_question(question_text,days):
    """
    创建一个以question_text 为标题,pub_date 为days天之后的问题。
    days为正表示将来,为负表示过去。
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        如果数据库里没有保存问题,应该显示一个合适的提示信息。
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        """
        值pub_date 是过去的,问题应该被显示在主页上。
        """
        create_question(question_text="Past question.",days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        值pub_date 是将来的,问题不应该被显示在主页上。
        """
        create_question(question_text="Future question.",days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.contest['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        """
        如果数据库里同时存在有过去和将来的投票,那么只应该显示过去那些。
        """
        create_question(question_text="Past question.",days=-30)
        create_question(question_text="Future question.",days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        问题索引页应该可以显示多个问题。
        """

        create_question(question_text="Past question 1.",days=-30)
        create_question(question_text="Past question 2.",days=-5)
        response =self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>','<Question: Past question 1.>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        访问将来发布问题详情页应该会收到一个404 错误。
        """
        future_question = create_question(question_text='Future question.',days=5)
        url = reverse('polls:detail',args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_past_question(self):
        """
        访问过去发布的问题详情页,页面上应该显示问题描述。
        """
        past_question = create_question(question_text='Past Question.',days=-5)
        url = reverse('polls:detail',args=(past_question.id,))
        response =self.client.get(url)
        self.assertContains(response,past_question.question_text)


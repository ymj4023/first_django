from django.test import TestCase

# Create your tests here.
import datetime

from django.utils import timezone
from django.test import TestCase

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


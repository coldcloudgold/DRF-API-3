from api.models import Poll, Question, User
from django.db.models import Q
from django.utils.timezone import now


class DefaultUserLogic:
    def check_current_user(self, request, id_user):
        if not request.user.is_staff:
            if request.user.id != id_user:
                return False


class UserAnswerLogic(DefaultUserLogic):
    def check_actually_poll(self, id_poll):
        if not Poll.objects.filter(
            Q(pk=id_poll, date_start__lte=now(), date_end__gte=now())
            | Q(pk=id_poll, date_start__lte=now(), date_end=None)
        ).exists():
            return False

    def check_actually_question(self, id_poll, id_question):
        poll = Poll.objects.get(pk=id_poll)
        if not poll.questions.all().filter(pk=id_question).exists():
            return False

    def delete_old_answers(self, id_question, id_user):
            question = Question.objects.get(pk=id_question)
            user = User.objects.get(pk=id_user)
            answers_user = question.answers.all().filter(user=user)
            if question.type_question in ("1", "2"):
                if answers_user.count() > 1:
                    answers_user.first().delete()
            elif question.type_question == "3":
                answer_admin = question.answers.all().filter(is_admin=True)
                if answers_user.count() > answer_admin.count():
                    answers_user.first().delete()

    def make_connection(self, id_user, id_poll):
        user = User.objects.get(pk=id_user)
        poll = Poll.objects.get(pk=id_poll)
        poll.users.add(user)

from django.urls import path, include
from rest_framework import routers

from .views import (
    ActuallyPollView,
    ActuallyPollQuestionAnswerView,
    #
    AllPollQuestionView,
    AdminPollQuestionAnswerView,
    RightPollQuestionAnswerView,
    #
    UserAnswerView,
    #
    UserAnswersView,
)

router = routers.DefaultRouter()

router.register(r"actually_polls", ActuallyPollView)
router.register(r"actually_polls_questions_answers", ActuallyPollQuestionAnswerView)
router.register(r"all_polls_questions", AllPollQuestionView)
router.register(r"polls_questions_answers_admin", AdminPollQuestionAnswerView)
router.register(r"polls_questions_answers_right", RightPollQuestionAnswerView)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "user_answer/<int:id_user>/<int:id_poll>/<int:id_question>/",
        UserAnswerView.as_view(),
    ),
    path("user_answers/<int:id_user>/", UserAnswersView.as_view()),
]

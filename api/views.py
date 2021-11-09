from django.utils.timezone import now
from django.db.models import Q

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated


from users.models import User
from .models import Poll
from .service.businness_views import DefaultUserLogic, UserAnswerLogic
from .service.serializers import (
    ActuallyPollSerializer,
    ActuallyPollQuestionAnswerSerializer,
    AllPollQuestionSerializer,
    AdminPollQuestionAnswerSerializer,
    RightPollQuestionAnswerSerializer,
    UserAnswerSerializer,
    UserAnswersSerializer,
)


class ActuallyPollView(viewsets.ReadOnlyModelViewSet):
    """Поулчение актуальных опросов."""

    queryset = Poll.objects.filter(
        Q(date_start__lte=now(), date_end__gte=now())
        | Q(date_start__lte=now(), date_end=None)
    )
    serializer_class = ActuallyPollSerializer


class ActuallyPollQuestionAnswerView(viewsets.ReadOnlyModelViewSet):
    """Поулчение актуальных опросов, вопросов, вариантов ответов."""

    queryset = Poll.objects.filter(
        Q(date_start__lte=now(), date_end__gte=now())
        | Q(date_start__lte=now(), date_end=None)
    )
    serializer_class = ActuallyPollQuestionAnswerSerializer
    permission_classes = (IsAuthenticated,)


class AllPollQuestionView(viewsets.ReadOnlyModelViewSet):
    """Поулчение всех опросов и вопросов."""

    queryset = Poll.objects.all()
    serializer_class = AllPollQuestionSerializer
    permission_classes = (IsAdminUser,)


class AdminPollQuestionAnswerView(viewsets.ReadOnlyModelViewSet):
    """Поулчение опросов, вопросов, вариантов ответов с пометкой."""

    queryset = Poll.objects.all()
    serializer_class = AdminPollQuestionAnswerSerializer
    permission_classes = (IsAdminUser,)


class RightPollQuestionAnswerView(viewsets.ReadOnlyModelViewSet):
    """Поулчение опросов, вопросов и только правильных ответов."""

    queryset = Poll.objects.all()
    serializer_class = RightPollQuestionAnswerSerializer
    permission_classes = (IsAdminUser,)


class UserAnswerView(UserAnswerLogic, APIView):
    """Регистрация ответов пользователя."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, id_user, id_poll, id_question):

        if self.check_current_user(request, id_user) is False:
            return Response(
                {"error": "Не верно указан идентификатор пользователя"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not Poll.objects.filter(pk=id_poll).exists():
            return Response(
                {"error": "Не найдено опроса с указанным идентификатором"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if self.check_actually_poll(id_poll) is False:
            return Response(
                {"error": "Нет доступа к опросу"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if self.check_actually_question(id_poll, id_question) is False:
            return Response(
                {
                    "error": "Не найдено вопроса с указанным идентификатором для заданного опроса"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data
        data.update({"is_admin": False, "user": id_user, "question": id_question})

        serializer = UserAnswerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.delete_old_answers(id_question, id_user)
        self.make_connection(id_user, id_poll)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class UserAnswersView(DefaultUserLogic, APIView):
    """Поулчение опросов, вопросов и ответов пользователя."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, id_user):
        if self.check_current_user(request, id_user) is False:
            return Response(
                {"error": "Не верно указан идентификатор пользователя"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        polls = Poll.objects.filter(users=id_user)
        user = User.objects.get(pk=id_user)
        serializer = UserAnswersSerializer(polls, context={"user": user}, many=True)
        data = serializer.data

        return Response(
            data if data else {"error": "Пользователь не имеет ответов"},
            status.HTTP_200_OK if data else status.HTTP_404_NOT_FOUND,
        )

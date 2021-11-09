from rest_framework import serializers

from api.models import Poll, Question, Answer


# Third party


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("pk", "text")


# actually_polls


class ActuallyPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ("pk", "name", "description")


# actually_polls_questions_answers


class ActuallyQuestionAnswerSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ("pk", "description", "type_question", "answers")

    def get_answers(self, obj):
        if obj.type_question != "1":
            _answers = Answer.objects.filter(is_admin=True, question=obj)
            return AnswerSerializer(_answers, many=True).data
        else:
            return []


class ActuallyPollQuestionAnswerSerializer(serializers.ModelSerializer):
    questions = ActuallyQuestionAnswerSerializer(many=True)

    class Meta:
        model = Poll
        fields = ("pk", "name", "description", "questions")


# all_polls_questions


class AllQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("pk", "description", "type_question")


class AllPollQuestionSerializer(serializers.ModelSerializer):
    questions = AllQuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ("pk", "name", "description", "questions")


# polls_questions_answers_admin


class AdminAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("pk", "text", "is_right")


class AdminQuestionAnswerSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ("pk", "description", "type_question", "answers")

    def get_answers(self, obj):
        _answers = Answer.objects.filter(is_admin=True, question=obj)
        return AdminAnswerSerializer(_answers, many=True).data


class AdminPollQuestionAnswerSerializer(serializers.ModelSerializer):
    questions = AdminQuestionAnswerSerializer(many=True)

    class Meta:
        model = Poll
        fields = ("pk", "name", "description", "questions")


# polls_questions_answers_right


class RightQuestionAnswerSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ("pk", "description", "type_question", "answers")

    def get_answers(self, obj):
        _answers = Answer.objects.filter(is_admin=True, is_right=True, question=obj)
        return AnswerSerializer(_answers, many=True).data


class RightPollQuestionAnswerSerializer(serializers.ModelSerializer):
    questions = RightQuestionAnswerSerializer(many=True)

    class Meta:
        model = Poll
        fields = ("pk", "name", "description", "questions")


# user_answer/<int:id_user>/<int:id_poll>/<int:id_question>/


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


# user_answers/<int:id_user>/


class UserQuestionAnswerSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ("pk", "description", "type_question", "answers")

    def get_answers(self, obj):
        _answers = Answer.objects.filter(user=self.context.get("user"), question=obj)
        return AnswerSerializer(_answers, many=True).data


class UserAnswersSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ("pk", "name", "description", "questions")

    def get_questions(self, obj):
        _questions = Question.objects.filter(poll=obj)
        return UserQuestionAnswerSerializer(
            _questions, context={"user": self.context.get("user")}, many=True
        ).data

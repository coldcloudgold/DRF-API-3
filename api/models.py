from django.db import models
from django.template.defaultfilters import truncatewords
from users.models import User

from .service.businness_models import PollLogic


class Poll(PollLogic, models.Model):
    name = models.CharField(verbose_name="Название", unique=True, max_length=250)
    date_start = models.DateTimeField(verbose_name="Дата начала", blank=True, null=True)
    date_start_no_editable = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(
        verbose_name="Дата окончания", blank=True, null=True
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    users = models.ManyToManyField(to=User, related_name="polls")

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return f"{self.name}"

    @property
    def short_name(self):
        return truncatewords(self.name, 5)


class Question(models.Model):
    CHOICES_TYPE = [
        ("1", "Ответ текстом"),
        ("2", "Ответ с выбором одного варианта"),
        ("3", "Ответ с выбором нескольких вариантов"),
    ]

    poll = models.ForeignKey(
        verbose_name="Опрос",
        to=Poll,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    description = models.TextField(verbose_name="Описание")
    type_question = models.CharField(
        verbose_name="Тип вопроса", choices=CHOICES_TYPE, max_length=2
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        unique_together = (("poll", "description", "type_question"),)

    def __str__(self):
        return f"{self.description}"

    @property
    def short_description(self):
        return truncatewords(self.description, 5)


class Answer(models.Model):
    text = models.TextField(verbose_name="Ответ")
    question = models.ForeignKey(
        verbose_name="Вопрос",
        to=Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    user = models.ForeignKey(
        verbose_name="Пользователь",
        to=User,
        on_delete=models.CASCADE,
        related_name="user_answers",
        blank=True,
        null=True,
    )
    is_admin = models.BooleanField(default=True)
    is_right = models.BooleanField(verbose_name="Правильный ответ", default=False)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        unique_together = (("text", "question", "user", "is_admin"),)

    def __str__(self):
        return f"{self.text}"

    @property
    def short_text(self):
        return truncatewords(self.text, 5)

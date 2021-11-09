from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import Poll, Question, Answer, User


class AnswerInline(NestedStackedInline):
    model = Answer
    extra = 1
    fk_name = "question"
    exclude = ("user", "is_admin")

    def get_queryset(self, request):
        qs = super(AnswerInline, self).get_queryset(request)
        return qs.filter(is_admin=True)


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    fk_name = "poll"
    inlines = (AnswerInline,)


class PollAdmin(NestedModelAdmin):
    model = Poll
    list_display = ("pk", "short_name", "date_start", "date_end")
    list_display_links = ("short_name",)
    list_filter = ("date_start", "date_end")
    exclude = ("date_start_no_editable", "users")
    inlines = (QuestionInline,)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        try:
            return super(PollAdmin, self).change_view(
                request, object_id, form_url, extra_context
            )
        except ValidationError as e:

            request.method = "GET"
            messages.error(request, e.message)
            return super(PollAdmin, self).change_view(
                request, object_id, form_url, extra_context
            )


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ("pk", "short_description")
    list_display_links = ("short_description",)


class AnswerAdmin(admin.ModelAdmin):
    model = Answer
    list_display = ("pk", "short_text")
    list_display_links = ("short_text",)


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ("pk", "username")
    list_display_links = ("username",)


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(User, UserAdmin)

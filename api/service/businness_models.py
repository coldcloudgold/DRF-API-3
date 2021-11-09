from django.core.exceptions import ValidationError


class PollLogic:
    def save(self, *args, **kwargs):
        if not self.date_start_no_editable:
            self.date_start_no_editable = self.date_start
        if self.date_start != self.date_start_no_editable:
            self.date_start = self.date_start_no_editable
            raise ValidationError(
                "Не возможно изменить дату начала опроса."
            )
        return super().save(*args, **kwargs)

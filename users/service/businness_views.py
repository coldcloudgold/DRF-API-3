from django.conf import settings

DEFAULT_ANONUMOUS_USER_PASSWORD = settings.DEFAULT_ANONUMOUS_USER_PASSWORD

def _get_data_anonymous_user(user):
    if user:
        id = user.id + 1
    else:
        id = 1
    password = DEFAULT_ANONUMOUS_USER_PASSWORD
    username = f"Anonymous-{id}"
    is_anonymous_user = True

    return {
        "id": id,
        "username": username,
        "password": password,
        "is_anonymous_user": is_anonymous_user,
    }

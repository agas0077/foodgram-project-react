# Third Party Library
from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import SubscriberSubscribee

User = get_user_model()

# Register your models here.


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
    )
    list_filter = ("email", "username")


class SubscriberSubscribeeAdmin(admin.ModelAdmin):
    SUBSCRIBER_EMAIL_NAME = "Адрес электронной почты того, кто подписывается"
    SUBSCRIBER_USERNAME_NAME = "Ник того, кто подписывается"
    SUBSCRIBEE_EMAIL_NAME = "Адрес электронной почты того, на кого подписываются"
    SUBSCRIBEE_USERNAME_NAME = "Ник того, на кого подписываются"

    list_display = (
        "subscriber",
        "subscribee",
    )
    list_filter = (
        ("subscriber__email", custom_titled_filter(SUBSCRIBER_EMAIL_NAME)),
        (
            "subscriber__username",
            custom_titled_filter(SUBSCRIBER_USERNAME_NAME),
        ),
        ("subscribee__email", custom_titled_filter(SUBSCRIBEE_EMAIL_NAME)),
        (
            "subscribee__username",
            custom_titled_filter(SUBSCRIBEE_USERNAME_NAME),
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(SubscriberSubscribee, SubscriberSubscribeeAdmin)

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
    list_display = (
        "subscriber",
        "subscribee",
    )
    list_filter = (
        ("subscriber__email", custom_titled_filter("Subscriber email")),
        ("subscriber__username", custom_titled_filter("Subscriber username")),
        ("subscribee__email", custom_titled_filter("Subscribee email")),
        ("subscribee__username", custom_titled_filter("Subscribee username")),
    )


admin.site.register(User, UserAdmin)
admin.site.register(SubscriberSubscribee, SubscriberSubscribeeAdmin)

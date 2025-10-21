from django.apps import apps
from django.conf import settings
from django.db import router


def is_valid_app(app_label: str) -> bool:
    return apps.is_installed(app_label) and app_label in settings.APIS


def is_same_api(app_label_1: str, app_label_2: str) -> bool:
    return settings.APIS.get(app_label_1) == settings.APIS.get(app_label_2)


def is_same_database(model_1, model_2) -> bool:
    return router.db_for_read(model_1) == router.db_for_read(model_2)


def is_possible_connect_apps(app_label_1: str, app_label_2: str) -> bool:
    if not is_valid_app(app_label_1) or not is_valid_app(app_label_2):
        return False

    return is_same_api(app_label_1, app_label_2)

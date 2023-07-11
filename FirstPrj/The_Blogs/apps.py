from django.apps import AppConfig
import FirstPrj.UserDefinedConstValue as UserDefinedConstValue

class TheBlogsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = UserDefinedConstValue.APPNAME

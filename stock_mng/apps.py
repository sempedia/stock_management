from django.apps import AppConfig


class StockMngConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock_mng'

    def ready(self):
        import stock_mng.signals 


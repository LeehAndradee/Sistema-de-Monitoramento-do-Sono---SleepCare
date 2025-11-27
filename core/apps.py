# core/apps.py

from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    # Adicione este método:
    def ready(self):
        try:
            import pymysql
            pymysql.install_as_MySQLdb()
        except ImportError:
            pass # Se o pymysql não estiver instalado, ignoramos.
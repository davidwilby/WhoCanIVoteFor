from django.core.management.base import BaseCommand


from django.db import connection


class Command(BaseCommand):
    """
    Runs SQL query to truncate tables that are populated with data
    after initial migrate. This is used before database replication
    is setup to avoid tablesync errors caused by trying to sync tables
    that already contain data e.g. the initial Site object.
    """

    def handle(self, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                BEGIN;
                TRUNCATE "auth_permission", "auth_group_permissions", "auth_user_user_permissions", "django_admin_log", "robots_rule_sites", "django_content_type", "django_site", "django_migrations", "spatial_ref_sys"  RESTART IDENTITY;
                COMMIT;
                """
            )

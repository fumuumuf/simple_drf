from .middleware import get_current_db_name


class CustomDBRouter:
    """
    DB のルーティングを制御します.
    """

    def common_routing(self, model):
        db = get_current_db_name() # or 'default'
        # print('routing db', db)
        return db

    def db_for_read(self, model, **hints):
        return self.common_routing(model)

    def db_for_write(self, model, **hints):
        return self.common_routing(model)

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        allow migrations
        """
        return None

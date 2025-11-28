import threading

class UserContext:
    _local = threading.local()

    @classmethod
    def get_user(cls):
        user = getattr(cls._local, "user", None)
        if user is None:
            raise RuntimeError("User not found in context")
        return user

    @classmethod
    def set_user(cls, user):
        cls._local.user = user

    @classmethod
    def clear(cls):
        if hasattr(cls._local, "user"):
            del cls._local.user

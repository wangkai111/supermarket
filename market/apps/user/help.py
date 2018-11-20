import hashlib
from django.conf import settings


def set_password(password):
    # 加密再加密
    new_password = "{}{}".format(password,settings.SECRET_KEY)
    h = hashlib.md5(new_password.encode("utf-8"))
    return h.hexdigest()

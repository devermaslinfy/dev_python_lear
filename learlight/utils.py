import string
import random

from datetime import datetime


def generate_id(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_internal_id():
    return '-'.join([str(datetime.now().year)[2:], generate_id(3, string.digits)])


def generate_external_id():
    return generate_id(4, string.digits)


class StreamBuffer(object):

    def write(self, value):
        return value

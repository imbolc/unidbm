import sys


if sys.version_info >= (3, ):
    basestring = str


def name_to_object(str_or_obj):
    if isinstance(str_or_obj, basestring):
        if '.' not in str_or_obj:
            str_or_obj = str_or_obj + '.'
        mod_name, obj_name = str_or_obj.rsplit('.', 1)
        __import__(mod_name)
        mod = sys.modules[mod_name]
        return getattr(mod, obj_name) if obj_name else mod
    else:
        return str_or_obj

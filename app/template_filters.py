from django.template.defaulttags import register

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='range')
def range(min=5):
    return range(min)
__author__ = 'faebser'


class Option(object):
    value = None
    choices = None
    reference = None

    def __unicode__(self):
        return unicode(self.value)

    def __str__(self):
        return self.__unicode__()

    def has_choices(self):
        if self.choices is None or len(self.choices) is 0:
            return False
        else:
            return True

    def update_value(self, value):
        self.reference.value = value
        self.value = value

    def __init__(self, ref, choices=None, ):
        self.value = ref.value
        self.choices = choices
        self.reference = ref

    def __repr__(self):
        return str(self.value)


class Section(object):
    options = None
    template = None

    def update(self, option, value):
        self.options[option].update_value(value)

    def __unicode__(self):
        return unicode(self.options)

    def __str__(self):
        return self.__unicode__()

    def __init__(self):
        pass

    def to_dict(self):
        data = dict()
        for key in self.options.iterkeys():
            data.update({
                key: self.options[key].value
            })
        return data

    def __repr__(self):
        return unicode(self.options)

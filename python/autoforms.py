#!/usr/bin/python3

import requests
from lxml import html
import traceback

def pError(*args):
    print(*args)
    traceback.print_exc()

url = 'http://www.spiegel.de/extra/a-961705.html'

def getTree(url):
    result = requests.get(url)
    return html.fromstring(result.content)

def autoForms(tree):
    for form in tree.xpath('.//form'):
        yield AutoForm(form)


class Base():
    __slots__ = ('name', 'value')

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "[%s: %s]" % (self.name, self.value)

class Select():
    __slots__ = ('name', 'value', 'values')

    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.value = ''

    def __repr__(self):
        return "[Select %s: %s (%s)]" % (self.name, self.value, self.values)

    def fromTree(tree):
        values = {}

        for o in tree.xpath('.//option'):
            try:
                val = o.attrib['data-value']
            except:
                val = o.attrib.get('value', '')

            #print('is', val, o.attrib, o.text)
            values[val] = o.text

        return Select(tree.name, values)

    def select(self, value):
        if value not in self.values:
            raise Exception("Value %s not in %s" % (value, self.name))
        self.value = value

class Input():
    __slots__ = ('name', 'value')

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "[%s: %s]" % (self.name, self.value)

    def set(self, value):
        self.value = value

    def fromTree(tree):
        typ = {
            'hidden':   InputHidden,
            'submit':   InputSubmit,
            'text':     InputText,
            'checkbox': InputCheckBox
        }[tree.attrib['type'].lower()]
        return typ(tree.name, tree.attrib.get('value', ''))

class InputHidden(Input):
    def __repr__(self):
        return "[Input/Hidden: %s %s]" % (self.name, self.value)

class InputText(Input):
    def __repr__(self):
        return "[Input/Text: %s %s]" % (self.name, self.value)

class InputSubmit(Input):
    def __repr__(self):
        return "[Input/Submit: %s %s]" % (self.name, self.value)

    def set(self):
        raise Exception("TODO")

class InputCheckBox(Input):
    def __repr__(self):
        return "[Input/Checkbox: %s %s]" % (self.name, self.value)

    def set(self, value):
        self.value = int(not not value)

class AutoForm():
    __slots__ = ('_inputs')

    def __init__(self, tree):
        #self.action = tree.attrib['action']
        self._inputs = {}

        for tag in tree.xpath('.//input'):
            try:
                self._inputs[tag.name] = Input.fromTree(tag)
            except Exception as e:
                pError('err', e, tag, tag.attrib)

        for tag in tree.xpath('.//select'):
            try:
                self._inputs[tag.name] = Select.fromTree(tag)
            except Exception as e:
                pError('err', e, tag, tag.attrib)

    def __getitem__(self, name):
        return self._inputs[name]


from pprint import pprint
tree = getTree(url)
for form in autoForms(tree):
    pprint(form._inputs)


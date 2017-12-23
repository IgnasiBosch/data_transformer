import html

from html.parser import HTMLParser


class Transformer:
    def __init__(self, source, target_schema):
        self.source = source
        self.target_schema = target_schema
        self.target = {}

    def transform(self):
        self._transform_level(self.source, self.target,
                              self.target_schema["root"])

        return self.target

    @staticmethod
    def html_unescape(value):
        return html.unescape(value)

    @staticmethod
    def html_cleaner(raw_html):
        class MLStripper(HTMLParser):
            def error(self, message):
                pass

            def __init__(self):
                super().__init__()
                self.reset()
                self.strict = False
                self.convert_charrefs = True
                self.fed = []

            def handle_data(self, d):
                self.fed.append(d)

            def get_data(self):
                return ''.join(self.fed)

        def strip_tags(_html):
            s = MLStripper()
            s.feed(_html)
            return s.get_data()

        return strip_tags(raw_html)
        # clean = re.compile('<.*?>')
        # clean_text = re.sub(clean, '', raw_html)
        # return clean_text

    def _transform_level(self, source_level, target_level, target_schema_level):
        for key, value in target_schema_level.items():
            if type(value) is list:
                self._handle_list_node(
                    key, source_level, target_level, value
                )
            elif type(value) is str:
                self._handle_string_node(
                    key, source_level, target_level, value
                )
            elif type(value) is dict:
                self._handle_dict_node(
                    key, source_level, target_level, target_schema_level
                )

    def _handle_dict_node(self, key, source_level, target_level,
                          target_schema_level):
        target_level.update({key: {}})
        self._transform_level(
            source_level,
            target_level[key],
            target_schema_level[key]
        )

    def _handle_string_node(self, key, source_level, target_level, value):
        _value = source_level
        if not value:
            _value = value
        else:
            for _key in value.split('>'):
                if self._has_funcs(_key):
                    _value = self._handle_funcs(_key, _value)
                else:
                    _value = _value[_key]

        target_level.update({key: _value})

    def _handle_list_node(self, key, source_level, target_level, value):
        _value = source_level
        value_list = []
        for _key in value[0].split('>'):
            if self._has_schema_ref(_key):
                self._handle_schema_ref(_key, _value, value_list)
            else:
                _value = _value[_key]
        target_level.update({key: value_list})

    def _handle_schema_ref(self, _key, _value, value_list):
        split_key = _key.split('$')
        _key = split_key[0]
        _value = _value[_key]
        for _item in _value:
            v = {}
            value_list.append(v)
            self._transform_level(_item, v, self._get_schema_ref(split_key[1]))

    def _get_schema_ref(self, schema_key):
        return self.target_schema[schema_key]

    def _handle_funcs(self, _key, _value):
        split_key = _key.split(':')
        _key = split_key[0]
        _value = _value[_key]
        for _func in split_key[1:]:
            _value = getattr(self, _func)(_value)
        return _value

    @staticmethod
    def _has_funcs(string):
        return ':' in string

    @staticmethod
    def _has_schema_ref(string):
        return '$' in string

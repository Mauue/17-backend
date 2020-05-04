class CodeWithMessage:
    def __init__(self, code, msg):
        self._code = code
        self._msg = msg

    def with_message(self, msg):
        c = CodeWithMessage(self.code, msg)
        return c

    @property
    def code(self):
        return self._code

    @property
    def msg(self):
        return self._msg


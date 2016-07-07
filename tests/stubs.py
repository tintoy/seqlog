import logging


class StubStructuredLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()

        self.records = []
        self.messages = []

    @property
    def no_records(self):
        return len(self.records) == 0

    def pop(self):
        return (
            self.records.pop(),
            self.messages.pop()
        )

    def pop_message(self):
        self.records.pop()

        return self.messages.pop()

    def pop_record(self):
        self.messages.pop()

        return self.records.pop()

    def emit(self, record):
        self.records.append(record)
        self.messages.append(
            self.format(record)
        )

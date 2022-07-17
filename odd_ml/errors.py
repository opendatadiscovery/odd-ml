from email import message


class WrongDataEntityTypeError(Exception):
    message = "Entity is not a dataset"

    def __init__(self):
        super().__init__(self.message)


class ProfilerError(Exception):
    pass

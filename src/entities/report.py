class Report:
    name: str
    title: str
    body: str

    def __init__(self, name: str, title: str, body: str) -> None:
        self.name = name
        self.title = title
        self.body = body

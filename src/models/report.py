class Report:
    name: str
    title: str
    body: str
    date: str

    def __init__(self, name: str, title: str, body: str, date: str) -> None:
        self.name = name
        self.title = title
        self.body = body
        self.date = date

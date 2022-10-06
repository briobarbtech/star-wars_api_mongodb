class Report:
    userId: str
    id: str
    title: str
    body: str

    def __init__(self, userId: str, id: str, title: str, body: str) -> None:
        self.userId = userId
        self.id = id
        self.title = title
        self.body = body

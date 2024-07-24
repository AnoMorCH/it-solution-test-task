class Message:
    """Return a dictionary as a message to send to the client."""

    MSG_KEY = "msg"

    def __init__(self, body: str) -> None:
        self.body = body

    def get(self) -> dict:
        """Return message."""
        return {self.MSG_KEY: self.body}

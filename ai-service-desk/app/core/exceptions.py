class TicketNotFoundError(Exception):
    """Raised when a ticket with the given ID does not exist."""

    def __init__(self, ticket_id: str) -> None:
        self.ticket_id = ticket_id
        super().__init__(f"Ticket '{ticket_id}' not found")


class ClosedTicketError(Exception):
    """Raised when attempting to reopen a closed ticket."""

    def __init__(self, ticket_id: str) -> None:
        self.ticket_id = ticket_id
        super().__init__(f"Ticket '{ticket_id}' is closed and cannot be reopened")
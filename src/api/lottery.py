from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import date
from uuid import uuid4
from ..models.lottery_ticket import LotteryTicket
from ..models.lottery_ticket_create import LotteryTicketCreate

# Router for lottery-related endpoints
lottery_router = APIRouter()

# In-memory database for lottery tickets
tickets_db: List[LotteryTicket] = [
    LotteryTicket(
        ticket_number="A12345",
        ticket_price=100.0,
        is_winner=True,
        prize_amount=1.0,
        ticket_id="1656d2eb-8b44-4341-8fce-0ef2720955ce",
        purchase_date=date(2024, 10, 30)
    ),
    LotteryTicket(
        ticket_number="A12345",
        ticket_price=200.0,
        is_winner=True,
        prize_amount=2.0,
        ticket_id="1294c4f7-d31f-489a-93eb-a724addab76f",
        purchase_date=date(2024, 11, 21)
    ),
    LotteryTicket(
        ticket_number="A12345",
        ticket_price=300.0,
        is_winner=True,
        prize_amount=3.0,
        ticket_id="d78cc300-366c-475c-a90f-3bdee8eadf94",
        purchase_date=date(2024, 11, 20)
    ),
    LotteryTicket(
        ticket_number="A12345",
        ticket_price=100.0,
        is_winner=True,
        prize_amount=4.0,
        ticket_id="e68dff93-965d-44ac-92cf-9dfb5cf48db5",
        purchase_date=date(2024, 10, 30)
    ),
    LotteryTicket(
        ticket_number="A12345",
        ticket_price=100.0,
        is_winner=True,
        prize_amount=5.0,
        ticket_id="5aacd4f4-ee58-45a1-8570-d9137c8f0055",
        purchase_date=date(2024, 5, 30)
    ),
    LotteryTicket(
        ticket_number="A12345",
        ticket_price=100.0,
        is_winner=True,
        prize_amount=6.0,
        ticket_id="4afaf74e-410a-4ecd-82ae-032e88edf6db",
        purchase_date=date(2024, 1, 1)
    )
]

@lottery_router.get("/tickets", response_model=List[LotteryTicket])
def get_tickets(sort_by: Optional[str] = None, order: Optional[str] = "asc"):
    """
    Retrieve all tickets.
    - Optional parameter `sort_by` allows sorting by any field.
    - Optional parameter `order` determines sorting direction ('asc' or 'desc').
    """

    # Returning data as is if required params are not provided
    if not sort_by:
        return tickets_db

    # Ensure order is a valid string
    if order is None:
        order = "asc"  # Default value

    # Check if model has passed field
    if sort_by and field_in_model(sort_by, LotteryTicket):
        # Defining the sorting order
        is_reverse = order.lower() == "desc"
        # Sorting
        return sorted(
            tickets_db,
            key=lambda x: getattr(x, sort_by),
            reverse=is_reverse
        )

    # Returning data as is otherwise
    return tickets_db

@lottery_router.get("/tickets/statistics")
def get_statistics():
    """
    Retrieve statistics:
    - Average ticket price
    - Total, min, max, avg for all numeric fields
    - Number of winning tickets
    - Total prize amount
    """
    if not tickets_db:
        raise HTTPException(status_code=404, detail="No tickets available for analysis.")

    # Helper function to calculate statistics for a numeric field
    def calculate_stats(values):
        return {
            "total": sum(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values) if values else 0,
        }

    # Extract numeric field values
    ticket_prices = [ticket.ticket_price for ticket in tickets_db]
    prize_amounts = [ticket.prize_amount or 0 for ticket in tickets_db]
    total_winners = [1 if ticket.is_winner else 0 for ticket in tickets_db]  # Boolean to numeric

    # Calculate statistics for each field
    stats = {
        "ticket_price": calculate_stats(ticket_prices),
        "prize_amount": calculate_stats(prize_amounts),
        "winners_count": calculate_stats(total_winners),
    }

    return stats

@lottery_router.post("/tickets", response_model=LotteryTicket)
def add_ticket(ticket: LotteryTicketCreate):
    """
    Add a new ticket to the database with auto-generated ID and purchase date.
    """
    new_ticket = LotteryTicket(
        ticket_id=str(uuid4()),
        purchase_date=date.today(),
        **ticket.model_dump()
    )
    tickets_db.append(new_ticket)
    return new_ticket

@lottery_router.put("/tickets/{ticket_id}", response_model=LotteryTicket)
def update_ticket(ticket_id: str, updated_ticket: LotteryTicketCreate):
    """
    Update ticket information by ID.
    """
    for i, ticket in enumerate(tickets_db):
        if ticket.ticket_id == ticket_id:
            # Create a new LotteryTicket object while preserving ticket_id and purchase_date
            tickets_db[i] = LotteryTicket(
                ticket_id=ticket.ticket_id,
                purchase_date=ticket.purchase_date,
                **updated_ticket.model_dump()
            )
            return tickets_db[i]
    raise HTTPException(status_code=404, detail="Ticket with this ID not found.")

@lottery_router.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: str):
    """
    Delete a ticket by ID.
    """
    for i, ticket in enumerate(tickets_db):
        if ticket.ticket_id == ticket_id:
            del tickets_db[i]
            return {"message": f"Ticket with ID {ticket_id} has been deleted."}
    raise HTTPException(status_code=404, detail="Ticket with this ID not found.")

def field_in_model(field: str, model: type) -> bool:
    """
    Check if a field exists in the model or its parent models.
    """
    for cls in model.__mro__:
        if field in getattr(cls, "__annotations__", {}):
            return True
    return False
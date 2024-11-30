from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import date
from ..models.lottery import LotteryTicket

# Router for lottery-related endpoints
lottery_router = APIRouter()

# In-memory database for lottery tickets
tickets_db: List[LotteryTicket] = []

@lottery_router.get("/tickets", response_model=List[LotteryTicket])
def get_tickets(sort_by: Optional[str] = None):
    """
    Retrieve all tickets.
    - Optional parameter `sort_by` allows sorting by any field.
    """
    if sort_by and sort_by in LotteryTicket.__annotations__:
        return sorted(tickets_db, key=lambda x: getattr(x, sort_by))
    return tickets_db

@lottery_router.get("/tickets/statistics")
def get_statistics():
    """
    Retrieve statistics:
    - Average ticket price
    - Number of winning tickets
    - Total prize amount
    """
    if not tickets_db:
        raise HTTPException(status_code=404, detail="No tickets available for analysis.")

    # Calculate total ticket price
    total_price = sum(ticket.ticket_price for ticket in tickets_db)

    # Filter winners and count
    winners = [ticket for ticket in tickets_db if ticket.is_winner]

    # Sum prize amounts, ignoring None values
    total_prize = sum(ticket.prize_amount or 0 for ticket in winners)

    return {
        "average_ticket_price": total_price / len(tickets_db),
        "total_winners": len(winners),
        "total_prize_amount": total_prize
    }


@lottery_router.post("/tickets", response_model=LotteryTicket)
def add_ticket(ticket: LotteryTicket):
    """
    Add a new ticket to the database.
    """
    if any(existing_ticket.ticket_id == ticket.ticket_id for existing_ticket in tickets_db):
        raise HTTPException(status_code=400, detail="Ticket with this ID already exists.")
    tickets_db.append(ticket)
    return ticket

@lottery_router.put("/tickets/{ticket_id}", response_model=LotteryTicket)
def update_ticket(ticket_id: int, updated_ticket: LotteryTicket):
    """
    Update ticket information by ID.
    """
    for i, ticket in enumerate(tickets_db):
        if ticket.ticket_id == ticket_id:
            tickets_db[i] = updated_ticket
            return updated_ticket
    raise HTTPException(status_code=404, detail="Ticket with this ID not found.")

@lottery_router.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    """
    Delete a ticket by ID.
    """
    for i, ticket in enumerate(tickets_db):
        if ticket.ticket_id == ticket_id:
            del tickets_db[i]
            return {"message": f"Ticket with ID {ticket_id} has been deleted."}
    raise HTTPException(status_code=404, detail="Ticket with this ID not found.")

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import date
from uuid import uuid4
from ..models.lottery_ticket import LotteryTicket
from ..models.lottery_ticket_create import LotteryTicketCreate

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

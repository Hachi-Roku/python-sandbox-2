from pydantic import BaseModel
from typing import Optional

class LotteryTicketCreate(BaseModel):
    """
    Model for creating a lottery ticket. Does not include ID or purchase date.
    """
    ticket_number: str
    ticket_price: float
    is_winner: bool
    prize_amount: Optional[float] = 0.0

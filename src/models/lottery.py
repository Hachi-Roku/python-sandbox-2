from pydantic import BaseModel
from typing import Optional
from datetime import date

# Model for a lottery ticket
class LotteryTicket(BaseModel):
    ticket_id: int
    ticket_number: str
    purchase_date: date
    ticket_price: float
    is_winner: bool
    prize_amount: Optional[float] = 0.0

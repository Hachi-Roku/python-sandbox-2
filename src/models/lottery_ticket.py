from datetime import date
from .lottery_ticket_create import LotteryTicketCreate

class LotteryTicket(LotteryTicketCreate):
    """
    Full model for a lottery ticket. Extends LotteryTicketCreate with ID and purchase date.
    """
    ticket_id: str
    purchase_date: date

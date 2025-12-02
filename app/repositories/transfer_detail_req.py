from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
class TransferDetailReq(BaseModel):
    roomId: int
    payeeUserId: int
    amount: Decimal

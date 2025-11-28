from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
class TransferDetailReq(BaseModel):
    id: int
    roomId: int
    payerUserId: int
    payeeUserId: int
    amount: Decimal
    createTime: datetime

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.db_utils import add_transaction, get_balance, get_monthly_summary
from app.utils.utils import format_money

router = APIRouter()

class TransactionRequest(BaseModel):
    telegram_id: str
    type: str  # income / expense
    amount: int
    description: Optional[str] = "tanpa keterangan"

@router.post("/transaction")
async def record_transaction(req: TransactionRequest):
    if req.type not in ["income", "expense"]:
        return {"error": "Type must be 'income' or 'expense'"}
    
    add_transaction(req.telegram_id, req.type, req.amount, req.description)
    return {"message": f"{req.type.capitalize()} {format_money(req.amount)} berhasil dicatat!"}


@router.get("/balance")
async def check_balance(telegram_id: str):
    balance = get_balance(telegram_id)
    return {"balance": format_money(balance)}


@router.get("/summary")
async def monthly_summary(telegram_id: str):
    summary = get_monthly_summary(telegram_id)
    return {
        "total_income": format_money(summary["total_income"]),
        "total_expense": format_money(summary["total_expense"]),
        "remaining": format_money(summary["total_income"] - summary["total_expense"])
    }

# --- Keep-Alive Endpoint ---
@router.get("/keep-alive")
async def keep_alive():
    """
    Endpoint untuk keep-alive (digunakan oleh Uptime Checker)
    """
    return {"status": "ok"}
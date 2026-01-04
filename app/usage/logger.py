import uuid
from sqlalchemy.orm import Session

from app.database.models import UsageLog


def log_usage(
    db: Session,
    api_key_id: str,
    account_id: str,
    model_id: str,
    provider: str,
    input_tokens: int,
    output_tokens: int,
    total_cost: float
):
    usage = UsageLog(
        id=str(uuid.uuid4()),
        api_key_id=api_key_id,
        account_id=account_id,
        model_id=model_id,
        provider=provider,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_cost=total_cost
    )

    db.add(usage)
    db.commit()

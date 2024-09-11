"""recurrent billing table

Revision ID: 3ab984854687
Revises:
Create Date: 2024-09-07 18:48:42.471524

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3ab984854687"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLE = "recurrent_bill"


def upgrade() -> None:
    op.create_table(
        TABLE,
        sa.Column(
            "id", sa.BigInteger, primary_key=True, autoincrement=True, nullable=False
        ),
        sa.Column(
            "client_id", sa.BigInteger, sa.ForeignKey("client.id"), nullable=False
        ),
        sa.Column(
            "invoice_id", sa.BigInteger, sa.ForeignKey("invoice.id"), nullable=True
        ),
        sa.Column("product_name", sa.String(100), nullable=False),
        sa.Column("amount_expected", sa.DECIMAL(16, 2), nullable=False),
        sa.Column("date_created", sa.DateTime(timezone=True), nullable=False),
        sa.Column("date_due", sa.Date(), nullable=False),
        sa.Column("date_updated", sa.DateTime(timezone=True)),
        sa.Column("payment_status", sa.Integer, nullable=False),
    )

    op.create_index(
        "recurrent_bill_args_req", TABLE, ["id", "client_id"], if_not_exists=True
    )
    op.create_index(
        "recurrent_bill_invoice_req", TABLE, ["id", "invoice_id"], if_not_exists=True
    )


def downgrade() -> None:
    op.drop_index("recurrent_bill_args_req", TABLE, if_exists=True)
    op.drop_index("recurrent_bill_invoice_req", TABLE, if_exists=True)
    op.drop_table(TABLE)

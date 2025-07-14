"""invoice recurrent bill fk

Revision ID: 8fbc4e6f390c
Revises: 3ab984854687
Create Date: 2024-09-10 20:27:36.804011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fbc4e6f390c'
down_revision: Union[str, None] = '3ab984854687'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLE = 'invoice'

def upgrade() -> None:
    op.add_column(TABLE, sa.Column('recurrent_bill_id', sa.BigInteger, sa.ForeignKey('recurrent_bill.id')), if_not_exists=True)


def downgrade() -> None:
    op.drop_column(TABLE, 'recurrent_bill_id', if_exists=True)


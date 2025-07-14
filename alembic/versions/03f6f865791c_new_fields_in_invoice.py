"""new fields in invoice

Revision ID: 03f6f865791c
Revises: 8fbc4e6f390c
Create Date: 2025-07-07 03:55:41.635503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03f6f865791c'
down_revision: Union[str, None] = '8fbc4e6f390c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE = 'invoice'

def upgrade() -> None:
    op.add_column(TABLE, sa.Column('send_reminders', sa.Boolean(), nullable=True), if_not_exists=True)
    op.add_column(TABLE, sa.Column('reminder_frequency', sa.Integer(), nullable=True), if_not_exists=True)
    op.add_column(TABLE, sa.Column('reminder_logs', sa.JSON(), nullable=True), if_not_exists=True)


def downgrade() -> None:
    op.drop_column(TABLE, 'reminder_logs', if_exists=True)
    op.drop_column(TABLE, 'reminder_frequency', if_exists=True)
    op.drop_column(TABLE, 'send_reminders', if_exists=True)

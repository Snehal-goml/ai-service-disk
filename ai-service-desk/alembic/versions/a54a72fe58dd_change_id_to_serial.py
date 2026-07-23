"""change_id_to_serial

Revision ID: a54a72fe58dd
Revises: ecd67b50d025
Create Date: 2026-07-23 09:15:41.875171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a54a72fe58dd'
down_revision: Union[str, Sequence[str], None] = 'ecd67b50d025'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: change id from UUID to SERIAL."""
    # Drop existing table and recreate with new id type
    op.drop_table('tickets')
    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('priority', sa.String(20), default='medium'),
        sa.Column('status', sa.String(20), default='open'),
        sa.Column('assignee_email', sa.String(254), nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema: change id back to UUID."""
    op.drop_table('tickets')
    op.create_table(
        'tickets',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('priority', sa.String(20), default='medium'),
        sa.Column('status', sa.String(20), default='open'),
        sa.Column('assignee_email', sa.String(254), nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
    )

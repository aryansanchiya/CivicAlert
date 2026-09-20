"""make road name nullable

Revision ID: 5c6fc88501cf
Revises: e3d62b860b10
Create Date: 2026-09-20
"""

from alembic import op
import sqlalchemy as sa


revision = "5c6fc88501cf"
down_revision = "e3d62b860b10"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "roads",
        "name",
        existing_type=sa.String(length=255),
        nullable=True,
    )


def downgrade():
    op.alter_column(
        "roads",
        "name",
        existing_type=sa.String(length=255),
        nullable=False,
    )

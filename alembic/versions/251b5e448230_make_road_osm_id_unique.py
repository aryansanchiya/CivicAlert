"""make road osm id unique

Revision ID: 251b5e448230
Revises: 5c6fc88501cf
Create Date: 2026-09-21 06:38:19.891460

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "251b5e448230"
down_revision = "5c6fc88501cf"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index(
        "ix_roads_osm_id",
        table_name="roads",
    )

    op.create_index(
        "ix_roads_osm_id",
        "roads",
        ["osm_id"],
        unique=True,
    )


def downgrade():
    op.drop_index(
        "ix_roads_osm_id",
        table_name="roads",
    )

    op.create_index(
        "ix_roads_osm_id",
        "roads",
        ["osm_id"],
        unique=False,
    )

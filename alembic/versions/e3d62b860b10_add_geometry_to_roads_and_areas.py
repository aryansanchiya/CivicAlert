"""add geometry to roads and areas

Revision ID: e3d62b860b10
Revises: a6b2727530d9
Create Date: 2026-09-20 08:42:04.573587

"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry


# revision identifiers, used by Alembic.
revision = "e3d62b860b10"
down_revision = "a6b2727530d9"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "areas",
        sa.Column(
            "geometry",
            Geometry(
                geometry_type="MULTIPOLYGON",
                srid=4326,
                dimension=2,
		spatial_index=False
            ),
            nullable=True,
        ),
    )

    op.create_index(
        "idx_areas_geometry",
        "areas",
        ["geometry"],
        unique=False,
        postgresql_using="gist",
    )

    op.add_column(
        "roads",
        sa.Column(
            "geometry",
            Geometry(
                geometry_type="LINESTRING",
                srid=4326,
                dimension=2,
		spatial_index=False
            ),
            nullable=True,
        ),
    )

    op.create_index(
        "idx_roads_geometry",
        "roads",
        ["geometry"],
        unique=False,
        postgresql_using="gist",
    )


def downgrade():
    op.drop_index(
        "idx_roads_geometry",
        table_name="roads",
        postgresql_using="gist",
    )

    op.drop_column("roads", "geometry")

    op.drop_index(
        "idx_areas_geometry",
        table_name="areas",
        postgresql_using="gist",
    )

    op.drop_column("areas", "geometry")

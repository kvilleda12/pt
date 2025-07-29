"""forcing a clean up

Revision ID: 4300edc8d58e
Revises: 6208539e9aeb
Create Date: 2025-07-28 01:11:38.885087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4300edc8d58e'
down_revision: Union[str, None] = '6208539e9aeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TABLE IF EXISTS training_sources.body_part_counts CASCADE;")
    op.execute("DROP TYPE IF EXISTS body_id_enum CASCADE;")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

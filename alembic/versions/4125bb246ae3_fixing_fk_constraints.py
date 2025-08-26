"""fixing fk constraints (ALTER-only; no table re-creates)

Revision ID: 4125bb246ae3
Revises: 7ca2778da7fb
Create Date: 2025-08-26 10:25:25.387232
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4125bb246ae3'
down_revision: Union[str, None] = '7ca2778da7fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply FK/constraint fixes without re-creating tables."""

    # 1) Expand the ENUM with the new fine-grained labels (safe if repeated).
    #    Supabase/Postgres 15 supports IF NOT EXISTS.
    new_labels = [
        'ls','rs','lt','rt','lb','rb','lh','rh','lq','rq','lc','rc','la','ra'
    ]
    for val in new_labels:
        op.execute(f"ALTER TYPE body_id_enum ADD VALUE IF NOT EXISTS '{val}'")

    # 2) Drop FKs that force pre-populating training_sources.body_part_counts.
    #    These are the default Postgres names (<table>_<column>_fkey).
    #    If you've custom-named them, change the names below accordingly.
    try:
        op.drop_constraint(
            'problem_reports_body_part_id_fkey',
            'problem_reports',
            schema='frontend_data',
            type_='foreignkey',
        )
    except Exception:
        # already dropped or never existed
        pass

    try:
        op.drop_constraint(
            'research_paper_sources_part_id_fkey',
            'research_paper_sources',
            schema='training_sources',
            type_='foreignkey',
        )
    except Exception:
        pass

    try:
        op.drop_constraint(
            'textbook_sources_part_id_fkey',
            'textbook_sources',
            schema='training_sources',
            type_='foreignkey',
        )
    except Exception:
        pass

    # 3) Tighten the BP check constraint: id IN (1,2) instead of (1,2,3).
    #    Drop old constraint and add the new one.
    try:
        op.drop_constraint(
            'check_valid_bp_id',
            'part',
            schema='training_sources',
            type_='check',
        )
    except Exception:
        # if it didn't exist, that's fine
        pass

    op.create_check_constraint(
        'check_valid_bp_id',
        'part',
        'id IN (1, 2)',
        schema='training_sources',
    )

    # 4) (Optional) Make problem_reports.body_part_id NOT NULL.
    #    If you might have NULLs from earlier inserts, set a default first.
    op.execute("""
        UPDATE frontend_data.problem_reports
        SET body_part_id = 'e'
        WHERE body_part_id IS NULL
    """)
    # existing_type defined to keep Alembic happy on some setups
    existing_enum = sa.Enum(
        'n','f','h','a','l','s','c','b','e',
        'ls','rs','lt','rt','lb','rb','lh','rh','lq','rq','lc','rc','la','ra',
        name='body_id_enum'
    )
    try:
        op.alter_column(
            'problem_reports',
            'body_part_id',
            schema='frontend_data',
            existing_type=existing_enum,
            nullable=False,
        )
    except Exception:
        # if it's already NOT NULL, that's fine
        pass


def downgrade() -> None:
    """Recreate dropped FKs and loosen constraint; ENUM value removals are not performed."""
    # Note: Postgres cannot *remove* enum values easily; we leave added labels in place.

    # Recreate original FK constraints (adjust names if you had custom names).
    try:
        op.create_foreign_key(
            'problem_reports_body_part_id_fkey',
            source_table='problem_reports',
            referent_table='body_part_counts',
            local_cols=['body_part_id'],
            remote_cols=['id'],
            source_schema='frontend_data',
            referent_schema='training_sources',
        )
    except Exception:
        pass

    try:
        op.create_foreign_key(
            'research_paper_sources_part_id_fkey',
            source_table='research_paper_sources',
            referent_table='body_part_counts',
            local_cols=['part_id'],
            remote_cols=['id'],
            source_schema='training_sources',
            referent_schema='training_sources',
        )
    except Exception:
        pass

    try:
        op.create_foreign_key(
            'textbook_sources_part_id_fkey',
            source_table='textbook_sources',
            referent_table='body_part_counts',
            local_cols=['part_id'],
            remote_cols=['id'],
            source_schema='training_sources',
            referent_schema='training_sources',
        )
    except Exception:
        pass

    # Loosen the check constraint back to (1,2,3)
    try:
        op.drop_constraint(
            'check_valid_bp_id',
            'part',
            schema='training_sources',
            type_='check',
        )
    except Exception:
        pass

    op.create_check_constraint(
        'check_valid_bp_id',
        'part',
        'id IN (1, 2, 3)',
        schema='training_sources',
    )

    # Allow NULLs again on problem_reports.body_part_id (if you want full revert)
    existing_enum = sa.Enum(
        'n','f','h','a','l','s','c','b','e',
        'ls','rs','lt','rt','lb','rb','lh','rh','lq','rq','lc','rc','la','ra',
        name='body_id_enum'
    )
    try:
        op.alter_column(
            'problem_reports',
            'body_part_id',
            schema='frontend_data',
            existing_type=existing_enum,
            nullable=True,
        )
    except Exception:
        pass
"""search_quality_tuning_field_boosting

Revision ID: 5a7f326c26ff
Revises: 2f222cc59632
Create Date: 2026-05-06 00:16:41.807702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a7f326c26ff'
down_revision: Union[str, Sequence[str], None] = '2f222cc59632'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE research_projects DROP COLUMN search_vector;
    """)
    op.execute("""
        ALTER TABLE research_projects
        ADD COLUMN search_vector tsvector GENERATED ALWAYS AS (
            setweight(to_tsvector('simple', public.immutable_unaccent(coalesce(title, ''))), 'A') || 
            setweight(to_tsvector('simple', public.immutable_unaccent(coalesce(author, ''))), 'C')
        ) STORED;
    """)
    op.execute("""
        CREATE INDEX ix_research_projects_search_vector 
        ON research_projects USING gin (search_vector);
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE research_projects DROP COLUMN search_vector;
    """)
    op.execute("""
        ALTER TABLE research_projects
        ADD COLUMN search_vector tsvector GENERATED ALWAYS AS (
            to_tsvector('simple', public.immutable_unaccent(coalesce(title, '')) || ' ' || public.immutable_unaccent(coalesce(author, '')))
        ) STORED;
    """)
    op.execute("""
        CREATE INDEX ix_research_projects_search_vector 
        ON research_projects USING gin (search_vector);
    """)

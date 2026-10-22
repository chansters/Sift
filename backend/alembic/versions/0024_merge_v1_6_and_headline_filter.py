"""Join upstream 1.6.0 and the local headline category filtering migration.

Revision ID: 0024_merge_v1_6_headline_filter
Revises: 0013_headline_category_filter, 0023_article_story_dates_index
"""

from collections.abc import Sequence

revision: str = "0024_merge_v1_6_headline_filter"
down_revision: tuple[str, str] = (
    "0013_headline_category_filter",
    "0023_article_story_dates_index",
)
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

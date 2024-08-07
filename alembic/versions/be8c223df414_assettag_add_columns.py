"""AssetTag: add columns

Revision ID: be8c223df414
Revises: d66cd7fd0e37
Create Date: 2024-07-29 19:03:25.412116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be8c223df414'
down_revision = 'd66cd7fd0e37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('url', sa.String(), nullable=True))
    op.add_column('tags', sa.Column('is_project', sa.Boolean(), nullable=False, server_default="false"))
    op.add_column('tags', sa.Column('is_post', sa.Boolean(), nullable=False, server_default="false"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tags', 'is_post')
    op.drop_column('tags', 'is_project')
    op.drop_column('tags', 'url')
    # ### end Alembic commands ###

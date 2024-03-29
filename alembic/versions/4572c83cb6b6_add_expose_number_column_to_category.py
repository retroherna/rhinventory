"""Add expose number column to Category

Revision ID: 4572c83cb6b6
Revises: 3598f0d2ca40
Create Date: 2021-11-22 17:23:12.581581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4572c83cb6b6'
down_revision = '3598f0d2ca40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('expose_number', sa.Boolean(), nullable=True))
    op.execute("UPDATE categories SET expose_number = True")
    op.alter_column('categories', 'expose_number', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'expose_number')
    # ### end Alembic commands ###

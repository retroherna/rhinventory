"""Add original hash columns to File

Revision ID: aa274b1d029d
Revises: ed5b345f047a
Create Date: 2021-11-09 21:49:16.304935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa274b1d029d'
down_revision = 'ed5b345f047a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('original_md5', sa.LargeBinary(length=16), nullable=True))
    op.add_column('files', sa.Column('original_sha256', sa.LargeBinary(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('files', 'original_sha256')
    op.drop_column('files', 'original_md5')
    # ### end Alembic commands ###

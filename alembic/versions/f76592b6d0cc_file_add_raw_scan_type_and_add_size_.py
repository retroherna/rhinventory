"""File: add raw_scan type and add size column

Revision ID: f76592b6d0cc
Revises: 71858021f889
Create Date: 2024-05-20 17:26:50.408695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f76592b6d0cc'
down_revision = '71858021f889'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('size', sa.Integer(), nullable=True))
    op.sync_enum_values('public', 'filecategory', ['collection', 'cover_page', 'dump', 'dump_metadata', 'image', 'index_page', 'logo', 'other', 'photo', 'prose', 'scan', 'test_result', 'text', 'transcription', 'unknown'], ['collection', 'cover_page', 'dump', 'dump_metadata', 'image', 'index_page', 'logo', 'other', 'photo', 'prose', 'raw_scan', 'scan', 'test_result', 'text', 'transcription', 'unknown'], [('files', 'category')], False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values('public', 'filecategory', ['collection', 'cover_page', 'dump', 'dump_metadata', 'image', 'index_page', 'logo', 'other', 'photo', 'prose', 'raw_scan', 'scan', 'test_result', 'text', 'transcription', 'unknown'], ['collection', 'cover_page', 'dump', 'dump_metadata', 'image', 'index_page', 'logo', 'other', 'photo', 'prose', 'scan', 'test_result', 'text', 'transcription', 'unknown'], [('files', 'category')], True)
    op.drop_column('files', 'size')
    # ### end Alembic commands ###

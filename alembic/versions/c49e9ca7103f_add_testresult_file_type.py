"""Add testresult file type

Revision ID: c49e9ca7103f
Revises: ca9e995a442b
Create Date: 2023-06-11 14:23:25.094945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c49e9ca7103f'
down_revision = 'ca9e995a442b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values('public', 'filecategory', ['collection', 'cover_page', 'dump', 'dump_metadata', 'image', 'index_page', 'logo', 'other', 'photo', 'prose', 'scan', 'text', 'transcription', 'unknown'], ['collection', 'cover_page', 'dump', 'dump_metadata', 'image', 'index_page', 'logo', 'other', 'photo', 'prose', 'scan', 'test_result', 'text', 'transcription', 'unknown'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values('public', 'filecategory', ['collection', 'cover_page', 'dump', 'dump_metadata', 'image', 'index_page', 'logo', 'other', 'photo', 'prose', 'scan', 'test_result', 'text', 'transcription', 'unknown'], ['collection', 'cover_page', 'dump', 'dump_metadata', 'image', 'index_page', 'logo', 'other', 'photo', 'prose', 'scan', 'text', 'transcription', 'unknown'])
    # ### end Alembic commands ###

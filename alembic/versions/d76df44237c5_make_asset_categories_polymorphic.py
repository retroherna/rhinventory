"""Make Asset categories polymorphic

Revision ID: 20cd509a831e
Revises: 3dd084df4064
Create Date: 2022-08-07 16:43:24.897100

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20cd509a831e'
down_revision = '3dd084df4064'
branch_labels = None
depends_on = None


# As per https://stackoverflow.com/a/24623979

from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

AssetCategorySaEnum = sa.Enum('unknown', 'game', 'console', 'computer', 'console_accesory', 'computer_accessory', 'computer_component', 'computer_mouse', 'keyboard', 'television', 'monitor', 'software', 'multimedia', 'receipt', 'literature', 'other', 'rewritable_media', name='assetcategory')
AssetCategoryPostgresEnum = postgresql.ENUM('unknown', 'game', 'console', 'computer', 'console_accesory', 'computer_accessory', 'computer_component', 'computer_mouse', 'keyboard', 'television', 'monitor', 'software', 'multimedia', 'receipt', 'literature', 'other', 'rewritable_media', name='assetcategory')

# Old category table
class Category(Base):
    __tablename__ = 'categories'
    id          = sa.Column(sa.Integer, primary_key=True)
    name        = sa.Column(sa.String, nullable=False)

# in-progress asset table
class Asset(Base):
    __tablename__ = 'assets'
    id          = sa.Column(sa.Integer, primary_key=True)

    # old category column
    category_id = sa.Column(sa.Integer, sa.ForeignKey('categories.id'), nullable=False)

    # new category column
    category    = sa.Column(AssetCategorySaEnum, default='unknown', nullable=True)

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    AssetCategoryPostgresEnum.create(bind)
    
    op.add_column('assets', sa.Column('category', AssetCategorySaEnum, nullable=True))
    
    session = orm.Session(bind=bind)

    asset: Asset
    for asset in session.query(Asset):
        old_category: Category = session.query(Category).get(asset.category_id)
        category_name = old_category.name.replace(" ", "_").lower()
        if category_name == "rewriteable_media":
            category_name = "rewritable_media"
        asset.category = category_name
        session.add(asset)

    session.commit()

    op.drop_constraint('assets_category_id_fkey', 'assets', type_='foreignkey')
    op.drop_column('assets', 'category_id')

    op.drop_table('category_templates')
    op.drop_table('categories')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assets', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('assets_category_id_fkey', 'assets', 'categories', ['category_id'], ['id'])
    op.drop_column('assets', 'category')
    op.create_table('categories',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('categories_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('prefix', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('counter', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('color', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('expose_number', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='categories_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('category_templates',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('key', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('value', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name='category_templates_category_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='category_templates_pkey')
    )
    # ### end Alembic commands ###

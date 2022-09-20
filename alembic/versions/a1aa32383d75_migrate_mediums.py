"""Migrate mediums

Revision ID: a1aa32383d75
Revises: dab4e5bb9f5a
Create Date: 2022-09-13 21:12:56.181603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1aa32383d75'
down_revision = 'dab4e5bb9f5a'
branch_labels = None
depends_on = None

from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Packaging(Base):
    __tablename__ = 'packagings'
    id: int          = sa.Column(sa.Integer, primary_key=True)  # type: ignore
    name: str        = sa.Column(sa.String, nullable=False)  # type: ignore

class AssetPackaging(Base):
    __tablename__ = 'asset_packaging'
    id: int           = sa.Column(sa.Integer, primary_key=True)  # type: ignore
    asset_id: int     = sa.Column(sa.Integer, sa.ForeignKey('assets.id'))  # type: ignore
    packaging_id: int = sa.Column(sa.Integer, sa.ForeignKey(Packaging.id))  # type: ignore

    asset = orm.relationship("Asset", backref="packaging")
    packaging = orm.relationship(Packaging, backref="assets")

class Medium(Base):
    __tablename__ = 'media'
    id: int          = sa.Column(sa.Integer, primary_key=True)  # type: ignore
    name: str        = sa.Column(sa.String, nullable=False)  # type: ignore

class AssetMedium(Base):
    __tablename__ = 'asset_mediums'
    id: int           = sa.Column(sa.Integer, primary_key=True)  # type: ignore
    asset_id: int     = sa.Column(sa.Integer, sa.ForeignKey('assets.id'))  # type: ignore
    medium_id: int    = sa.Column(sa.Integer, sa.ForeignKey(Medium.id))  # type: ignore

    #asset =  orm.relationship("Asset", backref="mediums")
    medium = orm.relationship(Medium)


class Asset(Base):
    __tablename__ = 'assets'
    id          = sa.Column(sa.Integer, primary_key=True)
    medium_id   = sa.Column(sa.Integer, sa.ForeignKey('media.id'))
    medium      = orm.relationship("Medium")#, backref="assets")

PACKAGINGS = [
    "case", "book", "sleeve", "slipcover", "slipcase",
    "long sleeve", "carton", "box", "jewel", "a5 sleeve", "tall a5 sleeve",
    "plastic sleeve", "longbox", "envelope"
]

def string_to_medium_and_packaging(string: str):
    mediums, packagings = [], []
    for thing in string.split("+"):
        thing = thing.strip()
        count = 1
        if thing[0] in "123456789":
            count = int(thing[0])
            thing = thing.lstrip("123456789").strip()
        
        if thing.lower() in PACKAGINGS:
            packagings.append((count, thing))
        else:
            mediums.append((count, thing))
    
    return mediums, packagings


def upgrade():
    print("Migrating mediums...")
    
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    medium_objects = {}
    packaging_objects = {}
    association_objects = []

    old_mediums = session.query(Medium).all()

    asset: Asset
    for asset in session.query(Asset):
        old_medium = asset.medium.name if asset.medium else None
        if old_medium:
            mediums, packagings = string_to_medium_and_packaging(old_medium)

            for count, name in mediums:
                if name.lower() in medium_objects:
                    medium = medium_objects[name.lower()]
                else:
                    medium = Medium(name=name)
                
                association = AssetMedium(asset_id=asset.id, medium=medium)
                association_objects.append(association)
            
            for count, name in packagings:
                if name.lower() in packaging_objects:
                    packaging = packaging_objects[name.lower()]
                else:
                    packaging = Packaging(name=name)
                
                association = AssetPackaging(asset_id=asset.id, packaging=packaging)
                association_objects.append(association)

    op.drop_constraint('assets_medium_id_fkey', 'assets', type_='foreignkey')
    op.drop_column('assets', 'medium_id')

    for old_medium in old_mediums:
        session.delete(old_medium)
    session.commit()

    for obj in medium_objects.items():
        session.add(obj)
    
    for obj in packaging_objects.items():
        session.add(obj)
    
    for obj in association_objects:
        session.add(obj)

    session.commit()
    
    #raise Exception()
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assets', sa.Column('medium_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('assets_medium_id_fkey', 'assets', 'media', ['medium_id'], ['id'])
    # ### end Alembic commands ###

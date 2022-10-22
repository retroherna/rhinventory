import enum

import flask_login
import sqlalchemy.orm
from sqlalchemy import func

from rhinventory.extensions import db


def get_current_user_id(self):
    """Get's current looged in user."""
    return flask_login.current_user.id


class HistoryTrait(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    created_by = db.Column(db.Integer, default=get_current_user_id)
    updated_by = db.Column(db.Integer, default=get_current_user_id, onupdate=get_current_user_id)


class Issuer(HistoryTrait):
    __tablename__ = "issuers"
    id = db.Column(db.Integer(), unique=True, primary_key=True)
    title = db.Column(db.String(255), info={"label": "Jméno vydavatele"})

    def __str__(self):
        return self.title


class Magazine(HistoryTrait):
    __tablename__ = "magazines"
    id = db.Column(db.Integer(), unique=True, primary_key=True)
    title = db.Column(db.String(255), unique=True, info={"label": "Název časopisu"})
    description = db.Column(db.Text(), default="", info={"label": "Popis"})
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=True)

    def __str__(self):
        return self.title


class BindingType(enum.Enum):
    glued = "GL"
    stapled = "ST"
    none = "NO"
    sewn = "SW"
    not_applicable = "NA"


class Periodicity(enum.Enum):
    weekly = "w"
    biweekly = "bw"
    monthly = "m"
    bimonthly = "bm"
    quarterly = "q"
    annually = "a"
    non_periodical = "np"

    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(item) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)


class MagazineForm(enum.Enum):
    electronic = "ele"
    paper = "pap"
    CD = "CD"
    DVD = "DVD"
    diskette = "dis"


class IssueStatus(enum.Enum):
    have = "h"
    dont_have = "n"
    problems = "p"


class MagazineIssue(HistoryTrait):
    __tablename__ = "magazine_issues"
    id = db.Column(db.Integer(), unique=True, primary_key=True)
    issue_number = db.Column(db.Integer(), nullable=True)
    calendar_id = db.Column(db.String(64), nullable=True)

    issue_title = db.Column(db.String(127), default="")
    current_magazine_name = db.Column(db.String(127))
    is_special_issue = db.Column(db.Boolean())

    # TODO: logo
    periodicity = db.Column(db.Enum(Periodicity))

    # TODO: index page

    published_day = db.Column(db.Integer(), nullable=True)
    published_month = db.Column(db.Integer(), nullable=True)
    published_year = db.Column(db.Integer(), nullable=True)

    page_count = db.Column(db.Integer(), nullable=True)
    circulation = db.Column(db.Integer(), nullable=True)

    chief_editor_id = db.Column(db.Integer, db.ForeignKey('parties.id'))

    issuer_id = db.Column(db.Integer(), db.ForeignKey("issuers.id"))
    issuer = db.relationship("Issuer")

    magazine_id = db.Column(db.Integer(), db.ForeignKey("magazines.id"), nullable=False)
    magazine = db.relationship("Magazine")

    note = db.Column(db.Text())

    def __str__(self):
        return f"{str(self.magazine)}: { self.calendar_id if not self.is_special_issue else self.issue_title}"


class Currency(enum.Enum):
    CZK = "CZK"
    EUR = "EUR"
    CSK = "CSK"
    SK = "SK"
    PLN = "PLN"
    GBP = "GBP"


class Format(HistoryTrait):
    __tablename__ = "formats"
    id = db.Column(db.Integer(), unique=True, primary_key=True)
    binding_type = db.Column(db.Enum(BindingType), nullable=True)
    name = db.Column(db.String(127), default="")
    width = db.Column(db.Integer())
    height = db.Column(db.Integer())

    def __str__(self):
        return self.name


class MagazineIssueVersion(HistoryTrait):
    __tablename__ = "magazine_issue_versions"
    id = db.Column(db.Integer(), unique=True, primary_key=True)
    magazine_issue_id = db.Column(db.Integer(), db.ForeignKey("magazine_issues.id"), nullable=False)
    magazine_issue = db.relationship("MagazineIssue")
    name_suffix = db.Column(db.String(127))
    # TODO: cover page
    form = db.Column(db.Enum(MagazineForm))

    format_id = db.Column(db.Integer(), db.ForeignKey("formats.id"))
    format = db.relationship("Format")

    confirmed = db.Column(db.Boolean())
    isbn = db.Column(db.String(25), nullable=True)
    barcode = db.Column(db.String(15), nullable=True)
    status = db.Column(db.Enum(IssueStatus))

    def __str__(self):
        return f"{str(self.magazine_issue)} {self.name_suffix if self.name_suffix is not None else ''}"


class MagazineIssueVersionPrice(HistoryTrait):
    __tablename__ = "magazine_issue_version_prices"
    id = db.Column(db.Integer(), unique=True, primary_key=True)

    issue_version_id = db.Column(db.Integer(), db.ForeignKey("magazine_issue_versions.id"))
    issue_version = db.relationship("MagazineIssueVersion")

    value = db.Column(db.Float())
    currency = db.Column(db.Enum(Currency))


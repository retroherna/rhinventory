from collections import defaultdict
from typing import OrderedDict

import flask.templating
from flask import Blueprint, render_template

from rhinventory.models.magdb import Magazine, MagazineIssue, MagazineIssueVersion, IssueStatus, \
    MagazineIssueVersionFiles, MagDBFileType
from rhinventory.service.public_magdb import PublicMagDBService

magdb_bp = Blueprint("magdb", __name__, url_prefix="/public-magdb")


@magdb_bp.route("/")
def index():
    return render_template("magdb/index.html")

@magdb_bp.route("/catalog")
def catalog():
    context = {
        "magazines": Magazine.query.order_by(Magazine.title).all(),
        "logos": {},
    }

    for logo in MagazineIssueVersionFiles.query.filter(MagazineIssueVersionFiles.file_type==MagDBFileType.logo).all():
        local_magazine_id = logo.magazine_issue_version.magazine_issue.magazine_id
        if local_magazine_id not in context["logos"]:
            context["logos"][local_magazine_id] = set()

        context["logos"][local_magazine_id].add(logo.file)

    return render_template("magdb/catalog.html", **context)


@magdb_bp.route("/catalog/magazine-detail/<int:magazine_id>")
def magazine_detail(magazine_id):
    context = {
        "magazine": Magazine.query.get(magazine_id),
        "issues_by_year": defaultdict(list),
        "files": {
            "cover_pages": defaultdict(list),
            "index_pages": defaultdict(list),
            "logos": defaultdict(set),
        }
    }

    special_issues = []
    issue_ids = set()

    service = PublicMagDBService()
    new_data = service.list_magazine(magazine_id)

    for issue in new_data:
        issue_ids.add(issue.id)

        if issue.is_special_issue:
            special_issues.append(issue)
            continue

        context["issues_by_year"][issue.published_year].append(issue)

    if len(special_issues):
        context["issues_by_year"]["Speciály"] = special_issues

    # get logos

    logos = MagazineIssueVersionFiles.query \
        .join(MagazineIssueVersion).join(MagazineIssue) \
        .filter(MagazineIssueVersionFiles.file_type == MagDBFileType.logo) \
        .filter(MagazineIssueVersion.magazine_issue_id.in_(issue_ids)) \
        .all()

    for logo in logos:
        context["files"]["logos"][magazine_id].add(logo.file)


    return render_template("magdb/magazine_detail.html", **context)


@magdb_bp.route("/miss-list")
def miss_list():
    context = {
        "missing_magazines": {},
        "magazines": {},
    }

    logos = defaultdict(set)
    for logo in MagazineIssueVersionFiles.query.filter(MagazineIssueVersionFiles.file_type==MagDBFileType.logo).all():
        magazine_id = logo.magazine_issue_version.magazine_issue.magazine_id
        logos[magazine_id].add(logo.file)

    for issue in MagazineIssueVersion.query.filter(
            MagazineIssueVersion.status != IssueStatus.have
    ).all():

        magazine_id = issue.magazine_issue.magazine_id
        if magazine_id not in context["missing_magazines"]:
            context["missing_magazines"][magazine_id] = []

        context["missing_magazines"][magazine_id].append(
            issue
        )

        if magazine_id not in context["magazines"]:
            context["magazines"][magazine_id] = {
                "magazine": issue.magazine_issue.magazine,
                "logos": logos[issue.magazine_issue.magazine_id] if issue.magazine_issue.magazine_id in logos else [],
            }

    context["magazines"] = OrderedDict(
        sorted(
            context["magazines"].items(),
            key=lambda x: x[1]["magazine"].title,
        )
    )

    return render_template("magdb/miss-list.html", **context)

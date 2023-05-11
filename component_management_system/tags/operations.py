from database import db
from flask import abort, make_response

from .models import Tag
from .schemas import tag_schema, tags_schema


def read_all():
    tags = Tag.query.all()
    return tags_schema.dump(tags)


def read_one(pk):
	tag = Tag.query.filter(Tag.id==pk).one_or_none()

	if tag is None:
		abort(404, f"Tag with id {pk} not found!")

	return tag_schema.dump(tag), 200


def create(tag):
	label = tag.get("label")
	existing_tag = Tag.query.filter(Tag.label==label).one_or_none()

	if existing_tag is not None:
		abort(406, f"Tag with label {label} already exists")

	new_tag = tag_schema.load(tag, session=db.session)
	db.session.add(new_tag)
	db.session.commit()
	return tag_schema.dump(new_tag), 201


def delete(pk):
	existing_tag = Tag.query.filter(Tag.id==pk).one_or_none()

	if existing_tag is None:
		abort(404, f"Tag with id {pk} not found")

	db.session.delete(existing_tag)
	db.session.commit()
	return make_response(f"{existing_tag.label}:{pk} successfully deleted", 200)

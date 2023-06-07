from flask_sqlalchemy import SQLAlchemy
from flask import g

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    created_by = db.Column(db.String(50))
    modified_on = db.Column(db.DateTime, default=None, onupdate=db.func.now())
    modified_by = db.Column(db.String(50))

    @classmethod
    def create(cls, data: dict) -> db.Model:
        """
        This function is used to create the record.
        :param data:
        :return:
        """
        record = cls(**data)
        record.created_by = g.user["email"] if g.user else None
        db.session.add(record)
        db.session.commit()
        return record

    def update(self, data: dict):
        """
        This function is used to update the record.
        :param data:
        :return:
        """
        self.modified_by = g.user["email"] if g.user else None
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        db.session.commit()

    @classmethod
    def delete(cls, **filters):
        """
        This function is used to delete the records based on filters.
        :param filters:
        :return:
        """
        db.session.query(cls).filter_by(**filters).delete()
        db.session.commit()

    def serialize(self) -> dict:
        """
        This function is used to convert the model object to a dict.
        :return:
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def rollback():
        """
        This function is used to rollback db.
        :return:
        """
        db.session.rollback()

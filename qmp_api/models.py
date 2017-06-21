from qmp_api import db


class Channel(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128))
    image = db.Column(db.String(128))
    description = db.Column(db.Text())

    @classmethod
    def from_object(cls, obj):
        return cls(obj.name, obj.name, obj.image, obj.description)

    def __init__(self, id, name, image, desc):
        self.id = id
        self.name = name
        self.image = image
        self.description = desc

    def __str__(self):
        return "<Channel {}>".format(self.name, self.id)

    def __repr__(self):
        return str(self)
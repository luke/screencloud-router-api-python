from flask.ext.restful import Resource

from screencloud.sql import models
from .. import g, schemas

class List(Resource):
    def get(self):
        pass

    def post(self):
        acc = schemas.Account(g.request.get_json())
        acc.validate()
        db_acc = models.Account(**acc.to_native())
        g.sql.add(db_acc)
        g.sql.commit()
        return schemas.Account(db_acc.__dict__)


class Item(Resource):
    def get(self, id):
        pass

    def patch(self, id):
        pass

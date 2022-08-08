from dao.director import DirectorDAO


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, director_d):
        return self.dao.create(director_d)

    def update(self, director_d):
        self.dao.update(director_d)

    def update_partial(self, director_d):
        did = director_d.get("id")
        director = self.dao.get_one(did)

        if "name" in director_d:
            director.title = director_d.get("name")

        self.dao.update(director)

    def delete(self, rid):
        self.dao.delete(rid)
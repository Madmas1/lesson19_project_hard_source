from dao.genre import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, gid):
        return self.dao.get_one(gid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, genre_d):
        return self.dao.create(genre_d)

    def update(self, genre_d):
        self.dao.update(genre_d)
        return self.dao

    def update_partial(self, genre_d):
        gid = genre_d.get("id")
        genre = self.dao.get_one(gid)

        if "name" in genre_d:
            genre.title = genre_d.get("name")

        self.dao.update(genre)

    def delete(self, rid):
        self.dao.delete(rid)

class IBaseRepository:
    def create(self, obj: object):
        raise NotImplementedError

    def get_by_id(self, id: int):
        raise NotImplementedError

    def update(self, obj: object, updated_data: dict):
        raise NotImplementedError

    def delete_by_id(self, id: int):
        raise NotImplementedError

    def find_all(self):
        raise NotImplementedError

from a1chemy.common import Tag
import itertools

class MongoTags(object):
    mongo_client = None
    db = None
    tags_collection = None

    def __init__(self, mongo_client) -> None:
        self.mongo_client = mongo_client
        self.db = mongo_client["a1chemy"]
        self.tags_collection = self.db['tags']

    def find(self, id=None):
        data = self.tags_collection.find_one({'id': id})
        return Tag(data)
    
    def find_children(self, id_list=None):
        query = {
            'parent': {
                '$in': id_list
            }
        }
        data = self.tags_collection.find(query)
        return dict((k, list(map(lambda x:Tag(x), values))) for k, values in itertools.groupby(data, key=lambda x:x['parent']))

    def delete(self, id=None):
        return self.tags_collection.delete_many({'id': id})

    def insert(self, tag: Tag = None):
        """
        insert tag, if exsits, delete first.
        """
        query = {
            'id': tag.id
        }
        new_value = {
            '$set': tag.to_dict()
        }
        return self.tags_collection.update_one(query, new_value, upsert=True)

import os
from dotenv import load_dotenv
from hashids import Hashids

load_dotenv()


class HashIdService():

    def encode_id(self, id):
        hashids = Hashids(salt=os.getenv('HASH_ID_SALT'),
                          min_length=15)
        return hashids.encode(id)

    def decode_id(self, hash_id):
        hashids = Hashids(salt=os.getenv('HASH_ID_SALT'),
                          min_length=15)
        id = hashids.decode(hash_id)
        if id:
            id = id[0]
        return id

    def encode_member_id(self, member_id):
        hashids = Hashids(salt=os.getenv('HASH_ID_SALT'),
                          min_length=8)
        return hashids.encode(member_id)

    def decode_member_id(self, member_hash_id):
        hashids = Hashids(salt=os.getenv('HASH_ID_SALT'),
                          min_length=8)
        return hashids.decode(member_hash_id)

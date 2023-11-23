
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
        return hashids.decode(hash_id)

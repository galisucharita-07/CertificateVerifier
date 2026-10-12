
import hashlib
import json
from datetime import datetime, timezone


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
        }

        encoded_data = json.dumps(
            block_data,
            sort_keys=True
        ).encode("utf-8")

        return hashlib.sha256(encoded_data).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(
            0,
            datetime.now(timezone.utc).isoformat(),
            {"message": "Genesis Block"},
            "0"
        )

    def get_latest_block(self):
        return self.chain[-1]

    def add_certificate(self, certificate_hash):
        latest_block = self.get_latest_block()

        new_block = Block(
            len(self.chain),
            datetime.now(timezone.utc).isoformat(),
            {"certificate_hash": certificate_hash},
            latest_block.hash
        )

        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for index in range(1, len(self.chain)):
            current = self.chain[index]
            previous = self.chain[index - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

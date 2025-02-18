from solana.keypair import Keypair

class Wallet:
    @staticmethod
    def generate():
        keypair = Keypair()
        return {
            'public_key': str(keypair.public_key),
            'private_key': keypair.seed.hex()
        }

    @staticmethod
    def from_private_key(private_key):
        keypair = Keypair.from_seed(bytes.fromhex(private_key))
        return {
            'public_key': str(keypair.public_key),
            'private_key': private_key
        }

    def to_dict(self):
        return self.__dict__
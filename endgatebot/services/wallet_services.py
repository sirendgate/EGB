import json
from utils.file_utils import load_json, save_json
from config.config import WALLETS_FILE, ADMIN_WALLETS_FILE

# Fix the import issue by checking both solana and solders modules
try:
    from solana.keypair import Keypair  # Older versions
except ImportError:
    from solders.keypair import Keypair  # Newer versions

class WalletService:
    def __init__(self, storage_file=WALLETS_FILE):
        self.storage_file = storage_file
        self.wallets = self._load_wallets()
        self.default_wallet_index = 0

    def _load_wallets(self):
        """Load wallets from storage."""
        return load_json(self.storage_file, default=[])

    def _save_wallets(self):
        """Save wallets to storage."""
        save_json(self.storage_file, self.wallets)

    def generate_wallet(self):
        """Generate a new wallet and save it to the admin_wallets.json file."""
        keypair = Keypair()
        wallet = {
            'public_key': str(keypair.pubkey()),
            'private_key': keypair.secret().hex()
        }
        self.wallets.append(wallet)
        self._save_wallets()
        return wallet

    def import_wallet(self, private_key):
        """Import a wallet using a private key."""
        keypair = Keypair.from_seed(bytes.fromhex(private_key))
        wallet = {
            'public_key': str(keypair.pubkey()),
            'private_key': private_key
        }
        self.wallets.append(wallet)
        self._save_wallets()
        return wallet

    def get_all_wallets(self):
        """Retrieve all stored wallets."""
        return self.wallets

    def get_default_wallet(self):
        """Retrieve the default wallet, if any exist."""
        if self.wallets:
            return self.wallets[self.default_wallet_index]
        return None

    def set_default_wallet(self, index):
        """Set the default wallet by index."""
        if 0 <= index < len(self.wallets):
            self.default_wallet_index = index

    def delete_wallet(self, index):
        """Delete a wallet by index."""
        if 0 <= index < len(self.wallets):
            self.wallets.pop(index)
            self._save_wallets()

    def distribute_tokens(self, total_amount, num_wallets):
        """Distribute tokens evenly across wallets."""
        if num_wallets <= 0:
            return []
        amount_per_wallet = total_amount / num_wallets
        return [amount_per_wallet] * num_wallets
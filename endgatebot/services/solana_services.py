# services/solana_services.py
import random
import time

# Handle Solana imports properly
try:
    from solana.publickey import PublicKey  # Older versions
    from solana.keypair import Keypair
    from solana.spl.token import Token, MintLayout
    from solana.rpc.api import Client
    from solana.transaction import Transaction
    from solana.system_program import TransferParams, transfer
except ImportError:
    try:
        from solders.pubkey import Pubkey as PublicKey  # Newer versions
        from solders.keypair import Keypair
        from solders.spl.token import Token, MintLayout
        from solders.rpc.api import Client
        from solders.transaction import Transaction
        from solders.system_program import TransferParams, transfer
    except ImportError as e:
        raise ImportError("Failed to import Solana libraries. Ensure 'solana' or 'solders' is installed.") from e

# Connect to Solana (mainnet by default)
client = Client("https://api.mainnet-beta.solana.com")

def transfer_sol(sender_private_key: str, recipient_public_key: str, amount: float) -> str:
    """Transfer SOL from one wallet to another."""
    try:
        sender_keypair = Keypair.from_secret_key(bytes.fromhex(sender_private_key))
        txn = Transaction().add(
            transfer(
                TransferParams(
                    from_pubkey=sender_keypair.pubkey(),
                    to_pubkey=PublicKey(recipient_public_key),
                    lamports=int(amount * 1e9)  # Convert SOL to lamports
                )
            )
        )
        response = client.send_transaction(txn, sender_keypair)
        return response.get("result", "Transaction Failed")
    except Exception as e:
        print(f"Error transferring SOL: {e}")
        return str(e)

def generate_volume(wallet: dict, token_address: str, min_amount: float, max_amount: float, num_transactions: int, delay_range: tuple):
    """Simulate transactions for volume generation."""
    for _ in range(num_transactions):
        amount = round(random.uniform(min_amount, max_amount), 4)
        transfer_sol(wallet['private_key'], token_address, amount)
        time.sleep(random.uniform(*delay_range))

def microbuys(wallet: dict, token_address: str, num_buys: int, max_amount: float, delay_range: tuple):
    """Simulate microbuy transactions."""
    for _ in range(num_buys):
        amount = round(random.uniform(0.001, max_amount), 4)
        transfer_sol(wallet['private_key'], token_address, amount)
        time.sleep(random.uniform(*delay_range))

def bumps(wallet: dict, token_address: str, num_bumps: int, min_amount: float, max_amount: float, delay_range: tuple):
    """Simulate large sporadic buy transactions."""
    for _ in range(num_bumps):
        amount = round(random.uniform(min_amount, max_amount), 4)
        transfer_sol(wallet['private_key'], token_address, amount)
        time.sleep(random.uniform(*delay_range))

def create_token(payer_private_key: str, name: str, symbol: str, decimals: int, initial_supply: int) -> str:
    """Create a new token on the Solana blockchain."""
    try:
        payer = Keypair.from_secret_key(bytes.fromhex(payer_private_key))
        mint = Keypair()

        # Get rent-exempt amount for mint
        rent = client.get_minimum_balance_for_rent_exemption(MintLayout.sizeof()).get('result', 0)

        txn = Transaction().add(
            transfer(
                TransferParams(
                    from_pubkey=payer.pubkey(),
                    to_pubkey=mint.pubkey(),
                    lamports=rent
                )
            )
        )

        # Initialize the mint
        txn.add(
            Token.create_mint(
                payer=payer.pubkey(),
                mint=mint.pubkey(),
                decimals=decimals,
                mint_authority=payer.pubkey(),
                freeze_authority=payer.pubkey()
            )
        )

        # Send the transaction
        response = client.send_transaction(txn, payer, mint)
        if response.get("error"):
            raise Exception(response["error"]["message"])

        return str(mint.pubkey())
    except Exception as e:
        print(f"Error creating token: {e}")
        return str(e)

# Example Usage
if __name__ == "__main__":
    wallet = {
        "private_key": "your_private_key_here",
        "public_key": "your_public_key_here"
    }
    
    # Test Token Creation
    new_token = create_token(wallet['private_key'], "MyToken", "MTK", 6, 1000000)
    print(f"New Token Created: {new_token}")
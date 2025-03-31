
# sol.py — Створення токена AUCTO без airdrop (у тебе вже є SOL)

from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID

# 🔧 Підключення до офіційного RPC (Devnet)
client = Client("https://api.devnet.solana.com")

# 🔑 Адреса твого гаманця Phantom
wallet_pubkey = Pubkey.from_string("CYBVbcQ1tMStcEbzcaQ8BZoUkirtJbQqEnEWavebEnQa")

# ⚠️ Створюємо тимчасового платника (payer)
payer = Keypair()
print("🧾 Temporary payer:", payer.pubkey())
print("‼️ Надішли трохи SOL (0.01+) на цю адресу, і потім перезапусти скрипт.")

input("⏳ Натисни Enter після того, як SOL надіслані на тимчасовий гаманець...")

# 🪙 Створення токена AUCTO
token = Token.create_mint(
    conn=client,
    payer=payer,
    mint_authority=payer.pubkey(),
    decimals=2,
    program_id=TOKEN_PROGRAM_ID,
)


print("✅ AUCTO Token Created!")
print("📦 Mint Address:", token.pubkey)

# 📥 Створюємо акаунт токена для гаманця користувача
user_token_account = token.create_account(wallet_pubkey)
print("📥 Token Account for User:", user_token_account)

# 🧾 Випускаємо 10 000 000 AUCTO
token.mint_to(
    dest=user_token_account,
    mint_authority=payer,
    amount=10_000_000 * 100  # decimals = 2 → множимо на 100
)

print("🎉 Успішно випущено 10 000 000 AUCTO на адресу користувача!")

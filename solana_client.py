# services/solana_client.py

from solana.rpc.api import Client
from config import RPC_URL

client = Client(RPC_URL)

# routes/token.py

from flask import Blueprint, jsonify
from config import AUCTO_MINT
from services.solana_client import client
from solders.pubkey import Pubkey
from solana.rpc.types import TokenAccountOpts

token_bp = Blueprint("token", __name__)

@token_bp.route("/check-token/<wallet>", methods=["GET"])
def check_token(wallet):
    try:
        owner_pubkey = Pubkey.from_string(wallet)
        mint_pubkey = Pubkey.from_string(AUCTO_MINT)

        # Створюємо об'єкт TokenAccountOpts для фільтрації за mint
        opts = TokenAccountOpts(mint=mint_pubkey)

        # Викликаємо метод з передачею об'єкта opts
        resp = client.get_token_accounts_by_owner_json_parsed(
            owner=owner_pubkey,
            opts=opts
        )

        balance = 0
        accounts = resp.value
        for acc in accounts:
            parsed_data = acc.account.data.parsed
            amount = parsed_data['info']['tokenAmount']['uiAmount']
            balance += amount

        return jsonify({
            "wallet": wallet,
            "balance": balance
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

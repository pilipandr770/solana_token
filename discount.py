from flask import Blueprint, jsonify
from config import AUCTO_MINT
from services.solana_client import client
from solders.pubkey import Pubkey  # Використовуємо PublicKey із solders.pubkey!
from solana.rpc.types import TokenAccountOpts

discount_bp = Blueprint("discount", __name__)

@discount_bp.route("/get-discount/<wallet>", methods=["GET"])
def get_discount(wallet):
    try:
        # Конвертуємо адресу користувача та mint у Pubkey
        owner_pubkey = Pubkey.from_string(wallet)
        mint_pubkey = Pubkey.from_string(AUCTO_MINT)

        # Створюємо об'єкт TokenAccountOpts для фільтрації за mint
        opts = TokenAccountOpts(mint=mint_pubkey)
        
        # Викликаємо метод, як у token.py
        resp = client.get_token_accounts_by_owner_json_parsed(owner=owner_pubkey, opts=opts)
        
        if resp.value is None:
            raise Exception("No token accounts found or invalid response from RPC.")

        balance = 0
        accounts = resp.value
        for acc in accounts:
            parsed_data = acc.account.data.parsed
            amount = parsed_data['info']['tokenAmount']['uiAmount']
            balance += amount

        # Розрахунок знижки за фіксованою шкалою
        if balance >= 10000:
            discount = 50
        elif balance >= 5000:
            discount = 40
        elif balance >= 1000:
            discount = 30
        elif balance >= 500:
            discount = 20
        elif balance >= 100:
            discount = 10
        elif balance >= 10:
            discount = 5
        elif balance >= 1:
            discount = 1
        else:
            discount = 0

        return jsonify({
            "wallet": wallet,
            "balance": balance,
            "discount_percent": discount
        })

    except Exception as e:
        import logging
        logging.exception("Error while retrieving discount")
        return jsonify({"error": f"Unexpected error: {repr(e)}"}), 400

from flask import Blueprint, request, jsonify
import threading

dao_bp = Blueprint("dao", __name__)

# Глобальне сховище для пропозицій
proposals = {}
proposal_id_counter = 1
lock = threading.Lock()

@dao_bp.route("/dao/proposals", methods=["GET"])
def list_proposals():
    """
    Повертає список усіх пропозицій.
    """
    with lock:
        return jsonify(list(proposals.values()))

@dao_bp.route("/dao/proposals", methods=["POST"])
def create_proposal():
    """
    Створює нову пропозицію.
    Очікує JSON з полями "title" та "description".
    """
    global proposal_id_counter
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    if not title or not description:
        return jsonify({"error": "Title and description are required."}), 400
    with lock:
        proposal_id = proposal_id_counter
        proposal_id_counter += 1
        proposals[proposal_id] = {
            "proposal_id": proposal_id,
            "title": title,
            "description": description,
            "votes": {"yes": 0, "no": 0},
            "voters": {}  # зберігаємо, які гаманці вже проголосували
        }
    return jsonify(proposals[proposal_id]), 201

@dao_bp.route("/dao/vote", methods=["POST"])
def vote():
    """
    Дозволяє проголосувати за пропозицію.
    Очікує JSON з полями:
      - proposal_id (int)
      - wallet (рядок)
      - vote (значення "yes" або "no")
    
    Для спрощення, кожен голос має вагу 1.
    Забороняємо повторне голосування з одного гаманця.
    """
    data = request.get_json()
    proposal_id = data.get("proposal_id")
    wallet = data.get("wallet")
    vote_choice = data.get("vote")  # має бути "yes" або "no"
    if proposal_id is None or not wallet or vote_choice not in ("yes", "no"):
        return jsonify({"error": "proposal_id, wallet, and vote ('yes' or 'no') are required."}), 400
    with lock:
        if proposal_id not in proposals:
            return jsonify({"error": "Proposal not found."}), 404
        proposal = proposals[proposal_id]
        if wallet in proposal["voters"]:
            return jsonify({"error": "This wallet has already voted on this proposal."}), 400
        proposal["votes"][vote_choice] += 1
        proposal["voters"][wallet] = vote_choice
    return jsonify(proposal)

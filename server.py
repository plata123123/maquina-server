from flask import Flask, request, jsonify
from flask_cors import CORS
import mercadopago

app = Flask(__name__)
CORS(app)

# ===== CONFIGURAÇÃO =====
ACCESS_TOKEN = "SEU_TOKEN_MERCADOPAGO"  # Coloque seu token aqui
sdk = mercadopago.SDK(ACCESS_TOKEN)

# ===== ROTA PARA CRIAR QR CODE =====
@app.route("/api/create_qr", methods=["POST"])
def create_qr():
    data = request.json
    amount = data.get("amount", 0)
    machine_id = data.get("machine_id", "unknown")

    preference_data = {
        "items": [{"title": f"Bebida {machine_id}", "quantity": 1, "unit_price": float(amount)}],
        "payment_methods": {"excluded_payment_types": [{"id": "ticket"}]},
        "binary_mode": True
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    return jsonify({
        "id": preference["id"], 
        "init_point": preference["init_point"]
    })

# ===== ROTA PARA CHECAR PAGAMENTO =====
@app.route("/api/payment_status", methods=["GET"])
def payment_status():
    payment_id = request.args.get("payment_id")
    if not payment_id:
        return jsonify({"status": "error", "message": "payment_id required"}), 400

    payment = sdk.payment().get(payment_id)
    status = payment["response"]["status"]
    return jsonify({"status": status})

# ===== INICIO =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

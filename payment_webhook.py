from flask import Flask, request, jsonify
import os
import hmac
import hashlib
import logging
import json
from config import PAID_USER_IDS, TOYYIBPAY_SECRET_KEY

app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def initialize_paid_user_ids_file():
    """Create or initialize the paid_user_ids.json file."""
    if not os.path.exists('paid_user_ids.json'):
        with open('paid_user_ids.json', 'w') as file:
            json.dump([], file)
            print("Created paid_user_ids.json with an empty list.")

initialize_paid_user_ids_file()

# Fungsi untuk memeriksa tandatangan (signature) untuk keselamatan
def verify_signature(params, secret_key):
    signature = params.pop('signature', '')
    payload = '&'.join(f'{key}={value}' for key, value in sorted(params.items()))
    expected_signature = hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected_signature)

@app.route('/payment_return', methods=['POST'])
def payment_return():
    try:
        data = request.form
        if not verify_signature(data, TOYYIBPAY_SECRET_KEY):
            logger.error("Invalid signature")
            return jsonify({"status": "error", "message": "Invalid signature"}), 400

        invoice_no = data.get('invoice_no')
        payment_status = data.get('status')

        if payment_status == "paid":
            user_id = int(invoice_no.split('-')[1])
            with open('paid_user_ids.json', 'r+') as file:
                paid_user_ids = json.load(file)
                if user_id not in paid_user_ids:
                    paid_user_ids.append(user_id)
                    file.seek(0)
                    json.dump(paid_user_ids, file)
            
            logger.info(f"Payment successful for user_id: {user_id}")
            return jsonify({"status": "success", "message": "Payment successful"}), 200
        else:
            logger.warning("Payment failed or cancelled")
            return jsonify({"status": "error", "message": "Payment failed or cancelled"}), 400
    except Exception as e:
        logger.error(f"Error handling payment return: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Ubah port jika diperlukan

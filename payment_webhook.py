from flask import Flask, request, jsonify
import os
from config import PAID_USER_IDS, TOYYIBPAY_SECRET_KEY
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Fungsi untuk memeriksa tandatangan (signature) untuk keselamatan
def verify_signature(params, secret_key):
    import hmac
    import hashlib
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
            PAID_USER_IDS.add(user_id)  # Menambah pengguna ke dalam senarai pengguna berbayar
            
            # Simpan kemaskini ke dalam fail atau pangkalan data
            with open('config.env', 'a') as file:
                file.write(f'PAID_USER_IDS={",".join(map(str, PAID_USER_IDS))}\n')
            
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

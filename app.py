
import hashlib
import json

from flask import Flask, render_template, request, jsonify
from blockchain import Blockchain

app = Flask(__name__)

# Create an in-memory blockchain
blockchain = Blockchain()

# Store certificate records for this demo.
# Certificate details are not stored directly in blockchain blocks.
certificates = {}


def calculate_certificate_hash(certificate_data):
    """Create a consistent SHA-256 hash for certificate details."""
    canonical_data = json.dumps(
        certificate_data,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":")
    )

    return hashlib.sha256(
        canonical_data.encode("utf-8")
    ).hexdigest()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register_certificate():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "certificate_id",
        "student_name",
        "course_name",
        "issuer_name",
        "issue_date"
    ]

    # Check that all required fields are provided
    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            return jsonify({
                "success": False,
                "message": f"Please provide {field.replace('_', ' ')}."
            }), 400

    # Remove unnecessary spaces from submitted values
    certificate_data = {
        field: data[field].strip()
        for field in required_fields
    }

    certificate_id = certificate_data["certificate_id"]

    # Prevent duplicate certificate IDs
    if certificate_id in certificates:
        return jsonify({
            "success": False,
            "message": "This certificate ID is already registered."
        }), 409

    # Generate a unique fingerprint of the certificate details
    certificate_hash = calculate_certificate_hash(certificate_data)

    # Add only the hash to the blockchain
    block = blockchain.add_certificate(certificate_hash)

    # Keep the record in memory for verification
    certificates[certificate_id] = {
        "details": certificate_data,
        "hash": certificate_hash,
        "block_index": block.index
    }

    return jsonify({
        "success": True,
        "message": "Certificate registered successfully!",
        "certificate_id": certificate_id,
        "certificate_hash": certificate_hash,
        "block_index": block.index
    }), 201


@app.route("/verify", methods=["POST"])
def verify_certificate():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "certificate_id",
        "student_name",
        "course_name",
        "issuer_name",
        "issue_date"
    ]

    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            return jsonify({
                "success": False,
                "message": f"Please provide {field.replace('_', ' ')}."
            }), 400

    certificate_data = {
        field: data[field].strip()
        for field in required_fields
    }

    certificate_id = certificate_data["certificate_id"]
    registered = certificates.get(certificate_id)

    if registered is None:
        return jsonify({
            "success": True,
            "valid": False,
            "message": "Certificate not found in the registry."
        })

    submitted_hash = calculate_certificate_hash(certificate_data)

    if submitted_hash != registered["hash"]:
        return jsonify({
            "success": True,
            "valid": False,
            "message": "Certificate details do not match the registered record."
        })

    return jsonify({
        "success": True,
        "valid": True,
        "message": "Certificate verified successfully!",
        "block_index": registered["block_index"],
        "certificate_hash": registered["hash"],
        "blockchain_valid": blockchain.is_chain_valid()
    })


@app.route("/chain", methods=["GET"])
def view_chain():
    blocks = []

    for block in blockchain.chain:
        blocks.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })

    return jsonify({
        "chain": blocks,
        "chain_valid": blockchain.is_chain_valid()
    })


if __name__ == "__main__":
    app.run(debug=True)

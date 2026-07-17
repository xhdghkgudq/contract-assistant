from flask import Blueprint, request, jsonify
import os

from services.file_parser import parse_file
from services.ai_service import analyze_contract

contract_bp = Blueprint("contract", __name__)

UPLOAD_FOLDER = "uploads"

@contract_bp.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    text = parse_file(path)
    ai_result = analyze_contract(text)

    return jsonify({
        "msg": "上传成功",
        "content": text[:200],
        "ai": ai_result
    })
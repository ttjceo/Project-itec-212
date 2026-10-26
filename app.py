from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv

from dotenv import PdfReader
from docx import Documenet 

import os
import io 
import csv


load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



@app.route("/")
def home():
    return send_from_directory(".", "Trivahub.html")


@app.route("/triva")
def triva():
    return send_from_directory(".", "Triva.html")


@app.route("/chat", methods=["POST"])
def chat():
    message = request.form.get("message", "").strip()
    uploaded_files = request.files.getlist("files")

    if not uploaded_files or uploaded_files[0].filename == "":
        return jsonify({
            "error": "File or folder is not present. Please provide a file or folder before asking Triva a question."
        }), 400

    if not message:
        return jsonify({
            "error": "Please enter a question for Triva"
        }), 400

    source_information = ""

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.filename
        try:
            file_contents = uploaded_file.read()
            file_text = file_contents.decode("utf-8")
        except UnicodeDecodeError:
            source_information += f"""
FILE NAME:
{file_name}

Triva could not read this file as plain text.
"""
            continue

        source_information += f"""
FILE NAME:
{file_name}

FILE CONTENTS:
{file_text}
"""

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions="""
You are Triva, an evidence-based AI assistant.

Important:
Only answer questions using information provided by the user's uploaded file or web link.
If the provided source does not contain enough information to answer the question, clearly say the source doesn't provide enough information.
Do not pretend that information came from the source when it did not.
Be clear and helpful.
""",
            input=f"""
Uploaded FILE INFORMATION:

{source_information}

User Question:
{message}
"""
        )
        return jsonify({"response": response.output_text})
    except Exception as error:
        print("OPENAI ERROR:", error)
        return jsonify({
            "error": "Triva had a problem generating a response."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
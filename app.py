from flask import Flask, request, jsonify, send_file
import os
import sqlite3
import shutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Constants
CHUNK_SIZE = 1024 * 1024  # 1 MB
NODES = ["node1", "node2", "node3", "node4"]

# Ensure node directories exist
for node in NODES:
    os.makedirs(node, exist_ok=True)

# Initialize SQLite database
conn = sqlite3.connect("metadata.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS metadata (
    file_name TEXT,
    chunk_id INTEGER,
    node TEXT,
    replica_node TEXT
)
""")
conn.commit()

# Hashing function to decide the storage node
def get_node(chunk_id):
    return NODES[chunk_id % len(NODES)]

@app.route("/")
def home():
    return "Welcome to the Distributed File Storage System!"

# Upload a file
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    print("Upload request received")  # Log for debugging
    if not file:
        return jsonify({"error": "No file provided"}), 400

    file_name = file.filename
    chunk_id = 0

    while chunk := file.read(CHUNK_SIZE):
        primary_node = get_node(chunk_id)
        replica_node = get_node((chunk_id + 1) % len(NODES))

        # Save chunk to primary node
        primary_path = os.path.join(primary_node, f"{file_name}_chunk{chunk_id}")
        with open(primary_path, "wb") as f:
            f.write(chunk)

        # Save chunk to replica node
        replica_path = os.path.join(replica_node, f"{file_name}_chunk{chunk_id}")
        with open(replica_path, "wb") as f:
            f.write(chunk)

        # Save metadata
        cursor.execute("""
        INSERT INTO metadata (file_name, chunk_id, node, replica_node)
        VALUES (?, ?, ?, ?)
        """, (file_name, chunk_id, primary_node, replica_node))
        conn.commit()

        chunk_id += 1

    return jsonify({"message": f"File '{file_name}' uploaded successfully."})

# Download a file
@app.route("/download/<file_name>", methods=["GET"])
def download_file(file_name):
    output_path = f"{file_name}_downloaded"
    cursor.execute("SELECT * FROM metadata WHERE file_name = ?", (file_name,))
    chunks = cursor.fetchall()

    if not chunks:
        return jsonify({"error": f"File '{file_name}' not found."}), 404

    with open(output_path, "wb") as output_file:
        for chunk in sorted(chunks, key=lambda x: x[1]):  # Sort by chunk_id
            primary_path = os.path.join(chunk[2], f"{file_name}_chunk{chunk[1]}")
            if os.path.exists(primary_path):
                with open(primary_path, "rb") as f:
                    output_file.write(f.read())
            else:
                replica_path = os.path.join(chunk[3], f"{file_name}_chunk{chunk[1]}")
                if os.path.exists(replica_path):
                    with open(replica_path, "rb") as f:
                        output_file.write(f.read())
                else:
                    return jsonify({"error": f"Missing chunk {chunk[1]} for file '{file_name}'."}), 500

    return send_file(output_path, as_attachment=True)

# Simulate node failure
@app.route("/simulate_failure/<node>", methods=["POST"])
def simulate_failure(node):
    if node not in NODES:
        return jsonify({"error": f"Invalid node: {node}"}), 400

    if os.path.exists(node):
        shutil.rmtree(node)
        return jsonify({"message": f"Node '{node}' has been deleted (failure simulated)."}), 200
    else:
        return jsonify({"error": f"Node '{node}' does not exist."}), 404

# Recover data from replicas
@app.route("/recover", methods=["POST"])
def recover_data():
    cursor.execute("SELECT DISTINCT file_name, chunk_id, node, replica_node FROM metadata")
    chunks = cursor.fetchall()

    for file_name, chunk_id, node, replica_node in chunks:
        primary_path = os.path.join(node, f"{file_name}_chunk{chunk_id}")
        replica_path = os.path.join(replica_node, f"{file_name}_chunk{chunk_id}")

        if not os.path.exists(primary_path) and os.path.exists(replica_path):
            os.makedirs(node, exist_ok=True)
            shutil.copy(replica_path, primary_path)

    return jsonify({"message": "Data recovery completed."})

# View metadata
@app.route("/metadata", methods=["GET"])
def view_metadata():
    cursor.execute("SELECT * FROM metadata")
    rows = cursor.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)

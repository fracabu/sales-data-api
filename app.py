from flask import Flask, jsonify, request
import random
from datetime import datetime, timedelta
import socket

# Inizializza l'app Flask
app = Flask(__name__)

# Funzione per generare dati di vendita
def generate_sales_data(num_records):
    data = []
    products = ["Laptop", "Smartphone", "Tablet", "Monitor", "Mouse", "Keyboard"]
    regions = ["North", "South", "East", "West"]
    
    for i in range(1, num_records + 1):
        date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        product = random.choice(products)
        region = random.choice(regions)
        sales = round(random.uniform(100, 1000), 2)
        profit = round(random.uniform(10, 200), 2)
        
        record = {
            "ID": i,
            "Date": date,
            "Product": product,
            "Region": region,
            "Sales": sales,
            "Profit": profit
        }
        data.append(record)
    
    return data

# Endpoint di test per verificare che l'app funzioni
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Sales Data API is running!"})

# Endpoint per generare i dati di vendita
@app.route('/generate-sales', methods=['GET'])
def generate_sales_endpoint():
    try:
        # Ottieni il parametro num_records dall'URL
        num_records = request.args.get('num_records', default=1000, type=int)
        
        # Controlla che il numero di record sia valido
        if num_records <= 0:
            return jsonify({"error": "Number of records must be greater than 0."}), 400
        if num_records > 100000:
            return jsonify({"error": "Max limit of 100,000 records exceeded."}), 400
        
        # Genera i dati di vendita
        data = generate_sales_data(num_records)
        return jsonify(data), 200
    except ValueError:
        return jsonify({"error": "Invalid value for num_records. Must be an integer."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Funzione per trovare una porta disponibile
def find_free_port(starting_port=5000):
    port = starting_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port))
                return port  # La porta è libera
            except OSError:
                port += 1  # Prova la prossima porta

# Avvio dell'app
if __name__ == "__main__":
    # Trova la porta disponibile solo una volta
    PORT = find_free_port(5000)
    print(f"Starting server on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT, debug=True)

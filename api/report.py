from flask import Flask, request, jsonify
import requests
import json
import os
from datetime import datetime
import sqlite3
import threading

app = Flask(__name__)

# Configurare din variabilele de mediu Vercel
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
SERVER_NAME = os.environ.get('SERVER_NAME', 'TRUST.CSPOWER.RO')
SERVER_WEBSITE = os.environ.get('SERVER_WEBSITE', 'cspower.ro')

# Lock pentru thread safety
db_lock = threading.Lock()

def init_database():
    """Inițializează baza de date SQLite"""
    with db_lock:
        conn = sqlite3.connect('/tmp/reports.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reporter_name TEXT NOT NULL,
                reporter_steam_id TEXT NOT NULL,
                reported_name TEXT NOT NULL,
                reported_steam_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                map_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                additional_info TEXT
            )
        ''')
        conn.commit()
        conn.close()

def save_report_to_db(reporter_name, reporter_steam_id, reported_name, reported_steam_id, 
                     reason, map_name, additional_info=""):
    """Salvează raportul în baza de date"""
    with db_lock:
        conn = sqlite3.connect('/tmp/reports.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO reports (reporter_name, reporter_steam_id, reported_name, 
                               reported_steam_id, reason, map_name, timestamp, 
                               additional_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (reporter_name, reporter_steam_id, reported_name, reported_steam_id,
              reason, map_name, datetime.now().isoformat(), additional_info))
        
        conn.commit()
        conn.close()

def send_discord_webhook(reporter_name, reporter_steam_id, reported_name, reported_steam_id, 
                       reason, map_name, additional_info=""):
    """Trimite raport prin webhook Discord"""
    
    if not DISCORD_WEBHOOK_URL:
        print("❌ DISCORD_WEBHOOK_URL nu este configurat!")
        return False
    
    # Creează embed-ul Discord
    embed = {
        "title": "📋 Report Automat",
        "color": 0xff4444,
        "fields": [
            {
                "name": "Report realizat de",
                "value": f"{reporter_name} ({reporter_steam_id})",
                "inline": False
            },
            {
                "name": "Utilizator reclamat", 
                "value": f"{reported_name} ({reported_steam_id})",
                "inline": False
            },
            {
                "name": "Motivul reclamatiei",
                "value": reason,
                "inline": False
            },
            {
                "name": "Data & Ora",
                "value": datetime.now().strftime("%d/%m/%Y - %H:%M"),
                "inline": False
            },
            {
                "name": "Harta curenta",
                "value": map_name,
                "inline": False
            }
        ],
        "footer": {
            "text": f"Report System for {SERVER_WEBSITE}"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    # Adaugă informații suplimentare dacă există
    if additional_info:
        embed["fields"].append({
            "name": "Informații suplimentare",
            "value": additional_info,
            "inline": False
        })
    
    # Trimite webhook-ul
    webhook_data = {
        "embeds": [embed]
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=webhook_data, timeout=10)
        if response.status_code == 204:
            print(f"✅ Raport trimis cu succes pentru {reported_name}")
            return True
        else:
            print(f"❌ Eroare la trimiterea raportului: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Eroare la trimiterea webhook-ului: {str(e)}")
        return False

@app.route('/api/report', methods=['POST'])
def receive_report():
    """Endpoint pentru primirea rapoartelor de la serverul CS 1.6"""
    
    try:
        data = request.get_json()
        
        # Validează datele primite
        required_fields = ['reporter_name', 'reporter_steam_id', 'reported_name', 'reported_steam_id', 'reason', 'map_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Câmpul {field} este obligatoriu'}), 400
        
        # Extrage datele
        reporter_name = data['reporter_name']
        reporter_steam_id = data['reporter_steam_id']
        reported_name = data['reported_name']
        reported_steam_id = data['reported_steam_id']
        reason = data['reason']
        map_name = data['map_name']
        additional_info = data.get('additional_info', '')
        
        # Salvează în baza de date
        save_report_to_db(
            reporter_name, reporter_steam_id, reported_name, reported_steam_id,
            reason, map_name, additional_info
        )
        
        # Trimite prin webhook Discord
        success = send_discord_webhook(
            reporter_name, reporter_steam_id, reported_name, reported_steam_id,
            reason, map_name, additional_info
        )
        
        if success:
            return jsonify({'status': 'success', 'message': 'Raport trimis cu succes'})
        else:
            return jsonify({'status': 'error', 'message': 'Eroare la trimiterea raportului'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Endpoint pentru obținerea rapoartelor"""
    
    try:
        limit = request.args.get('limit', 10, type=int)
        
        with db_lock:
            conn = sqlite3.connect('/tmp/reports.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT reporter_name, reporter_steam_id, reported_name, reported_steam_id,
                       reason, map_name, timestamp, additional_info
                FROM reports
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            reports = cursor.fetchall()
            conn.close()
        
        # Formatează rapoartele
        formatted_reports = []
        for report in reports:
            formatted_reports.append({
                'reporter_name': report[0],
                'reporter_steam_id': report[1],
                'reported_name': report[2],
                'reported_steam_id': report[3],
                'reason': report[4],
                'map_name': report[5],
                'timestamp': report[6],
                'additional_info': report[7]
            })
        
        return jsonify({'reports': formatted_reports})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Endpoint pentru verificarea statusului serverului"""
    return jsonify({
        'status': 'online',
        'discord_webhook_configured': bool(DISCORD_WEBHOOK_URL),
        'server_name': SERVER_NAME,
        'server_website': SERVER_WEBSITE,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def home():
    """Pagina principală"""
    return jsonify({
        'message': 'CS 1.6 Report System API',
        'version': '1.0',
        'endpoints': {
            'POST /api/report': 'Trimite raport',
            'GET /api/reports': 'Obține rapoarte',
            'GET /api/status': 'Status server'
        }
    })

# Inițializează baza de date la pornire
init_database()

# Pentru Vercel
def handler(request):
    return app(request)

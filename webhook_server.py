from flask import Flask, request, jsonify
import discord
import asyncio
import json
import sqlite3
from datetime import datetime
import threading
import requests

app = Flask(__name__)

# Configurare
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

config = load_config()

# Clasa pentru gestionarea webhook-urilor Discord
class DiscordWebhook:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    def send_report(self, reporter_name, reporter_steam_id, reported_name, reported_steam_id, 
                   reason, map_name, additional_info=""):
        """Trimite raport prin webhook Discord"""
        
        # Creează embed-ul
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
                "text": f"Report System for {config.get('server_website', 'your-server.com')}"
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
            response = requests.post(self.webhook_url, json=webhook_data)
            if response.status_code == 204:
                print(f"✅ Raport trimis cu succes pentru {reported_name}")
                return True
            else:
                print(f"❌ Eroare la trimiterea raportului: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Eroare la trimiterea webhook-ului: {str(e)}")
            return False

# Inițializează webhook-ul Discord
discord_webhook = None

def init_discord_webhook():
    global discord_webhook
    webhook_url = config.get('discord_webhook_url')
    if webhook_url:
        discord_webhook = DiscordWebhook(webhook_url)
        print("✅ Webhook Discord configurat")
    else:
        print("⚠️ Webhook Discord nu este configurat în config.json")

# Endpoint pentru primirea rapoartelor de la serverul CS 1.6
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
        if discord_webhook:
            success = discord_webhook.send_report(
                reporter_name, reporter_steam_id, reported_name, reported_steam_id,
                reason, map_name, additional_info
            )
            
            if success:
                return jsonify({'status': 'success', 'message': 'Raport trimis cu succes'})
            else:
                return jsonify({'status': 'error', 'message': 'Eroare la trimiterea raportului'})
        else:
            return jsonify({'status': 'error', 'message': 'Webhook Discord nu este configurat'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Endpoint pentru obținerea rapoartelor"""
    
    try:
        limit = request.args.get('limit', 10, type=int)
        
        conn = sqlite3.connect('reports.db')
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
        'discord_webhook_configured': discord_webhook is not None,
        'timestamp': datetime.now().isoformat()
    })

def save_report_to_db(reporter_name, reporter_steam_id, reported_name, reported_steam_id, 
                     reason, map_name, additional_info=""):
    """Salvează raportul în baza de date"""
    conn = sqlite3.connect('reports.db')
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

def init_database():
    """Inițializează baza de date"""
    conn = sqlite3.connect('reports.db')
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

if __name__ == '__main__':
    # Inițializează baza de date
    init_database()
    
    # Inițializează webhook-ul Discord
    init_discord_webhook()
    
    print("🚀 Server webhook pornit!")
    print("📡 Endpoint-uri disponibile:")
    print("   POST /api/report - Trimite raport")
    print("   GET  /api/reports - Obține rapoarte")
    print("   GET  /api/status - Status server")
    
    # Rulează serverul Flask
    app.run(host='0.0.0.0', port=5000, debug=True)

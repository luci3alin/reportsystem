#!/usr/bin/env python3
"""
Script pentru pornirea bot-ului Discord
Rulează acest script pentru a porni bot-ul
"""

import os
import sys
import subprocess

def check_requirements():
    """Verifică dacă dependențele sunt instalate"""
    try:
        import discord
        print("✅ discord.py este instalat")
        return True
    except ImportError:
        print("❌ discord.py nu este instalat!")
        print("Instalează cu: pip install discord.py")
        return False

def check_env_vars():
    """Verifică variabilele de mediu"""
    required_vars = ['DISCORD_BOT_TOKEN', 'REPORT_CHANNEL_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variabile de mediu lipsă: {', '.join(missing_vars)}")
        print("Configurează-le în fișierul .env sau în sistem")
        return False
    
    print("✅ Toate variabilele de mediu sunt configurate")
    return True

def start_bot():
    """Pornește bot-ul Discord"""
    print("🚀 Pornire bot Discord...")
    
    try:
        # Importă și rulează bot-ul
        from discord_bot import bot, BOT_TOKEN
        
        if not BOT_TOKEN:
            print("❌ DISCORD_BOT_TOKEN nu este configurat!")
            return False
        
        print(f"🤖 Pornire bot cu token: {BOT_TOKEN[:10]}...")
        bot.run(BOT_TOKEN)
        
    except Exception as e:
        print(f"❌ Eroare la pornirea bot-ului: {str(e)}")
        return False

def main():
    """Funcția principală"""
    print("🤖 CS Report System - Bot Discord")
    print("=" * 40)
    
    # Verifică dependențele
    if not check_requirements():
        sys.exit(1)
    
    # Verifică variabilele de mediu
    if not check_env_vars():
        sys.exit(1)
    
    # Pornește bot-ul
    start_bot()

if __name__ == "__main__":
    main()

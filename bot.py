import discord
from discord.ext import commands
import asyncio
import json
import sqlite3
from datetime import datetime
import os
from typing import Optional

# Configurare bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configurare baza de date
def init_database():
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
            channel_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Încarcă configurarea
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Configurare implicită
        default_config = {
            "bot_token": "YOUR_BOT_TOKEN_HERE",
            "report_channel_id": None,
            "admin_role_id": None,
            "server_name": "CS 1.6 Server",
            "server_website": "your-server.com"
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        return default_config

config = load_config()

@bot.event
async def on_ready():
    print(f'{bot.user} s-a conectat la Discord!')
    print(f'Bot ID: {bot.user.id}')
    init_database()

@bot.command(name='report')
async def create_report(ctx, reported_player: str, *, reason: str):
    """
    Creează un raport pentru un jucător
    Utilizare: !report "Nume Jucător" Motivul raportului
    """
    
    # Verifică dacă canalul este configurat
    if not config.get('report_channel_id'):
        await ctx.send("❌ Canalul pentru rapoarte nu este configurat! Contactează administratorul.")
        return
    
    # Extrage informațiile despre cel care raportează
    reporter_name = ctx.author.display_name
    reporter_steam_id = "STEAM_1:0:000000000"  # Poate fi modificat pentru a obține Steam ID real
    
    # Creează embed-ul pentru raport
    embed = discord.Embed(
        title="📋 Report",
        color=0xff4444,
        timestamp=datetime.now()
    )
    
    # Adaugă informațiile în embed
    embed.add_field(
        name="Report realizat de",
        value=f"{reporter_name} ({reporter_steam_id})",
        inline=False
    )
    
    embed.add_field(
        name="Utilizator reclamat",
        value=f"{reported_player}",
        inline=False
    )
    
    embed.add_field(
        name="Motivul reclamatiei",
        value=reason,
        inline=False
    )
    
    embed.add_field(
        name="Data & Ora",
        value=datetime.now().strftime("%d/%m/%Y - %H:%M"),
        inline=False
    )
    
    embed.add_field(
        name="Harta curenta",
        value="de_dust2",  # Poate fi modificat pentru a obține harta curentă
        inline=False
    )
    
    # Adaugă footer
    embed.set_footer(text=f"Report System for {config.get('server_website', 'your-server.com')}")
    
    # Trimite raportul în canalul configurat
    try:
        report_channel = bot.get_channel(config['report_channel_id'])
        if report_channel:
            message = await report_channel.send(embed=embed)
            
            # Salvează în baza de date
            save_report_to_db(
                reporter_name, reporter_steam_id, reported_player, "N/A",
                reason, "de_dust2", datetime.now().isoformat(),
                report_channel.id, message.id
            )
            
            await ctx.send(f"✅ Raportul a fost trimis în {report_channel.mention}")
        else:
            await ctx.send("❌ Canalul pentru rapoarte nu a fost găsit!")
    except Exception as e:
        await ctx.send(f"❌ Eroare la trimiterea raportului: {str(e)}")

@bot.command(name='setup')
@commands.has_permissions(administrator=True)
async def setup_bot(ctx, channel: discord.TextChannel):
    """
    Configurează canalul pentru rapoarte
    Utilizare: !setup #canal-raporturi
    """
    config['report_channel_id'] = channel.id
    
    # Salvează configurarea
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    await ctx.send(f"✅ Canalul {channel.mention} a fost setat pentru rapoarte!")

@bot.command(name='reports')
@commands.has_permissions(administrator=True)
async def list_reports(ctx, limit: int = 10):
    """
    Afișează ultimele rapoarte
    Utilizare: !reports [număr]
    """
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT reporter_name, reported_name, reason, timestamp
        FROM reports
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    reports = cursor.fetchall()
    conn.close()
    
    if not reports:
        await ctx.send("📋 Nu există rapoarte în baza de date.")
        return
    
    embed = discord.Embed(
        title="📋 Ultimele Rapoarte",
        color=0x00ff00
    )
    
    for i, (reporter, reported, reason, timestamp) in enumerate(reports, 1):
        embed.add_field(
            name=f"Raport #{i}",
            value=f"**De la:** {reporter}\n**Pentru:** {reported}\n**Motiv:** {reason}\n**Data:** {timestamp}",
            inline=False
        )
    
    await ctx.send(embed=embed)

def save_report_to_db(reporter_name, reporter_steam_id, reported_name, reported_steam_id, 
                     reason, map_name, timestamp, channel_id, message_id):
    """Salvează raportul în baza de date"""
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO reports (reporter_name, reporter_steam_id, reported_name, 
                           reported_steam_id, reason, map_name, timestamp, 
                           channel_id, message_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (reporter_name, reporter_steam_id, reported_name, reported_steam_id,
          reason, map_name, timestamp, channel_id, message_id))
    
    conn.commit()
    conn.close()

@bot.command(name='help_report')
async def help_report(ctx):
    """
    Afișează ajutorul pentru comenzi
    """
    embed = discord.Embed(
        title="🤖 Comenzi Bot Report System",
        description="Comenzile disponibile pentru sistemul de rapoarte:",
        color=0x0099ff
    )
    
    embed.add_field(
        name="!report \"Nume Jucător\" Motiv",
        value="Creează un raport pentru un jucător",
        inline=False
    )
    
    embed.add_field(
        name="!setup #canal",
        value="Configurează canalul pentru rapoarte (doar admin)",
        inline=False
    )
    
    embed.add_field(
        name="!reports [număr]",
        value="Afișează ultimele rapoarte (doar admin)",
        inline=False
    )
    
    embed.add_field(
        name="!help_report",
        value="Afișează acest mesaj de ajutor",
        inline=False
    )
    
    embed.set_footer(text=f"Report System for {config.get('server_website', 'your-server.com')}")
    
    await ctx.send(embed=embed)

# Rulare bot
if __name__ == "__main__":
    if config['bot_token'] == "YOUR_BOT_TOKEN_HERE":
        print("❌ Te rog să configurezi token-ul bot-ului în config.json!")
    else:
        bot.run(config['bot_token'])

import discord
from discord.ext import commands
import asyncio
import json
import os
from datetime import datetime
import requests

# Configurare bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configurare din variabilele de mediu
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
REPORT_CHANNEL_ID = os.environ.get('REPORT_CHANNEL_ID')
SERVER_NAME = os.environ.get('SERVER_NAME', 'TRUST.CSPOWER.RO')
SERVER_WEBSITE = os.environ.get('SERVER_WEBSITE', 'cspower.ro')

@bot.event
async def on_ready():
    print(f'{bot.user} s-a conectat la Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Server: {bot.guilds[0].name if bot.guilds else "N/A"}')

@bot.command(name='setup')
@commands.has_permissions(administrator=True)
async def setup_bot(ctx, channel: discord.TextChannel):
    """
    Configurează canalul pentru rapoarte
    Utilizare: !setup #canal-raporturi
    """
    global REPORT_CHANNEL_ID
    REPORT_CHANNEL_ID = str(channel.id)
    
    await ctx.send(f"✅ Canalul {channel.mention} a fost setat pentru rapoarte!")
    print(f"Canalul pentru rapoarte setat: {channel.name} ({channel.id})")

@bot.command(name='test_report')
@commands.has_permissions(administrator=True)
async def test_report(ctx):
    """
    Testează sistemul de rapoarte
    """
    if not REPORT_CHANNEL_ID:
        await ctx.send("❌ Canalul pentru rapoarte nu este configurat! Folosește `!setup #canal`")
        return
    
    # Creează un raport de test
    embed = discord.Embed(
        title="📋 Report de Test",
        color=0xff4444,
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name="Report realizat de",
        value="Test Admin (STEAM_1:0:123456)",
        inline=False
    )
    
    embed.add_field(
        name="Utilizator reclamat",
        value="Test Player (STEAM_1:0:789012)",
        inline=False
    )
    
    embed.add_field(
        name="Motivul reclamatiei",
        value="AIM HACK",
        inline=False
    )
    
    embed.add_field(
        name="Data & Ora",
        value=datetime.now().strftime("%d/%m/%Y - %H:%M"),
        inline=False
    )
    
    embed.add_field(
        name="Harta curenta",
        value="de_dust2",
        inline=False
    )
    
    embed.add_field(
        name="Informații suplimentare",
        value="Kills: 15 | Deaths: 3",
        inline=False
    )
    
    embed.set_footer(text=f"Report System for {SERVER_WEBSITE}")
    
    try:
        report_channel = bot.get_channel(int(REPORT_CHANNEL_ID))
        if report_channel:
            await report_channel.send(embed=embed)
            await ctx.send(f"✅ Raport de test trimis în {report_channel.mention}")
        else:
            await ctx.send("❌ Canalul pentru rapoarte nu a fost găsit!")
    except Exception as e:
        await ctx.send(f"❌ Eroare la trimiterea raportului: {str(e)}")

@bot.command(name='status')
async def bot_status(ctx):
    """
    Afișează statusul bot-ului
    """
    embed = discord.Embed(
        title="🤖 Status Bot Report System",
        color=0x00ff00
    )
    
    embed.add_field(
        name="Status",
        value="🟢 Online",
        inline=True
    )
    
    embed.add_field(
        name="Server",
        value=SERVER_NAME,
        inline=True
    )
    
    embed.add_field(
        name="Website",
        value=SERVER_WEBSITE,
        inline=True
    )
    
    if REPORT_CHANNEL_ID:
        report_channel = bot.get_channel(int(REPORT_CHANNEL_ID))
        if report_channel:
            embed.add_field(
                name="Canal Rapoarte",
                value=report_channel.mention,
                inline=False
            )
        else:
            embed.add_field(
                name="Canal Rapoarte",
                value="❌ Canalul nu a fost găsit!",
                inline=False
            )
    else:
        embed.add_field(
            name="Canal Rapoarte",
            value="❌ Nu este configurat! Folosește `!setup #canal`",
            inline=False
        )
    
    embed.set_footer(text=f"Bot pentru {SERVER_WEBSITE}")
    
    await ctx.send(embed=embed)

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
        name="!setup #canal",
        value="Configurează canalul pentru rapoarte (doar admin)",
        inline=False
    )
    
    embed.add_field(
        name="!test_report",
        value="Testează sistemul de rapoarte (doar admin)",
        inline=False
    )
    
    embed.add_field(
        name="!status",
        value="Afișează statusul bot-ului",
        inline=False
    )
    
    embed.add_field(
        name="!help_report",
        value="Afișează acest mesaj de ajutor",
        inline=False
    )
    
    embed.set_footer(text=f"Report System for {SERVER_WEBSITE}")
    
    await ctx.send(embed=embed)

# Funcție pentru primirea rapoartelor de la Vercel
async def receive_report_from_vercel(report_data):
    """
    Primește raport de la Vercel și îl trimite în Discord
    """
    if not REPORT_CHANNEL_ID:
        print("❌ Canalul pentru rapoarte nu este configurat!")
        return False
    
    try:
        # Creează embed-ul pentru raport
        embed = discord.Embed(
            title="📋 Report Automat",
            color=0xff4444,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="Report realizat de",
            value=f"{report_data['reporter_name']} ({report_data['reporter_steam_id']})",
            inline=False
        )
        
        embed.add_field(
            name="Utilizator reclamat",
            value=f"{report_data['reported_name']} ({report_data['reported_steam_id']})",
            inline=False
        )
        
        embed.add_field(
            name="Motivul reclamatiei",
            value=report_data['reason'],
            inline=False
        )
        
        embed.add_field(
            name="Data & Ora",
            value=datetime.now().strftime("%d/%m/%Y - %H:%M"),
            inline=False
        )
        
        embed.add_field(
            name="Harta curenta",
            value=report_data['map_name'],
            inline=False
        )
        
        if report_data.get('additional_info'):
            embed.add_field(
                name="Informații suplimentare",
                value=report_data['additional_info'],
                inline=False
            )
        
        embed.set_footer(text=f"Report System for {SERVER_WEBSITE}")
        
        # Trimite raportul în canalul configurat
        report_channel = bot.get_channel(int(REPORT_CHANNEL_ID))
        if report_channel:
            await report_channel.send(embed=embed)
            print(f"✅ Raport trimis cu succes pentru {report_data['reported_name']}")
            return True
        else:
            print("❌ Canalul pentru rapoarte nu a fost găsit!")
            return False
            
    except Exception as e:
        print(f"❌ Eroare la trimiterea raportului: {str(e)}")
        return False

# Rulare bot
if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ DISCORD_BOT_TOKEN nu este configurat!")
    else:
        bot.run(BOT_TOKEN)

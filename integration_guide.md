# 🔗 Ghid de Integrare - Server CS 1.6 cu Discord

## 🎯 Sistem Complet de Rapoarte Automate

Acest sistem permite ca rapoartele să fie trimise automat de pe serverul CS 1.6 către Discord, exact ca în exemplul tău!

## 🏗️ Arhitectura Sistemului

```
CS 1.6 Server → AMX Mod X Plugin → Webhook Server → Discord Bot
```

### Componente:

1. **AMX Mod X Plugin** - Rulează pe serverul CS 1.6
2. **Webhook Server** - Server Python care primește rapoartele
3. **Discord Bot** - Trimite rapoartele în Discord
4. **Baza de Date** - Stochează toate rapoartele

## 🚀 Instalare Pas cu Pas

### 1. Configurarea Webhook Server-ului

```bash
# Instalează dependențele
pip install flask requests

# Rulează serverul webhook
python webhook_server.py
```

Serverul va rula pe `http://localhost:5000` și va primi rapoartele de la serverul CS 1.6.

### 2. Configurarea Discord Webhook-ului

1. **Creează un Webhook în Discord**:
   - Mergi la canalul unde vrei rapoartele
   - Click pe ⚙️ (Settings) → Integrations → Webhooks
   - Click "Create Webhook"
   - Copiază URL-ul webhook-ului

2. **Configurează config.json**:
```json
{
    "discord_webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL",
    "webhook_server_port": 5000,
    "enable_auto_reports": true
}
```

### 3. Instalarea Plugin-ului pe Serverul CS 1.6

1. **Copiază fișierele**:
   - `amx_report_plugin.sma` → `addons/amxmodx/scripting/`
   - `report_config.ini` → `addons/amxmodx/configs/`

2. **Compilează plugin-ul**:
```bash
# În folderul scripting
./compile amx_report_plugin.sma
```

3. **Activează plugin-ul**:
```ini
; În addons/amxmodx/configs/plugins.ini
amx_report_plugin.amxx
```

4. **Configurează report_config.ini**:
```ini
webhook_url = http://YOUR_SERVER_IP:5000/api/report
server_name = CS 1.6 Server
server_website = your-server.com
```

## 🎮 Utilizare pe Server

### Pentru Jucători:

1. **Raportare prin meniu**:
   ```
   /report
   ```
   - Selectează jucătorul
   - Alege motivul
   - Raportul se trimite automat!

2. **Motive disponibile**:
   - AIM HACK
   - WALL HACK  
   - SPEED HACK
   - BUNNY HOP
   - TEAM KILL
   - SPAM
   - INSULT
   - ALT MOTIV

### Pentru Admini:

```
amx_report <nume_jucator> <motiv>
```

## 📡 API Endpoints

Serverul webhook oferă următoarele endpoint-uri:

### `POST /api/report`
Trimite un raport nou.

**Exemplu de request**:
```json
{
    "reporter_name": "CSKA SOFIA HOOLIGANS",
    "reporter_steam_id": "STEAM_1:0:370053838",
    "reported_name": "CSDOWN | Original player",
    "reported_steam_id": "STEAM_1:0:670875696",
    "reason": "AIM HACK",
    "map_name": "de_dust2",
    "additional_info": "Kills: 15 | Deaths: 3 | Ping: 45ms"
}
```

### `GET /api/reports`
Obține ultimele rapoarte.

### `GET /api/status`
Verifică statusul serverului.

## 🔧 Configurare Avansată

### Personalizarea Rapoartelor

Editează `webhook_server.py` pentru a modifica:
- Aspectul embed-urilor
- Informațiile afișate
- Culorile și formatarea

### Adăugarea de Funcționalități

1. **Rapoarte cu Dovezi**:
   - Adaugă suport pentru imagini
   - Integrează cu sistemul de demo-uri

2. **Sistem de Avertismente**:
   - Conectează cu baza de date
   - Implementează escaladarea

3. **Notificări pentru Admini**:
   - Trimite ping-uri pentru rapoarte importante
   - Categorizează rapoartele

## 🐛 Rezolvarea Problemelor

### Rapoartele nu se trimit

1. **Verifică conexiunea**:
   ```bash
   curl http://localhost:5000/api/status
   ```

2. **Verifică log-urile**:
   - Server webhook: console
   - Server CS 1.6: addons/amxmodx/logs/

3. **Verifică configurarea**:
   - URL-ul webhook-ului
   - Permisiunile de rețea
   - Firewall-ul

### Plugin-ul nu se încarcă

1. **Verifică compilarea**:
   ```bash
   ./compile amx_report_plugin.sma
   ```

2. **Verifică plugins.ini**:
   ```ini
   amx_report_plugin.amxx
   ```

3. **Verifică log-urile**:
   - addons/amxmodx/logs/error_YYYYMMDD.log

## 📊 Monitorizare

### Verificarea Statusului

```bash
# Status server webhook
curl http://localhost:5000/api/status

# Ultimele rapoarte
curl http://localhost:5000/api/reports?limit=5
```

### Log-uri și Debugging

1. **Server webhook**: Console output
2. **Server CS 1.6**: `addons/amxmodx/logs/`
3. **Discord**: Audit log-uri

## 🎯 Exemplu Complet de Flux

1. **Jucătorul** folosește `/report` pe server
2. **Plugin-ul AMX** trimite datele la webhook server
3. **Webhook server** salvează în baza de date
4. **Discord webhook** trimite embed-ul în Discord
5. **Adminii** văd raportul instant în Discord

## 🚀 Următorii Pași

După configurarea de bază:

1. **Personalizează aspectul** rapoartelor
2. **Adaugă funcționalități** noi
3. **Integrează cu alte sisteme**
4. **Creează dashboard** web pentru administrare

---

**Sistem complet funcțional pentru rapoarte automate! 🎮🤖**

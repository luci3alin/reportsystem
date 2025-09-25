# 🤖 CS Report System pentru TRUST.CSPOWER.RO

Sistem complet de rapoarte automate pentru serverul CS 1.6 TRUST.CSPOWER.RO, integrat cu Discord.

## 📋 Informații Server

- **Server CS 1.6:** TRUST.CSPOWER.RO
- **IP:** 51.38.117.113:27015
- **Website:** cspower.ro
- **Discord Server ID:** 1418768496795582657
- **User ID:** 432658420428963841

## 🎯 Funcționalități

- 📋 **Rapoarte automate** de pe serverul CS 1.6
- 🤖 **Integrare Discord** cu embed-uri frumoase
- 🗄️ **Baza de date** pentru stocarea rapoartelor
- ⚙️ **Configurare ușoară** prin Vercel
- 👮 **Comenzi admin** pentru gestionarea rapoartelor

## 🚀 Deployment pe Vercel

### 1. Creează Repository GitHub NOU

```bash
# Creează un folder nou
mkdir cs-report-system-trust
cd cs-report-system-trust

# Copiază toate fișierele
git init
git add .
git commit -m "CS Report System for TRUST.CSPOWER.RO"
git remote add origin https://github.com/luci3alin/cs-report-system-trust.git
git push -u origin main
```

### 2. Deploy pe Vercel

1. **Mergi la [vercel.com](https://vercel.com)**
2. **Click "New Project"**
3. **Selectează repository-ul NOU** (cs-report-system-trust)
4. **Numele proiectului:** `cs-report-system-trust`

### 3. Configurează Environment Variables

```
DISCORD_WEBHOOK_URL = [URL-ul webhook-ului Discord]
SERVER_NAME = TRUST.CSPOWER.RO
SERVER_WEBSITE = cspower.ro
```

### 4. Creează Discord Webhook

1. **Mergi pe serverul Discord** (ID: 1418768496795582657)
2. **Creează un canal nou** pentru rapoarte (ex: #reports)
3. **Click ⚙️** pe canal → Integrations → Webhooks
4. **Click "Create Webhook"**
5. **Copiază URL-ul** și adaugă-l în Vercel Environment Variables

## 🔧 Configurarea Serverului CS 1.6

### 1. Instalare Plugin

```bash
# Pe serverul 51.38.117.113:27015
# 1. Instalează plugin-ul HTTP pentru AMX Mod X
# 2. Compilează amx_report_plugin.sma
# 3. Copiază amx_report_plugin.amxx în plugins/
# 4. Activează în plugins.ini
# 5. Restart serverul
```

### 2. Configurare report_config.ini

```ini
; Configurare pentru TRUST.CSPOWER.RO
webhook_url = https://cs-report-system-trust.vercel.app
server_name = TRUST.CSPOWER.RO
server_website = cspower.ro
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

## 🧪 Testarea Sistemului

### 1. Testează API-ul Vercel

```bash
# Testează status-ul
curl https://cs-report-system-trust.vercel.app/api/status
```

### 2. Testează pe Serverul CS 1.6

1. **Conectează-te la server** (51.38.117.113:27015)
2. **Folosește comanda:**
   ```
   /report
   ```
3. **Selectează un jucător și motivul**
4. **Verifică în Discord** că raportul apare în canalul #reports

## 📊 Monitorizarea

### 1. Vercel Dashboard
- **Mergi la proiectul NOU** (cs-report-system-trust)
- **Vezi log-urile** în Functions → Logs
- **Monitorizează erorile** în real-time

### 2. Discord
- **Verifică canalul #reports**
- **Testează cu rapoarte de test**

## 🐛 Rezolvarea Problemelor

### 1. Rapoartele nu se trimit

**Verifică:**
- URL-ul Vercel este corect în report_config.ini
- Discord webhook-ul este configurat în Environment Variables
- Plugin-ul HTTP este instalat pe server
- Log-urile Vercel pentru erori

### 2. Plugin-ul nu se încarcă

**Verifică:**
- Plugin-ul HTTP este instalat
- Compilarea a fost făcută corect
- plugins.ini conține plugin-ul
- Restart serverul după instalare

### 3. Erori de conexiune

**Verifică:**
- Firewall-ul serverului permite conexiuni HTTPS
- URL-ul Vercel este accesibil din server
- Conectivitatea la internet

## 📈 Următorii Pași

După deployment:

1. **Testează sistemul** complet cu rapoarte reale
2. **Configurează notificări** pentru admini
3. **Adaugă funcționalități** noi (ex: rapoarte cu dovezi)
4. **Monitorizează performanța** și traficul

## 🎯 Rezultatul Final

Ai un sistem complet de rapoarte care:
- ✅ **Funcționează pe Vercel** (proiect separat)
- ✅ **Se conectează la TRUST.CSPOWER.RO**
- ✅ **Trimite rapoarte în Discord** instant
- ✅ **Costă 0 lei** (gratuit pe Vercel)
- ✅ **Se scalează automat** cu traficul

---

**Sistem complet pentru TRUST.CSPOWER.RO! 🎮🚀**

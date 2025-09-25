# 🚀 Ghid de Deployment pe Vercel - CS Report System

## 🎯 Avantajele Vercel

- ✅ **Gratuit** pentru proiecte mici
- ✅ **Deployment automat** cu Git
- ✅ **HTTPS inclus** 
- ✅ **Scalare automată**
- ✅ **Nu necesită server dedicat**

## 📋 Pași pentru Deployment

### 1. Pregătirea Proiectului

```bash
# Structura proiectului
├── api/
│   └── report.py          # API endpoint-ul principal
├── vercel.json            # Configurarea Vercel
├── requirements.txt       # Dependențele Python
└── README.md
```

### 2. Crearea Contului Vercel

1. **Mergi la [vercel.com](https://vercel.com)**
2. **Loghează-te cu GitHub** (recomandat)
3. **Creează un cont nou**

### 3. Configurarea Variabilelor de Mediu

În dashboard-ul Vercel, mergi la **Settings** → **Environment Variables** și adaugă:

```
DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/YOUR_WEBHOOK_URL
SERVER_NAME = CS 1.6 Server
SERVER_WEBSITE = your-server.com
```

### 4. Deployment prin GitHub

1. **Creează un repository GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/username/cs-report-system.git
   git push -u origin main
   ```

2. **Conectează cu Vercel**:
   - Mergi la Vercel Dashboard
   - Click "New Project"
   - Selectează repository-ul GitHub
   - Click "Deploy"

### 5. Configurarea Discord Webhook

1. **Creează webhook-ul în Discord**:
   - Mergi la canalul unde vrei rapoartele
   - Click ⚙️ → Integrations → Webhooks
   - Click "Create Webhook"
   - Copiază URL-ul

2. **Adaugă în Vercel**:
   - Settings → Environment Variables
   - Adaugă `DISCORD_WEBHOOK_URL` cu URL-ul webhook-ului

## 🔧 Configurarea Serverului CS 1.6

### 1. Instalarea Plugin-ului HTTP

Pentru ca plugin-ul să funcționeze, ai nevoie de plugin-ul HTTP pentru AMX Mod X:

1. **Descarcă plugin-ul HTTP**:
   - Mergi la [AMX Mod X HTTP Plugin](https://github.com/Arkshine/HttpClient)
   - Descarcă `http_client.amxx`

2. **Instalează plugin-ul**:
   ```bash
   # Copiază în folderul plugins
   cp http_client.amxx addons/amxmodx/plugins/
   
   # Activează în plugins.ini
   echo "http_client.amxx" >> addons/amxmodx/configs/plugins.ini
   ```

### 2. Configurarea Plugin-ului

Editează `report_config.ini`:

```ini
; URL-ul Vercel (înlocuiește cu URL-ul tău)
webhook_url = https://your-app-name.vercel.app

; Numele serverului
server_name = CS 1.6 Server

; Website-ul serverului
server_website = your-server.com
```

### 3. Compilarea și Instalarea

```bash
# Compilează plugin-ul
./compile amx_report_plugin.sma

# Copiază în plugins
cp amx_report_plugin.amxx addons/amxmodx/plugins/

# Activează în plugins.ini
echo "amx_report_plugin.amxx" >> addons/amxmodx/configs/plugins.ini
```

## 🧪 Testarea Sistemului

### 1. Testează API-ul Vercel

```bash
# Testează status-ul
curl https://your-app-name.vercel.app/api/status

# Testează un raport
curl -X POST https://your-app-name.vercel.app/api/report \
  -H "Content-Type: application/json" \
  -d '{
    "reporter_name": "Test Player",
    "reporter_steam_id": "STEAM_1:0:123456",
    "reported_name": "Suspicious Player",
    "reported_steam_id": "STEAM_1:0:789012",
    "reason": "AIM HACK",
    "map_name": "de_dust2",
    "additional_info": "Test report"
  }'
```

### 2. Testează pe Serverul CS 1.6

1. **Conectează-te la server**
2. **Folosește comanda**:
   ```
   /report
   ```
3. **Selectează un jucător și motivul**
4. **Verifică în Discord** că raportul apare

## 📊 Monitorizarea

### 1. Log-uri Vercel

- Mergi la **Functions** în dashboard-ul Vercel
- Vezi log-urile în timp real
- Monitorizează erorile

### 2. Log-uri Discord

- Verifică canalul Discord pentru rapoarte
- Testează cu rapoarte de test

### 3. API Status

```bash
# Verifică status-ul
curl https://your-app-name.vercel.app/api/status
```

## 🔧 Configurare Avansată

### 1. Domeniu Personalizat

1. **Cumpără un domeniu** (opțional)
2. **Configurează în Vercel**:
   - Settings → Domains
   - Adaugă domeniul tău
   - Configurează DNS-ul

### 2. Variabile de Mediu Avansate

```bash
# Adaugă în Vercel
DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/...
SERVER_NAME = CS 1.6 Server
SERVER_WEBSITE = your-server.com
DEBUG_MODE = 1
MAX_REPORTS_PER_HOUR = 10
```

### 3. Rate Limiting

Editează `api/report.py` pentru a adăuga rate limiting:

```python
# Adaugă rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per hour"]
)

@app.route('/api/report', methods=['POST'])
@limiter.limit("5 per minute")
def receive_report():
    # Codul existent
```

## 🐛 Rezolvarea Problemelor

### 1. Rapoartele nu se trimit

**Verifică**:
- URL-ul Vercel este corect
- Discord webhook-ul este configurat
- Plugin-ul HTTP este instalat
- Log-urile Vercel pentru erori

### 2. Plugin-ul nu se încarcă

**Verifică**:
- Plugin-ul HTTP este instalat
- Compilarea a fost făcută corect
- plugins.ini conține plugin-ul

### 3. Erori de conexiune

**Verifică**:
- Firewall-ul serverului
- Conectivitatea la internet
- URL-ul Vercel este accesibil

## 📈 Optimizări

### 1. Cache pentru Rapoarte

```python
# Adaugă cache pentru rapoarte frecvente
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.memoize(timeout=300)
def get_recent_reports(limit=10):
    # Codul existent
```

### 2. Database Externă

Pentru proiecte mari, folosește o bază de date externă:

```python
# Folosește PostgreSQL sau MySQL
import psycopg2

# Configurează conexiunea
DATABASE_URL = os.environ.get('DATABASE_URL')
```

## 🎯 Următorii Pași

După deployment:

1. **Testează sistemul** complet
2. **Configurează notificări** pentru admini
3. **Adaugă funcționalități** noi
4. **Monitorizează performanța**

---

**Sistem complet pe Vercel - gratuit și scalabil! 🚀**

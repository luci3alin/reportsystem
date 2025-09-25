# 🤖 Discord Report System Bot pentru CS 1.6

Un bot Discord modern pentru gestionarea rapoartelor de jucători pe servere CS 1.6, similar cu sistemul observat pe respawn.gamelife.ro.

## ✨ Funcționalități

- 📋 **Rapoarte automate** cu embed-uri frumoase
- 🗄️ **Baza de date SQLite** pentru stocarea rapoartelor
- ⚙️ **Configurare ușoară** prin fișiere JSON
- 👮 **Comenzi admin** pentru gestionarea rapoartelor
- 🎨 **Design modern** cu embed-uri Discord

## 🚀 Instalare și Configurare

### 1. Instalare Dependențe

```bash
pip install -r requirements.txt
```

### 2. Configurare Bot Discord

1. Mergi la [Discord Developer Portal](https://discord.com/developers/applications)
2. Creează o aplicație nouă
3. Mergi la secțiunea "Bot" și creează un bot
4. Copiază token-ul bot-ului
5. Editează `config.json` și pune token-ul:

```json
{
    "bot_token": "TOKEN_UL_TAU_AICI",
    "report_channel_id": null,
    "admin_role_id": null,
    "server_name": "CS 1.6 Server",
    "server_website": "your-server.com"
}
```

### 3. Invitare Bot pe Server

1. Mergi la secțiunea "OAuth2" > "URL Generator"
2. Selectează "bot" în scope-uri
3. Selectează permisiunile necesare:
   - Send Messages
   - Embed Links
   - Read Message History
   - Use Slash Commands
4. Folosește URL-ul generat pentru a invita bot-ul

## 📖 Comenzi Disponibile

### Pentru Toți Utilizatorii

- `!report "Nume Jucător" Motivul raportului` - Creează un raport
- `!help_report` - Afișează ajutorul

### Pentru Administratori

- `!setup #canal-raporturi` - Configurează canalul pentru rapoarte
- `!reports [număr]` - Afișează ultimele rapoarte

## 🎯 Exemplu de Utilizare

1. **Configurare inițială** (doar o dată):
   ```
   !setup #raporturi
   ```

2. **Creare raport**:
   ```
   !report "CSKA SOFIA HOOLIGANS" AIM HACK
   ```

3. **Vizualizare rapoarte** (admin):
   ```
   !reports 5
   ```

## 📁 Structura Fișierelor

```
├── bot.py              # Codul principal al bot-ului
├── config.json         # Configurarea bot-ului
├── requirements.txt     # Dependențele Python
├── README.md           # Documentația
└── reports.db          # Baza de date (se creează automat)
```

## 🔧 Personalizare

### Modificarea Aspectului Rapoartelor

Editează funcția `create_report` din `bot.py` pentru a personaliza:
- Culorile embed-urilor
- Informațiile afișate
- Formatul datelor

### Integrare cu Server CS 1.6

Pentru a obține informații reale despre:
- Steam ID-urile jucătorilor
- Harta curentă
- Timpul exact

Poți integra bot-ul cu plugin-uri AMX Mod X sau SourceMod.

## 🛠️ Dezvoltare Avansată

### Adăugarea de Funcționalități

1. **Rapoarte cu Dovezi**:
   ```python
   @bot.command(name='report_with_evidence')
   async def report_with_evidence(ctx, reported_player: str, reason: str):
       # Logica pentru rapoarte cu imagini/video
   ```

2. **Sistem de Avertismente**:
   ```python
   # Adaugă tabel pentru avertismente
   # Implementează comenzi pentru avertismente
   ```

3. **Integrare Web**:
   ```python
   # API REST pentru a accesa rapoartele din web
   ```

## 📞 Suport

Pentru probleme sau întrebări:
1. Verifică că toate dependențele sunt instalate
2. Asigură-te că token-ul bot-ului este corect
3. Verifică că bot-ul are permisiunile necesare
4. Contactează dezvoltatorul pentru suport tehnic

## 📄 Licență

Acest proiect este open source și poate fi modificat conform nevoilor tale.

---

**Creat cu ❤️ pentru comunitatea CS 1.6**

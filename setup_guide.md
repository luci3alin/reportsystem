# 🚀 Ghid de Configurare - Discord Report Bot

## 📋 Pași pentru Configurare Completă

### 1. Pregătirea Mediului

```bash
# Instalează Python (dacă nu este deja instalat)
# Descarcă de la: https://python.org

# Verifică instalarea
python --version
pip --version
```

### 2. Instalarea Dependențelor

```bash
# Navighează la folderul proiectului
cd "D:\Discord bot cs TRUST"

# Instalează dependențele
pip install discord.py
```

### 3. Crearea Bot-ului pe Discord

1. **Mergi la Discord Developer Portal**:
   - Accesează: https://discord.com/developers/applications
   - Loghează-te cu contul Discord

2. **Creează o Aplicație Nouă**:
   - Apasă "New Application"
   - Dă un nume (ex: "CS Report Bot")
   - Apasă "Create"

3. **Configurează Bot-ul**:
   - Mergi la secțiunea "Bot" din meniul stâng
   - Apasă "Add Bot"
   - Copiază "Token" (va fi nevoie mai târziu)
   - Activează "Message Content Intent" dacă este necesar

4. **Configurează OAuth2**:
   - Mergi la "OAuth2" > "URL Generator"
   - Selectează "bot" în "Scopes"
   - Selectează permisiunile:
     - ✅ Send Messages
     - ✅ Embed Links
     - ✅ Read Message History
     - ✅ Use Slash Commands
     - ✅ Manage Messages (opțional)
   - Copiază URL-ul generat

### 4. Configurarea Bot-ului

1. **Editează config.json**:
```json
{
    "bot_token": "TOKEN_UL_COPIAT_MAI_SUS",
    "report_channel_id": null,
    "admin_role_id": null,
    "server_name": "CS 1.6 Server",
    "server_website": "your-server.com"
}
```

2. **Invită Bot-ul pe Server**:
   - Folosește URL-ul generat la pasul 3.4
   - Selectează serverul tău
   - Autorizează bot-ul

### 5. Rularea Bot-ului

```bash
# Rulează bot-ul
python bot.py
```

Dacă totul este configurat corect, vei vedea:
```
CS Report Bot#1234 s-a conectat la Discord!
Bot ID: 123456789012345678
```

### 6. Configurarea Canalului pentru Rapoarte

Pe serverul Discord, rulează:
```
!setup #canal-raporturi
```

Înlocuiește `#canal-raporturi` cu canalul dorit.

### 7. Testarea Bot-ului

```
!help_report
```

Ar trebui să vezi un mesaj cu toate comenzile disponibile.

## 🔧 Configurări Avansate

### Personalizarea Mesajelor

Editează `bot.py` pentru a schimba:
- Textul embed-urilor
- Culorile
- Informațiile afișate

### Adăugarea de Roluri

În `config.json`, adaugă:
```json
{
    "admin_role_id": 123456789012345678
}
```

### Integrare cu Server CS 1.6

Pentru a obține informații reale despre jucători:

1. **Instalează plugin-uri AMX Mod X** pe server
2. **Configurează webhook-uri** pentru a trimite date la bot
3. **Modifică bot.py** pentru a primi datele

## 🐛 Rezolvarea Problemelor

### Bot-ul nu se conectează
- ✅ Verifică token-ul în config.json
- ✅ Asigură-te că bot-ul este invitat pe server
- ✅ Verifică conexiunea la internet

### Comenzile nu funcționează
- ✅ Verifică că bot-ul are permisiunile necesare
- ✅ Asigură-te că prefixul este corect (!)
- ✅ Verifică că canalul permite bot-urilor să scrie

### Rapoartele nu se salvează
- ✅ Verifică că fișierul reports.db se creează
- ✅ Asigură-te că bot-ul are permisiuni de scriere în folder

## 📞 Suport Tehnic

Dacă întâmpini probleme:

1. **Verifică log-urile** în consolă
2. **Testează comenzile** una câte una
3. **Verifică configurarea** pas cu pas
4. **Contactează dezvoltatorul** cu detalii despre problema

## 🎯 Următorii Pași

După configurarea de bază, poți:

1. **Personaliza aspectul** rapoartelor
2. **Adăuga funcționalități** noi
3. **Integra cu serverul** CS 1.6
4. **Crea un dashboard** web pentru administrare

---

**Succes cu bot-ul tău! 🚀**

# 🤖 Ghid Setup Bot Discord pentru CS Report System

## 🎯 **Ce Trebuie să Faci:**

### **1. Creează Bot Discord**

1. **Mergi la [Discord Developer Portal](https://discord.com/developers/applications)**
2. **Click "New Application"**
3. **Numele:** `CS Report Bot`
4. **Click "Create"**

### **2. Configurează Bot-ul**

1. **Mergi la secțiunea "Bot"** (din meniul stâng)
2. **Click "Add Bot"**
3. **Copiază "Token"** (va fi nevoie mai târziu)
4. **Activează "Message Content Intent"** dacă este necesar

### **3. Invită Bot-ul pe Server**

1. **Mergi la secțiunea "OAuth2" → "URL Generator"**
2. **Selectează "bot" în Scopes**
3. **Selectează permisiunile:**
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Use Slash Commands
   - ✅ Manage Messages (opțional)
4. **Copiază URL-ul generat**
5. **Folosește URL-ul pentru a invita bot-ul pe serverul Discord**

### **4. Configurează Environment Variables în Vercel**

În proiectul Vercel, adaugă:

```
DISCORD_BOT_TOKEN = [TOKEN-ul bot-ului]
REPORT_CHANNEL_ID = [ID-ul canalului pentru rapoarte]
SERVER_NAME = TRUST.CSPOWER.RO
SERVER_WEBSITE = cspower.ro
```

### **5. Configurează Bot-ul pe Server**

1. **Conectează-te la serverul Discord** (ID: 1418768496795582657)
2. **Creează un canal nou** pentru rapoarte (ex: #reports)
3. **Click pe canal** → **Click pe ⚙️** → **Integrations** → **Webhooks**
4. **Click "Create Webhook"**
5. **Copiază URL-ul webhook-ului**
6. **Adaugă URL-ul** în Vercel Environment Variables ca `DISCORD_WEBHOOK_URL`

### **6. Testează Bot-ul**

1. **Scrie în chat:**
   ```
   !setup #reports
   ```
2. **Testează:**
   ```
   !test_report
   ```
3. **Verifică statusul:**
   ```
   !status
   ```

## 🔧 **Configurare Completă:**

### **Environment Variables Vercel:**
```
DISCORD_BOT_TOKEN = [TOKEN-ul bot-ului]
DISCORD_WEBHOOK_URL = [URL-ul webhook-ului]
REPORT_CHANNEL_ID = [ID-ul canalului]
SERVER_NAME = TRUST.CSPOWER.RO
SERVER_WEBSITE = cspower.ro
```

### **Comenzi Bot Discord:**
- `!setup #canal` - Configurează canalul pentru rapoarte
- `!test_report` - Testează sistemul
- `!status` - Status bot
- `!help_report` - Ajutor

## 🧪 **Testare Completă:**

### **1. Testează Bot-ul:**
```
!status
```

### **2. Testează Rapoartele:**
```
!test_report
```

### **3. Testează de pe Serverul CS 1.6:**
- Conectează-te la server (51.38.117.113:27015)
- Folosește `/report`
- Selectează un jucător și motivul
- Verifică că raportul apare în Discord

## 🎯 **Rezultatul Final:**

Ai un sistem complet care:
- ✅ **Bot Discord** pentru gestionarea rapoartelor
- ✅ **Webhook** pentru primirea rapoartelor de la CS 1.6
- ✅ **Embed-uri frumoase** în Discord
- ✅ **Comenzi admin** pentru gestionare
- ✅ **Integrare completă** cu serverul CS 1.6

---

**Sistem complet de rapoarte pentru TRUST.CSPOWER.RO! 🎮🤖**

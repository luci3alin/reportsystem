# 🤖 Ghid Pornire Bot Discord

## 🎯 **Problema: Bot-ul este Offline**

Bot-ul Discord trebuie să ruleze pe un server pentru a fi online! Iată cum să îl pornești:

## 🚀 **Opțiunea 1: Rulează Local (Cel Mai Simplu)**

### **1. Instalează Dependențele:**
```bash
pip install discord.py
```

### **2. Configurează Variabilele de Mediu:**

Creează fișierul `.env`:
```bash
DISCORD_BOT_TOKEN=TOKEN-ul_tau_aici
REPORT_CHANNEL_ID=ID-ul_canalului
SERVER_NAME=TRUST.CSPOWER.RO
SERVER_WEBSITE=cspower.ro
```

### **3. Pornește Bot-ul:**
```bash
python start_bot.py
```

## 🌐 **Opțiunea 2: Deploy pe Vercel (Recomandat)**

### **1. Adaugă Environment Variables în Vercel:**
```
DISCORD_BOT_TOKEN = [TOKEN-ul bot-ului]
REPORT_CHANNEL_ID = [ID-ul canalului]
SERVER_NAME = TRUST.CSPOWER.RO
SERVER_WEBSITE = cspower.ro
```

### **2. Deploy Bot-ul:**
- Bot-ul va rula automat pe Vercel
- Va fi online 24/7
- Nu trebuie să îl pornești manual

## 🔧 **Opțiunea 3: Server Dedicat (Avansat)**

### **1. Creează un Server VPS:**
- DigitalOcean, AWS, etc.
- Instalează Python
- Configurează variabilele de mediu

### **2. Rulează Bot-ul:**
```bash
python discord_bot.py
```

### **3. Păstrează-l Online:**
```bash
# Folosește screen sau tmux
screen -S discord_bot
python discord_bot.py
# Ctrl+A+D pentru a detașa
```

## 🧪 **Testează Bot-ul:**

### **1. Verifică Statusul:**
```
!status
```

### **2. Testează Rapoartele:**
```
!test_report
```

### **3. Configurează Canalul:**
```
!setup #reports
```

## 🎯 **Rezultatul Final:**

După ce pornești bot-ul:
- ✅ **Bot-ul va fi online** în Discord
- ✅ **Va primi rapoarte** de la serverul CS 1.6
- ✅ **Va afișa embed-uri** frumoase
- ✅ **Va funcționa 24/7** (dacă rulează pe server)

## 🚨 **Probleme Comune:**

### **1. Bot-ul nu se conectează:**
- Verifică token-ul
- Verifică permisiunile bot-ului
- Verifică conexiunea la internet

### **2. Bot-ul nu răspunde:**
- Verifică că bot-ul este online
- Verifică că are permisiuni în canal
- Verifică log-urile pentru erori

### **3. Rapoartele nu se trimit:**
- Verifică configurarea canalului
- Verifică integrarea cu Vercel
- Verifică log-urile

---

**Bot-ul trebuie să ruleze pentru a funcționa! 🚀**

# 🤖 Fantacalcio Bot - Inserimento Automatico Formazione

Bot automatico per inserire la formazione su [leghe.fantacalcio.it](https://leghe.fantacalcio.it/lega-paralimpica-seregno) ogni **martedì** e **giovedì** alle 13:00, anche a PC spento.

---

## 🎯 Funzionalità

- ✅ **Inserimento automatico** della formazione tramite GitHub Actions
- ✅ **Scheduling automatico**: martedì e giovedì alle 13:00 (ora italiana)
- ✅ **Notifiche email** a `saladaniele99@gmail.com` per conferma o errori
- ✅ **Log dettagliati** e screenshot automatici in caso di errore
- ✅ **Completamente gratuito** (usa GitHub Actions tier gratuito)
- ✅ **Funziona a PC spento** (eseguito nel cloud)

---

## 📋 Prerequisiti

- Account GitHub (già attivo ✅)
- Account Gmail per notifiche email
- Password App di Gmail (vedi setup sotto)

---

## 🚀 Setup Completo

### 1️⃣ Configura Password App Gmail

Per permettere al bot di inviare email di notifica:

1. Vai su [myaccount.google.com](https://myaccount.google.com/)
2. **Sicurezza** → Attiva **Verifica in due passaggi** (se non già attiva)
3. **Sicurezza** → **Password per le app**
4. Crea una nuova password app:
   - Nome: `Fantacalcio Bot`
   - Copia la password generata (16 caratteri)
   - **SALVALA** in un posto sicuro

### 2️⃣ Configura GitHub Secrets

Nel repository, vai su **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Crea questi **4 secrets**:

| Nome Secret | Valore | Descrizione |
|-------------|--------|-------------|
| `FANTACALCIO_USERNAME` | `tuo_username` | Username del sito fantacalcio.it |
| `FANTACALCIO_PASSWORD` | `tua_password` | Password del sito fantacalcio.it |
| `GMAIL_ADDRESS` | `saladaniele99@gmail.com` | Email per inviare notifiche |
| `GMAIL_APP_PASSWORD` | `password_16_caratteri` | Password app generata al punto 1 |

### 3️⃣ Personalizza la Formazione

Modifica il file **`formazione.json`** con i TUOI giocatori:

```json
{
  "modulo": "3-4-3",
  "titolari": {
    "portiere": "Maignan",
    "difensori": ["Bremer", "Bastoni", "Theo Hernandez"],
    "centrocampisti": ["Barella", "Tonali", "Zielinski", "Leao"],
    "attaccanti": ["Lautaro", "Osimhen", "Vlahovic"]
  }
}
```

### 4️⃣ Personalizza lo Script (IMPORTANTE)

⚠️ **MARTEDÌ** dovrai ispezionare il sito e aggiornare i selettori HTML in `fantacalcio_bot.py`:

- Apri il sito con Chrome
- Premi F12 (DevTools)
- Ispeziona i campi login, formazione, giocatori
- Aggiorna i selettori nello script

---

## 🧪 Test Manuale

Prima di aspettare martedì/giovedì, **testa subito**:

1. Vai su **Actions** nel repository
2. Clicca sul workflow `Fantacalcio Bot - Inserimento Automatico`
3. Clicca **Run workflow** → **Run workflow**
4. Aspetta 2-3 minuti
5. Controlla:
   - ✅ Il workflow è completato con successo?
   - ✅ Hai ricevuto l'email di notifica?

Se ci sono errori:
- Clicca sul run fallito
- Scarica i log dalla sezione **Artifacts**
- Controlla `fantacalcio_log.txt` e gli screenshot

---

## 📅 Scheduling Automatico

Il bot viene eseguito automaticamente:

- **Martedì alle 13:00** (ora italiana)
- **Giovedì alle 13:00** (ora italiana)

### Modificare gli orari

Edita `.github/workflows/fantacalcio.yml`:

```yaml
schedule:
  - cron: '0 11 * * 2'  # Martedì 13:00 IT = 11:00 UTC
  - cron: '0 11 * * 4'  # Giovedì 13:00 IT = 11:00 UTC
```

**Conversione UTC → Italia:**
- `10:00 UTC` = 12:00 Italia
- `11:00 UTC` = 13:00 Italia  
- `12:00 UTC` = 14:00 Italia

---

## 📧 Notifiche Email

Riceverai una email a `saladaniele99@gmail.com`:

### ✅ Email di Successo
```
✅ Fantacalcio Bot - Formazione inserita con successo!

La tua formazione è stata inserita automaticamente.
Non è necessaria alcuna azione da parte tua.
```

### ❌ Email di Errore
```
❌ URGENTE - Fantacalcio Bot: Formazione NON inserita!

⚠️ AZIONE RICHIESTA:
Inserisci MANUALMENTE la formazione su leghe.fantacalcio.it

Dettagli errore: [...]
Log completi: [link GitHub Actions]
```

---

## 🔍 Troubleshooting

### ❌ Il workflow non parte

**Problema:** Il bot non si esegue all'orario previsto  
**Soluzioni:**
- Verifica che GitHub Actions sia abilitato: `Settings` → `Actions` → `Allow all actions`
- Controlla che il repository sia privato (se pubblico, GitHub potrebbe limitare le Actions)
- Verifica che il file `.github/workflows/fantacalcio.yml` sia nella posizione corretta

### ❌ Nessuna email ricevuta

**Problema:** Il bot gira ma non ricevi email  
**Soluzioni:**
- Controlla la cartella **Spam/Promozioni** di Gmail
- Verifica che `GMAIL_ADDRESS` e `GMAIL_APP_PASSWORD` siano configurati correttamente nei Secrets
- Testa localmente con `python email_notifier.py`

### ❌ Login fallito

**Problema:** Il bot non riesce a fare login  
**Soluzioni:**
- Verifica che `FANTACALCIO_USERNAME` e `FANTACALCIO_PASSWORD` siano corretti
- Il sito potrebbe aver cambiato la pagina di login → aggiorna i selettori in `fantacalcio_bot.py`
- Controlla se c'è un CAPTCHA (in quel caso serve modificare lo script)

### ❌ Formazione non salvata

**Problema:** Login OK ma formazione non inserita  
**Soluzioni:**
- Verifica che i nomi giocatori in `formazione.json` siano esatti
- Il sito potrebbe richiedere conferme aggiuntive → ispeziona e aggiorna lo script
- Controlla screenshot `errore_*.png` negli Artifacts per vedere cosa è andato storto

---

## 📁 Struttura Repository

```
fantacalcio-bot/
├── .github/
│   └── workflows/
│       └── fantacalcio.yml          # Workflow GitHub Actions
├── fantacalcio_bot.py                # Script principale Python
├── email_notifier.py                 # Modulo notifiche email (standalone)
├── requirements.txt                  # Dipendenze Python
├── formazione.json                   # Configurazione formazione
└── README.md                         # Questo file
```

---

## 🛠️ Sviluppo e Test Locale

Per testare sul tuo PC prima di caricare su GitHub:

```bash
# 1. Clona il repository
git clone https://github.com/tuousername/fantacalcio-bot.git
cd fantacalcio-bot

# 2. Installa dipendenze
pip install -r requirements.txt

# 3. Imposta variabili ambiente (Windows)
set FANTACALCIO_USERNAME=tuo_username
set FANTACALCIO_PASSWORD=tua_password
set GMAIL_ADDRESS=saladaniele99@gmail.com
set GMAIL_APP_PASSWORD=tua_password_app

# 4. Esegui il bot
python fantacalcio_bot.py

# 5. Test email (opzionale)
python email_notifier.py
```

---

## 🔐 Sicurezza

- ✅ Credenziali protette tramite **GitHub Secrets** (crittografate AES-256)
- ✅ Repository **privato** (nessuno può vedere i tuoi dati)
- ✅ Password Gmail mai esposta nel codice
- ✅ Log pubblici NON contengono informazioni sensibili
- ✅ Secrets non visibili nei log di GitHub Actions

---

## 📊 Monitoraggio

### Storico esecuzioni
Vai su **Actions** nel repository per vedere:
- ✅ Esecuzioni completate con successo
- ❌ Esecuzioni fallite con dettagli errore
- 📊 Tempo di esecuzione (di solito 2-3 minuti)

### Log dettagliati
In caso di errore, scarica gli **Artifacts**:
- `fantacalcio_log.txt` → Log completo dell'esecuzione
- `errore_*.png` → Screenshot della pagina al momento dell'errore

---

## 📝 Note Importanti

- ⚠️ Il bot funziona **solo quando il sito permette di inserire formazioni**
- ⚠️ Assicurati che la giornata di campionato **non sia già iniziata**
- ⚠️ Il timeout per inserire la formazione è gestito dal sito (di solito fino all'anticipo)
- ℹ️ GitHub Actions tier gratuito: 2000 minuti/mese → questo bot ne usa ~10 minuti/mese (5 min × 2 volte)

---

## 🆘 Supporto

Se qualcosa non funziona:

1. **Controlla i log** su GitHub Actions
2. **Verifica i Secrets** siano configurati correttamente
3. **Testa manualmente** con "Run workflow"
4. **Scarica gli Artifacts** per vedere screenshot e log dettagliati
5. **Apri una Issue** nel repository se il problema persiste

---

## 🎉 Successo!

Una volta configurato correttamente, non dovrai più preoccuparti di dimenticare la formazione!  
Il bot penserà a tutto automaticamente ogni martedì e giovedì.

**Mai più 0 punti per formazione dimenticata!** 🏆

---

## 📌 Checklist Finale

Prima di considerare il setup completo:

- [ ] Repository creato e configurato come privato
- [ ] Tutti i 4 Secrets configurati su GitHub
- [ ] Password App Gmail generata e salvata
- [ ] File `formazione.json` personalizzato con i tuoi giocatori
- [ ] Script `fantacalcio_bot.py` personalizzato con selettori HTML corretti
- [ ] Test manuale eseguito con successo (`Run workflow`)
- [ ] Email di notifica ricevuta correttamente
- [ ] Workflow schedulato per martedì e giovedì

---

**Creato con ❤️ per la Lega Paralimpica Seregno**  
**Powered by:** GitHub Actions + Selenium + Python  
**Versione:** 1.0

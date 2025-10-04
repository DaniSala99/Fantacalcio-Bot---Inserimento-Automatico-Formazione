# 🤖 Fantacalcio Bot - Inserimento Automatico Formazione

Bot automatico per inserire la formazione su [leghe.fantacalcio.it](https://leghe.fantacalcio.it/lega-paralimpica-seregno) ogni martedì e giovedì.

## 🎯 Funzionalità

- ✅ **Inserimento automatico** della formazione anche a PC spento
- ✅ **Scheduling automatico**: martedì e giovedì alle 13:00 (ora italiana)
- ✅ **Notifiche email** per conferma o errori
- ✅ **Log dettagliati** e screenshot in caso di errore
- ✅ **Completamente gratuito** (GitHub Actions)

## 📋 Prerequisiti

- Account GitHub (già hai ✅)
- Account Gmail per notifiche email
- Password App di Gmail (vedi setup sotto)

## 🚀 Setup Iniziale

### 1. Configura Password App Gmail

Per permettere al bot di inviare email:

1. Vai su [Google Account](https://myaccount.google.com/)
2. **Sicurezza** → Attiva **Verifica in due passaggi** (se non attiva)
3. **Sicurezza** → **Password per le app**
4. Crea una nuova password app:
   - Nome: "Fantacalcio Bot"
   - Copia la password generata (16 caratteri)

### 2. Configura Secrets su GitHub

Nel repository, vai su **Settings** → **Secrets and variables** → **Actions**

Crea questi 4 secrets:

| Nome Secret | Valore |
|-------------|--------|
| `FANTACALCIO_USERNAME` | Il tuo username del sito |
| `FANTACALCIO_PASSWORD` | La tua password del sito |
| `GMAIL_ADDRESS` | saladaniele99@gmail.com |
| `GMAIL_APP_PASSWORD` | Password app generata sopra |

### 3. Personalizza la Formazione

Modifica il file `formazione.json` con i tuoi giocatori:

```json
{
  "modulo": "3-4-3",
  "titolari": {
    "portiere": "Nome Portiere",
    "difensori": ["Difensore1", "Difensore2", "Difensore3"],
    "centrocampisti": ["Centro1", "Centro2", "Centro3", "Centro4"],
    "attaccanti": ["Attaccante1", "Attaccante2", "Attaccante3"]
  }
}
```

## 🧪 Test Manuale

Prima di aspettare martedì/giovedì, testa subito:

1. Vai su **Actions** nel repository
2. Clicca sul workflow "Fantacalcio Bot"
3. **Run workflow** → **Run workflow**
4. Aspetta 2-3 minuti
5. Controlla l'email per la notifica

## 📅 Scheduling

Il bot gira automaticamente:
- **Martedì alle 13:00** (ora italiana)
- **Giovedì alle 13:00** (ora italiana)

Per modificare gli orari, edita `.github/workflows/fantacalcio.yml`:

```yaml
schedule:
  - cron: '0 11 * * 2'  # Martedì 13:00 IT (11:00 UTC)
  - cron: '0 11 * * 4'  # Giovedì 13:00 IT (11:00 UTC)
```

**Conversione orari UTC → Italia:**
- 10:00 UTC = 12:00 Italia
- 11:00 UTC = 13:00 Italia
- 12:00 UTC = 14:00 Italia

## 📧 Notifiche Email

Riceverai una email a `saladaniele99@gmail.com`:

- ✅ **Successo**: Conferma inserimento formazione
- ❌ **Errore**: Avviso per inserimento manuale + link ai log

## 🔍 Troubleshooting

### Il bot non gira
- Verifica che i secrets siano configurati correttamente
- Controlla che il repository sia privato
- GitHub Actions è abilitato? (Settings → Actions)

### Nessuna email ricevuta
- Verifica Gmail App Password corretta
- Controlla spam/promozioni
- Secrets `GMAIL_ADDRESS` e `GMAIL_APP_PASSWORD` configurati?

### Errori nel workflow
- Vai su **Actions** → Clicca sul run fallito
- Scarica i log e screenshot dalla sezione "Artifacts"
- Controlla `fantacalcio_log.txt` per dettagli
- Screenshot `errore_*.png` mostrano cosa è andato storto

### Login fallito
- Username/password corretti nei secrets?
- Il sito ha cambiato la pagina di login?
- Potrebbe esserci un CAPTCHA → Aggiorna lo script

### Formazione non salvata
- Verifica che i nomi giocatori siano esatti
- Controlla che tutti i campi obbligatori siano compilati
- Il sito potrebbe richiedere conferme aggiuntive

## 📁 Struttura Repository

```
fantacalcio-bot/
├── .github/
│   └── workflows/
│       └── fantacalcio.yml          # Workflow GitHub Actions
├── fantacalcio_bot.py                # Script principale
├── requirements.txt                  # Dipendenze Python
├── formazione.json                   # Configurazione formazione
└── README.md                         # Questo file
```

## 🛠️ Sviluppo Locale

Per testare sul tuo PC prima di caricare:

```bash
# 1. Clona il repository
git clone https://github.com/tuousername/fantacalcio-bot.git
cd fantacalcio-bot

# 2. Installa dipendenze
pip install -r requirements.txt

# 3. Imposta variabili ambiente
set FANTACALCIO_USERNAME=tuo_username
set FANTACALCIO_PASSWORD=tua_password
set GMAIL_ADDRESS=saladaniele99@gmail.com
set GMAIL_APP_PASSWORD=tua_password_app

# 4. Esegui
python fantacalcio_bot.py
```

## 🔐 Sicurezza

- ✅ Credenziali protette tramite GitHub Secrets (criptate)
- ✅ Repository privato (nessuno vede i tuoi dati)
- ✅ Password Gmail mai esposta nel codice
- ✅ Log pubblici non contengono informazioni sensibili

## 📊 Monitoraggio

- **GitHub Actions**: Vai su Actions per vedere lo storico esecuzioni
- **Email**: Ricevi notifica dopo ogni esecuzione
- **Log**: Scarica artifacts per debug dettagliato

## 🆘 Supporto

Se qualcosa non funziona:
1. Controlla i log su GitHub Actions
2. Verifica che secrets siano configurati
3. Testa manualmente con "Run workflow"
4. Apri una Issue nel repository (se necessario)

## 📝 Note

- Il bot funziona **solo quando il sito permette di inserire formazioni**
- Assicurati che la giornata di campionato non sia già iniziata
- Il timeout per l'inserimento formazione è gestito dal sito
- GitHub Actions ha un limite di 2000 minuti/mese (tier gratuito) - questo bot ne usa ~5 minuti/mese

## 🎉 Successo!

Una volta configurato correttamente, non dovrai più preoccuparti di dimenticare la formazione! Il bot penserà a tutto automaticamente ogni martedì e giovedì.

---

**Creato con ❤️ per la Lega Paralimpica Seregno**

**Powered by:** GitHub Actions + Selenium + Python

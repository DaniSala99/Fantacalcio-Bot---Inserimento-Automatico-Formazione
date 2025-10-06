# 🤖 Fantacalcio Bot - Salvataggio Automatico Formazione

Bot automatico per salvare la formazione su [leghe.fantacalcio.it](https://leghe.fantacalcio.it/lega-paralimpica-seregno) ogni **martedì** e **giovedì** alle **13:00**, anche a PC spento.

---

## 🎯 Funzionalità

- ✅ **Login automatico** con username e password
- ✅ **Salvataggio diretto** della formazione attuale (senza modifiche)
- ✅ **Mantiene titolari e panchina** esattamente come configurati manualmente
- ✅ **Salvataggio per tutte le competizioni** (Campionato, Coppa Italia, etc.)
- ✅ **Scheduling automatico**: martedì e giovedì alle 13:00 (ora italiana)
- ✅ **Notifiche email** a `saladaniele99@gmail.com` per conferma o errori
- ✅ **Log dettagliati** e screenshot automatici in caso di errore
- ✅ **Completamente gratuito** (usa GitHub Actions tier gratuito)
- ✅ **Funziona a PC spento** (eseguito nel cloud)

---

## 📋 Informazioni

- **Lega**: Lega Paralimpica Seregno
- **URL**: https://leghe.fantacalcio.it/lega-paralimpica-seregno
- **Username**: ------
- **Email notifiche**: saladaniele99@gmail.com
- **Metodo**: Salvataggio diretto senza modifiche alla formazione

---

## 🚀 Setup Completo

### 1️⃣ Configura Password App Gmail

Per ricevere le notifiche email:

1. Vai su [myaccount.google.com](https://myaccount.google.com/)
2. **Sicurezza** → Attiva **Verifica in due passaggi** (se non già attiva)
3. **Sicurezza** → **Password per le app**
4. Crea una nuova password app:
   - Nome: `Fantacalcio Bot`
   - Copia la password generata (16 caratteri senza spazi)
   - **SALVALA** - ti servirà nel prossimo step

### 2️⃣ Configura GitHub Secrets

Nel repository, vai su **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Crea questi **4 secrets**:

| Nome Secret | Valore | Descrizione |
|-------------|--------|-------------|
| `FANTACALCIO_USERNAME` | `-----` | Username del sito fantacalcio.it |
| `FANTACALCIO_PASSWORD` | `------` | Password del sito fantacalcio.it |
| `GMAIL_ADDRESS` | `saladaniele99@gmail.com` | Email per inviare notifiche |
| `GMAIL_APP_PASSWORD` | `[16 caratteri]` | Password app generata al punto 1 |

⚠️ **IMPORTANTE**: I secrets sono criptati e sicuri. Nessuno può vederli, nemmeno tu dopo averli salvati.

### 3️⃣ Verifica che i file siano caricati

Assicurati di avere questi file nel repository:

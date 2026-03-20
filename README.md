# 🤖 Fantacalcio Bot v3.0 - Salvataggio Automatico Formazione

Bot automatico che salva la formazione su [leghe.fantacalcio.it](https://leghe.fantacalcio.it/lega-paralimpica-seregno) nei giorni di campionato, anche a PC spento.

---

## 🎯 Funzionalità

- ✅ **Login automatico** con gestione popup e fallback multipli
- ✅ **Salvataggio formazione attuale** (senza modificarla) per tutte le competizioni
- ✅ **Scheduling automatico**: martedì, giovedì, venerdì alle 14:00 (ora italiana) + sabato 11:00 backup
- ✅ **Retry automatico**: 1 tentativo iniziale + 3 retry con attesa crescente (30/60/120s)
- ✅ **Retry a livello job** (GitHub Actions): ulteriore riesecuzione se il job fallisce
- ✅ **Verifica conferma salvataggio** con stato "incerto" se non trovata
- ✅ **Navigazione diretta** come fallback se la navigazione step-by-step fallisce
- ✅ **Gestione popup avanzata**: cookie, ads, overlay, ESC
- ✅ **Screenshot diagnostici** ad ogni step (caricati sempre come Artifact)
- ✅ **Log doppio**: file DEBUG + console INFO
- ✅ **Notifiche email** differenziate: successo / incerto / fallito

---

## 📅 Scheduling

| Trigger | UTC | Ora italiana | Note |
|---------|-----|--------------|------|
| Mar/Gio/Ven | 13:00 | 14:00 CET | Inverno (ottobre–marzo) |
| Mar/Gio/Ven | 12:00 | 14:00 CEST | Estate (marzo–ottobre) |
| Sabato | 09:00 | 11:00 CET / 10:00 CEST | Backup weekend |
| — | manuale | — | `workflow_dispatch` |

> **Nota**: entrambi i cron CET/CEST sono attivi tutto l'anno per garantire copertura a prescindere dal DST. Il salvataggio è idempotente, quindi la doppia esecuzione durante le transizioni è innocua.

---

## 📧 Notifiche email

| Stato | Oggetto | Azione richiesta |
|-------|---------|------------------|
| **Successo** | `Fantacalcio Bot - Formazione Salvata!` | Nessuna |
| **Incerto** | `Salvataggio INCERTO (verifica consigliata)` | Verificare manualmente |
| **Fallito** | `URGENTE - Formazione NON salvata!` | Inserire manualmente |

---

## 🔧 Come funziona il bot

```
1. Login su leghe.fantacalcio.it
2. Click su categoria "S-Cup Ella League"
3. Click su "Lega Paralimpica Seregno"
4. Click su "Schiera Formazione" (o navigazione diretta come fallback)
5. Click su "Salva per tutte le competizioni"
6. Verifica conferma salvataggio
7. Invio notifica email
```

In caso di errore ad ogni step: retry con selettori alternativi → fallback JS → eccezione → retry dell'intero processo.

---

## 🚀 Setup

### 1. Password App Gmail

1. [myaccount.google.com](https://myaccount.google.com/) → **Sicurezza** → **Verifica in due passaggi** (attivare se non già attivo)
2. **Sicurezza** → **Password per le app** → Crea nuova (nome: `Fantacalcio Bot`)
3. Copia la password generata (16 caratteri)

### 2. GitHub Secrets

**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret | Valore |
|--------|--------|
| `FANTACALCIO_USERNAME` | Username fantacalcio.it |
| `FANTACALCIO_PASSWORD` | Password fantacalcio.it |
| `GMAIL_ADDRESS` | Email mittente (es. `saladaniele99@gmail.com`) |
| `GMAIL_APP_PASSWORD` | Password app a 16 caratteri |

### 3. File nel repository

```
fantacalcio_bot.py
requirements.txt
.github/workflows/fantacalcio.yml
```

---

## 📋 Informazioni lega

- **Lega**: Lega Paralimpica Seregno
- **URL**: https://leghe.fantacalcio.it/lega-paralimpica-seregno
- **Formazione**: https://leghe.fantacalcio.it/lega-paralimpica-seregno/area-gioco/inserisci-formazione
- **Email notifiche**: saladaniele99@gmail.com + davidebanini99@gmail.com

---

## 🔍 Debug

Gli **Artifacts** di ogni run GitHub Actions contengono:
- `screenshot_*.png` — screenshot ad ogni step
- `fantacalcio_log.txt` — log completo (livello DEBUG)
- `debug_*.html` — HTML della pagina in caso di errore/incertezza

Retention: **3 giorni** (anche per le run riuscite).

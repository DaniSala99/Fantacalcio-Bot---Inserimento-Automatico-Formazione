"""
Email Notifier - Modulo per inviare notifiche email
Può essere usato standalone o integrato in fantacalcio_bot.py

Configurazione richiesta:
- GMAIL_ADDRESS: indirizzo Gmail mittente
- GMAIL_APP_PASSWORD: password per le app di Gmail
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os


def invia_email_successo(destinatario='saladaniele99@gmail.com', dettagli=''):
    """
    Invia una email di conferma per inserimento formazione riuscito
    
    Args:
        destinatario (str): Email del destinatario
        dettagli (str): Dettagli aggiuntivi sull'operazione
    
    Returns:
        bool: True se l'invio ha successo, False altrimenti
    """
    mittente = os.environ.get('GMAIL_ADDRESS')
    password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if not mittente or not password:
        print("❌ Credenziali email non configurate")
        return False
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "✅ Fantacalcio Bot - Formazione inserita con successo!"
    msg['From'] = mittente
    msg['To'] = destinatario
    
    timestamp = datetime.now().strftime('%d/%m/%Y alle %H:%M:%S')
    
    # Versione testo semplice
    testo = f"""
✅ FORMAZIONE INSERITA CON SUCCESSO!

Data e ora: {timestamp}
Lega: Lega Paralimpica Seregno
Stato: Confermata

{dettagli}

La tua formazione è stata inserita automaticamente.
Non è necessaria alcuna azione da parte tua.

---
🤖 Messaggio automatico dal Fantacalcio Bot
Repository: https://github.com/tuousername/fantacalcio-bot
    """
    
    # Versione HTML formattata
    html = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
          .header {{ background-color: #4CAF50; color: white; padding: 20px; border-radius: 5px; text-align: center; }}
          .content {{ padding: 20px; background-color: #f9f9f9; margin-top: 20px; border-radius: 5px; }}
          .info {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
          .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }}
          strong {{ color: #4CAF50; }}
        </style>
      </head>
      <body>
        <div class="header">
          <h1>✅ Formazione Inserita!</h1>
        </div>
        
        <div class="content">
          <div class="info">
            <p><strong>📅 Data e ora:</strong> {timestamp}</p>
            <p><strong>🏆 Lega:</strong> Lega Paralimpica Seregno</p>
            <p><strong>⚽ Stato:</strong> Formazione confermata</p>
          </div>
          
          <p>La tua formazione è stata inserita automaticamente.</p>
          <p>Non è necessaria alcuna azione da parte tua.</p>
          
          {f'<div class="info"><p>{dettagli}</p></div>' if dettagli else ''}
        </div>
        
        <div class="footer">
          <p>🤖 Messaggio automatico dal Fantacalcio Bot</p>
          <p>Repository: <a href="https://github.com/tuousername/fantacalcio-bot">fantacalcio-bot</a></p>
        </div>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(testo, 'plain'))
    msg.attach(MIMEText(html, 'html'))
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(mittente, password)
            server.send_message(msg)
        
        print(f"✉️ Email di successo inviata a {destinatario}")
        return True
        
    except Exception as e:
        print(f"❌ Errore nell'invio email: {str(e)}")
        return False


def invia_email_errore(destinatario='saladaniele99@gmail.com', errore='', dettagli=''):
    """
    Invia una email di notifica per inserimento formazione fallito
    
    Args:
        destinatario (str): Email del destinatario
        errore (str): Messaggio di errore
        dettagli (str): Dettagli aggiuntivi sull'errore
    
    Returns:
        bool: True se l'invio ha successo, False altrimenti
    """
    mittente = os.environ.get('GMAIL_ADDRESS')
    password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if not mittente or not password:
        print("❌ Credenziali email non configurate")
        return False
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "❌ URGENTE - Fantacalcio Bot: Formazione NON inserita!"
    msg['From'] = mittente
    msg['To'] = destinatario
    
    timestamp = datetime.now().strftime('%d/%m/%Y alle %H:%M:%S')
    
    # Versione testo semplice
    testo = f"""
❌ ERRORE NELL'INSERIMENTO FORMAZIONE!

Data e ora: {timestamp}
Lega: Lega Paralimpica Seregno
Stato: FALLITO

⚠️ ERRORE:
{errore}

DETTAGLI:
{dettagli}

🚨 AZIONE RICHIESTA:
Inserisci MANUALMENTE la formazione prima dell'inizio delle partite su:
https://leghe.fantacalcio.it/lega-paralimpica-seregno

Controlla i log su GitHub Actions per maggiori dettagli:
https://github.com/tuousername/fantacalcio-bot/actions

---
🤖 Messaggio automatico dal Fantacalcio Bot
    """
    
    # Versione HTML formattata
    html = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
          .header {{ background-color: #f44336; color: white; padding: 20px; border-radius: 5px; text-align: center; }}
          .content {{ padding: 20px; background-color: #f9f9f9; margin-top: 20px; border-radius: 5px; }}
          .error {{ background-color: #fff3cd; padding: 15px; margin: 10px 0; border-left: 4px solid #ffc107; }}
          .action {{ background-color: #e3f2fd; padding: 15px; margin: 10px 0; border-left: 4px solid #2196F3; }}
          .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }}
          .urgent {{ color: #f44336; font-weight: bold; }}
          pre {{ background-color: white; padding: 10px; border-radius: 3px; overflow-x: auto; }}
        </style>
      </head>
      <body>
        <div class="header">
          <h1>❌ Errore Inserimento Formazione</h1>
        </div>
        
        <div class="content">
          <div class="error">
            <p><strong>📅 Data e ora:</strong> {timestamp}</p>
            <p><strong>🏆 Lega:</strong> Lega Paralimpica Seregno</p>
            <p><strong>⚠️ Stato:</strong> <span class="urgent">FALLITO</span></p>
          </div>
          
          <div class="error">
            <h3>🚨 Errore:</h3>
            <pre>{errore}</pre>
          </div>
          
          {f'<div class="error"><h3>Dettagli:</h3><pre>{dettagli}</pre></div>' if dettagli else ''}
          
          <div class="action">
            <h3>⚡ AZIONE RICHIESTA:</h3>
            <p><strong>Inserisci MANUALMENTE la formazione prima dell'inizio delle partite!</strong></p>
            <p>👉 <a href="https://leghe.fantacalcio.it/lega-paralimpica-seregno" style="color: #2196F3; font-weight: bold;">Vai al sito Fantacalcio</a></p>
          </div>
          
          <p>Controlla i log dettagliati su <a href="https://github.com/tuousername/fantacalcio-bot/actions">GitHub Actions</a></p>
        </div>
        
        <div class="footer">
          <p>🤖 Messaggio automatico dal Fantacalcio Bot</p>
          <p>Repository: <a href="https://github.com/tuousername/fantacalcio-bot">fantacalcio-bot</a></p>
        </div>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(testo, 'plain'))
    msg.attach(MIMEText(html, 'html'))
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(mittente, password)
            server.send_message(msg)
        
        print(f"✉️ Email di errore inviata a {destinatario}")
        return True
        
    except Exception as e:
        print(f"❌ Errore nell'invio email: {str(e)}")
        return False


def test_email():
    """
    Funzione di test per verificare l'invio email
    Eseguila localmente prima di caricare su GitHub
    """
    print("📧 Test invio email...")
    print("=" * 50)
    
    # Test email di successo
    print("\n1. Test email di SUCCESSO:")
    successo1 = invia_email_successo(
        dettagli="Test locale: formazione inserita correttamente con tutti i giocatori."
    )
    print(f"   Risultato: {'✅ OK' if successo1 else '❌ FALLITO'}")
    
    # Test email di errore
    print("\n2. Test email di ERRORE:")
    successo2 = invia_email_errore(
        errore="Test locale: simulazione errore",
        dettagli="Questo è un test per verificare che le notifiche di errore funzionino correttamente."
    )
    print(f"   Risultato: {'✅ OK' if successo2 else '❌ FALLITO'}")
    
    print("\n" + "=" * 50)
    print("📧 Test completato!")
    
    if successo1 and successo2:
        print("✅ Entrambe le email sono state inviate correttamente!")
        print("📬 Controlla la tua inbox: saladaniele99@gmail.com")
    else:
        print("❌ Alcuni invii sono falliti. Verifica:")
        print("   1. GMAIL_ADDRESS è configurato?")
        print("   2. GMAIL_APP_PASSWORD è corretto?")
        print("   3. Hai attivato la verifica in 2 passaggi su Gmail?")
        print("   4. Hai generato una Password per le app?")


# Esecuzione standalone per test
if __name__ == "__main__":
    print("🤖 Email Notifier - Modulo di Test")
    print("=" * 50)
    print("")
    
    # Verifica che le variabili d'ambiente siano configurate
    gmail_address = os.environ.get('GMAIL_ADDRESS')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if not gmail_address or not gmail_password:
        print("⚠️ ATTENZIONE: Variabili d'ambiente non configurate!")
        print("")
        print("Per testare localmente, esegui prima:")
        print("")
        print("Windows:")
        print("  set GMAIL_ADDRESS=saladaniele99@gmail.com")
        print("  set GMAIL_APP_PASSWORD=tua_password_app")
        print("  python email_notifier.py")
        print("")
        print("Linux/Mac:")
        print("  export GMAIL_ADDRESS=saladaniele99@gmail.com")
        print("  export GMAIL_APP_PASSWORD=tua_password_app")
        print("  python email_notifier.py")
        print("")
    else:
        print(f"✅ GMAIL_ADDRESS configurato: {gmail_address}")
        print(f"✅ GMAIL_APP_PASSWORD configurato: {'*' * len(gmail_password)}")
        print("")
        
        # Esegui i test
        test_email()
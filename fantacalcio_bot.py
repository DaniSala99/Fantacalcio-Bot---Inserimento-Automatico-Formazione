"""
Fantacalcio Bot - Salvataggio Automatico Formazione
VERSIONE FINALE SEMPLIFICATA per Lega Paralimpica Seregno

Repository: https://github.com/tuousername/fantacalcio-bot
Lega: https://leghe.fantacalcio.it/lega-paralimpica-seregno

Username: saladany99
Email notifiche: saladaniele99@gmail.com

Funzionamento:
1. Login automatico con credenziali
2. Navigazione a "Schiera Formazione"
3. Click diretto su "Salva per tutte le competizioni"
4. Invio email di conferma/errore

NOTA: Salva la formazione attuale senza modificarla, mantenendo panchina e titolari come sono.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import logging
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurazione logging
logging.basicConfig(
    filename='fantacalcio_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FantacalcioBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Configura il browser Chrome in modalità headless per ambiente cloud"""
        logging.info("=" * 60)
        logging.info("Configurazione browser Chrome...")
        
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Per ambienti cloud Linux
        chrome_options.binary_location = os.environ.get('CHROME_BIN', '/usr/bin/google-chrome')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        
        logging.info("✅ Browser configurato con successo")
        
    def login(self):
        """Effettua il login al sito"""
        try:
            logging.info("=" * 60)
            logging.info("STEP 1: LOGIN")
            logging.info("=" * 60)
            
            # Vai alla pagina della lega
            logging.info("Navigazione a: https://leghe.fantacalcio.it/lega-paralimpica-seregno")
            self.driver.get("https://leghe.fantacalcio.it/lega-paralimpica-seregno")
            time.sleep(3)
            
            # Clicca sul pulsante "Accedi"
            logging.info("Ricerca pulsante 'Accedi'...")
            accedi_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='https://leghe.fantacalcio.it/login' and contains(@class, 'btn-primary')]"))
            )
            accedi_btn.click()
            logging.info("✅ Click su 'Accedi' effettuato")
            time.sleep(3)
            
            # Inserisci username
            logging.info(f"Inserimento username: {self.username}")
            username_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='username']"))
            )
            username_field.clear()
            username_field.send_keys(self.username)
            logging.info("✅ Username inserito")
            time.sleep(1)
            
            # Inserisci password
            logging.info("Inserimento password...")
            password_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='password']"))
            )
            password_field.clear()
            password_field.send_keys(self.password)
            logging.info("✅ Password inserita")
            time.sleep(1)
            
            # Clicca su LOGIN
            logging.info("Click su pulsante LOGIN...")
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ant-btn-primary') and .//span[text()='LOGIN']]"))
            )
            login_btn.click()
            logging.info("✅ Click su LOGIN effettuato")
            time.sleep(5)
            
            logging.info("✅✅ LOGIN COMPLETATO CON SUCCESSO")
            return True
            
        except Exception as e:
            logging.error(f"❌ ERRORE durante il login: {str(e)}")
            self.driver.save_screenshot(f"errore_login_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            return False
    
    def salva_formazione(self):
        """
        Salva la formazione attuale (già configurata) per tutte le competizioni
        """
        try:
            logging.info("=" * 60)
            logging.info("STEP 2: SALVATAGGIO FORMAZIONE")
            logging.info("=" * 60)
            
            # STEP 2.1: Clicca su "Schiera Formazione"
            logging.info("Ricerca link 'Schiera Formazione'...")
            inserisci_formazione_link = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    "//a[@class='shortcut' and @href='https://leghe.fantacalcio.it/lega-paralimpica-seregno/area-gioco/inserisci-formazione']"
                ))
            )
            inserisci_formazione_link.click()
            logging.info("✅ Click su 'Schiera Formazione' effettuato")
            time.sleep(4)
            
            # STEP 2.2: Clicca direttamente su "Salva per tutte le competizioni"
            logging.info("Ricerca pulsante 'Salva per tutte le competizioni'...")
            salva_btn = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class, 'btn-orange') and contains(@onclick, 'saveFormationForAllComps')]"
                ))
            )
            salva_btn.click()
            logging.info("✅ Click su 'Salva per tutte le competizioni' effettuato")
            time.sleep(4)
            
            logging.info("✅✅ FORMAZIONE SALVATA CON SUCCESSO!")
            return True
            
        except Exception as e:
            logging.error(f"❌ ERRORE nel salvataggio della formazione: {str(e)}")
            self.driver.save_screenshot(f"errore_formazione_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            return False
    
    def invia_notifica_email(self, successo, dettagli=""):
        """Invia una email di notifica con il risultato"""
        try:
            mittente = os.environ.get('GMAIL_ADDRESS')
            password = os.environ.get('GMAIL_APP_PASSWORD')
            destinatario = 'saladaniele99@gmail.com'
            
            if not mittente or not password:
                logging.warning("⚠️ Credenziali email non configurate, notifica saltata")
                return False
            
            msg = MIMEMultipart('alternative')
            timestamp = datetime.now().strftime('%d/%m/%Y alle %H:%M:%S')
            
            if successo:
                msg['Subject'] = "✅ Fantacalcio Bot - Formazione Salvata!"
                
                # Versione testo
                testo = f"""
✅ FORMAZIONE SALVATA CON SUCCESSO!

📅 Data e ora: {timestamp}
🏆 Lega: Lega Paralimpica Seregno
👤 Username: saladany99

La formazione attuale è stata salvata automaticamente per tutte le competizioni 
(Campionato, Coppa Italia, Supercoppa, etc.).

La formazione precedentemente configurata (titolari e panchina) è stata mantenuta 
e salvata senza modifiche.

{dettagli}

Non è necessaria alcuna azione da parte tua.
Buona fortuna! ⚽

---
🤖 Messaggio automatico dal Fantacalcio Bot
Repository: https://github.com/tuousername/fantacalcio-bot
                """
                
                # Versione HTML
                html = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                  color: white; padding: 30px; border-radius: 10px; text-align: center; }}
                        .content {{ padding: 20px; background-color: #f9f9f9; margin-top: 20px; 
                                   border-radius: 10px; }}
                        .info {{ background-color: white; padding: 20px; margin: 15px 0; 
                                border-left: 5px solid #4CAF50; border-radius: 5px; }}
                        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd; 
                                  color: #666; font-size: 12px; text-align: center; }}
                        strong {{ color: #4CAF50; }}
                        h1 {{ margin: 0; font-size: 28px; }}
                        .emoji {{ font-size: 40px; }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <div class="emoji">✅</div>
                        <h1>Formazione Salvata!</h1>
                    </div>
                    
                    <div class="content">
                        <div class="info">
                            <p><strong>📅 Data e ora:</strong> {timestamp}</p>
                            <p><strong>🏆 Lega:</strong> Lega Paralimpica Seregno</p>
                            <p><strong>👤 Username:</strong> saladany99</p>
                            <p><strong>✅ Stato:</strong> Formazione salvata per tutte le competizioni</p>
                        </div>
                        
                        <p>La <strong>formazione attuale</strong> è stata salvata automaticamente per 
                        <strong>tutte le competizioni</strong> (Campionato, Coppa Italia, Supercoppa, etc.).</p>
                        
                        <p>✅ Titolari: mantenuti come configurato<br>
                        ✅ Panchina: mantenuta come configurata<br>
                        ✅ Nessuna modifica apportata</p>
                        
                        <p>Non è necessaria alcuna azione da parte tua. Buona fortuna! ⚽</p>
                    </div>
                    
                    <div class="footer">
                        <p>🤖 Messaggio automatico dal <strong>Fantacalcio Bot</strong></p>
                        <p>Prossima esecuzione automatica: Martedì/Giovedì alle 13:00</p>
                    </div>
                </body>
                </html>
                """
                
            else:
                msg['Subject'] = "❌ URGENTE - Fantacalcio Bot: Formazione NON salvata!"
                
                # Versione testo
                testo = f"""
❌ ERRORE NEL SALVATAGGIO FORMAZIONE!

📅 Data e ora: {timestamp}
🏆 Lega: Lega Paralimpica Seregno
👤 Username: saladany99

⚠️ ERRORE:
{dettagli}

🚨 AZIONE RICHIESTA:
Inserisci/Salva MANUALMENTE la formazione prima dell'inizio delle partite!

👉 Vai su: https://leghe.fantacalcio.it/lega-paralimpica-seregno/area-gioco/inserisci-formazione

📊 Log dettagliati disponibili su:
https://github.com/tuousername/fantacalcio-bot/actions

---
🤖 Messaggio automatico dal Fantacalcio Bot
                """
                
                # Versione HTML
                html = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                        .header {{ background: linear-gradient(135deg, #f44336 0%, #e91e63 100%); 
                                  color: white; padding: 30px; border-radius: 10px; text-align: center; }}
                        .content {{ padding: 20px; background-color: #f9f9f9; margin-top: 20px; 
                                   border-radius: 10px; }}
                        .error {{ background-color: #fff3cd; padding: 20px; margin: 15px 0; 
                                 border-left: 5px solid #ffc107; border-radius: 5px; }}
                        .action {{ background-color: #e3f2fd; padding: 20px; margin: 15px 0; 
                                  border-left: 5px solid #2196F3; border-radius: 5px; }}
                        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd; 
                                  color: #666; font-size: 12px; text-align: center; }}
                        .urgent {{ color: #f44336; font-weight: bold; font-size: 18px; }}
                        pre {{ background-color: white; padding: 15px; border-radius: 5px; 
                              overflow-x: auto; border: 1px solid #ddd; }}
                        h1 {{ margin: 0; font-size: 28px; }}
                        .emoji {{ font-size: 40px; }}
                        a {{ color: #2196F3; font-weight: bold; text-decoration: none; }}
                        a:hover {{ text-decoration: underline; }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <div class="emoji">❌</div>
                        <h1>Errore Salvataggio!</h1>
                    </div>
                    
                    <div class="content">
                        <div class="error">
                            <p><strong>📅 Data e ora:</strong> {timestamp}</p>
                            <p><strong>🏆 Lega:</strong> Lega Paralimpica Seregno</p>
                            <p><strong>👤 Username:</strong> saladany99</p>
                            <p class="urgent">⚠️ Stato: OPERAZIONE FALLITA</p>
                        </div>
                        
                        <div class="error">
                            <h3>🚨 Dettagli errore:</h3>
                            <pre>{dettagli}</pre>
                        </div>
                        
                        <div class="action">
                            <h3>⚡ AZIONE RICHIESTA:</h3>
                            <p class="urgent">Inserisci/Salva MANUALMENTE la formazione prima dell'inizio delle partite!</p>
                            <p>👉 <a href="https://leghe.fantacalcio.it/lega-paralimpica-seregno/area-gioco/inserisci-formazione">
                            Vai al sito Fantacalcio</a></p>
                        </div>
                        
                        <p>📊 Log dettagliati e screenshot disponibili su 
                        <a href="https://github.com/tuousername/fantacalcio-bot/actions">GitHub Actions</a></p>
                    </div>
                    
                    <div class="footer">
                        <p>🤖 Messaggio automatico dal <strong>Fantacalcio Bot</strong></p>
                    </div>
                </body>
                </html>
                """
            
            msg['From'] = mittente
            msg['To'] = destinatario
            msg.attach(MIMEText(testo, 'plain'))
            msg.attach(MIMEText(html, 'html'))
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(mittente, password)
                server.send_message(msg)
            
            logging.info(f"✉️ Email di notifica inviata a {destinatario}")
            return True
            
        except Exception as e:
            logging.error(f"❌ Errore nell'invio email: {str(e)}")
            return False
    
    def esegui(self):
        """Esegue l'intero processo"""
        dettagli_errore = ""
        
        try:
            self.setup_driver()
            
            if not self.login():
                raise Exception("Login fallito - Verifica username e password nei GitHub Secrets")
            
            if not self.salva_formazione():
                raise Exception("Impossibile salvare la formazione - Controlla screenshot")
            
            logging.info("=" * 60)
            logging.info("✅✅✅ PROCESSO COMPLETATO CON SUCCESSO! ✅✅✅")
            logging.info("=" * 60)
            self.invia_notifica_email(True, "Formazione salvata correttamente senza modifiche.")
            return True
            
        except Exception as e:
            dettagli_errore = str(e)
            logging.error("=" * 60)
            logging.error(f"❌❌❌ PROCESSO FALLITO: {dettagli_errore}")
            logging.error("=" * 60)
            self.invia_notifica_email(False, f"Errore: {dettagli_errore}\n\nControlla i log e screenshot su GitHub Actions.")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()
                logging.info("Browser chiuso")


# ============================================================================
# ESECUZIONE PRINCIPALE
# ============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("🤖  FANTACALCIO BOT - Salvataggio Automatico Formazione")
    print("=" * 70)
    print(f"⏰  Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🏆  Lega: Lega Paralimpica Seregno")
    print(f"📧  Email notifiche: saladaniele99@gmail.com")
    print("=" * 70)
    print()
    
    # Leggi credenziali da variabili d'ambiente (GitHub Secrets)
    username = os.environ.get('FANTACALCIO_USERNAME')
    password = os.environ.get('FANTACALCIO_PASSWORD')
    
    if not username or not password:
        print("❌ ERRORE: Credenziali non configurate!")
        print("Configura FANTACALCIO_USERNAME e FANTACALCIO_PASSWORD nei GitHub Secrets")
        print()
        exit(1)
    
    print(f"👤  Username: {username}")
    print(f"🔒  Password: {'*' * len(password)}")
    print()
    print("🚀  Avvio bot...")
    print("💡  Modalità: Salvataggio formazione attuale (senza modifiche)")
    print()
    
    # Esegui il bot
    bot = FantacalcioBot(username, password)
    successo = bot.esegui()
    
    print()
    print("=" * 70)
    if successo:
        print("✅  OPERAZIONE COMPLETATA CON SUCCESSO!")
        print("📧  Controlla saladaniele99@gmail.com per la conferma")
        print("🏆  Formazione salvata per tutte le competizioni")
        print("=" * 70)
        exit(0)
    else:
        print("❌  OPERAZIONE FALLITA")
        print("📄  Controlla fantacalcio_log.txt per i dettagli")
        print("📧  Dovresti aver ricevuto una email di notifica errore")
        print("🔍  Screenshot salvato in errore_*.png")
        print("=" * 70)
        exit(1)

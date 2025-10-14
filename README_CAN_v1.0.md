# 🌍 CAN – Cambiamento Ambientale Nazionale

### Analisi e visualizzazione dei dati ambientali ed energetici regionali italiani

---

## 📖 Descrizione

**CAN Dashboard** è un progetto completo che integra:
- un **backend FastAPI** per la gestione e l’esposizione dei dati ambientali regionali italiani;
- un **frontend Dash/Plotly** per la visualizzazione interattiva di mappe e grafici;
- un **database MySQL** gestito tramite Docker, per garantire persistenza e scalabilità.

L’obiettivo è offrire una panoramica chiara e interattiva della transizione energetica italiana,
fornendo uno strumento utile a enti, analisti e cittadini.

---

## 🧩 Architettura generale

| Componente | Descrizione | Tecnologie principali |
|-------------|--------------|------------------------|
| **Backend (API)** | Fornisce endpoint REST per CRUD e consultazione dei dati | FastAPI, SQLAlchemy, PyMySQL |
| **Frontend (Dashboard)** | Interfaccia interattiva per la visualizzazione dei dati | Dash, Plotly, Bootstrap |
| **Database** | Archiviazione strutturata dei dati ambientali e regionali | MySQL, Docker |

---

## 📂 Struttura del progetto

```
CAN/
│
├── backend/
│   ├── main.py               → Avvio FastAPI e registrazione router
│   ├── routes.py             → Endpoint API per ogni tabella
│   ├── models.py             → Modelli SQLAlchemy
│   ├── schemas.py            → Schemi Pydantic
│   ├── services.py           → Logica CRUD separata dalle route
│   ├── database.py           → Connessione e motore MySQL
│   ├── popola_tabelle.py     → Script di popolamento iniziale del DB
│   ├── can_dump.sql          → Dump SQL del database CAN
│   ├── dockerfile
│   └── requirements.txt      → Dipendenze backend
│
├── frontend/
│   ├── app.py                → File principale Dash (avvio dell’app)
│   ├── api.py                → Funzioni di richiesta ai servizi FastAPI
│   ├── data_utils.py         → Dati e funzioni condivise
│   ├── __init__.py           
│   │
│   ├── components/           → Layout della dashboard
│   │   ├── navbar.py
│   │   ├── mappa.py
│   │   ├── meteo.py
│   │   ├── suolo.py
│   │   ├── swot.py
│   │   ├── fonti.py
│   │   ├── edifici.py
│   │   ├── industria.py
│   │   ├── azioni.py
│   │   ├── comparazione.py
│   │   └── footer.py
│   │
│   ├── callbacks/            → Logica interattiva per ogni sezione
│   │   ├── navbar_callbacks.py
│   │   ├── mappa_callbacks.py
│   │   ├── meteo_callbacks.py
│   │   ├── swot_callbacks.py
│   │   ├── fonti_callbacks.py
│   │   ├── edifici_callbacks.py
│   │   ├── industria_callbacks.py
│   │   ├── azioni_callbacks.py
│   │   └── comparazione_callbacks.py
│   │  
│   ├── assets/
│   │   ├── style.css         → Stile globale della dashboard
│   │   ├── pannello.png
│   │   ├── palaeolica.png
│   │   ├── autoelettrica.png
│   │   └── casa.png
│   │
│   ├── limits_IT_regions.geojson  → Dati geografici delle regioni italiane
│   ├── meteo.env                  → API key OpenWeather
│   ├── dockerfile
│   └── requirements.txt      → Dipendenze frontend
│
├── DB/
│   ├── *.csv                    → Dataset originali regionali
│   ├── can_dump.sql 
│   ├── dump.sql
│   └── mysqldata/               → Volume dati persistente
│
├── backupSQL/                    
│
├── docker-compose.yml           → Avvio container MySQL + phpMyAdmin
├── dump_mysql.py                → Esegue il dump
├── import_mysql.py              → Importa il file MySQL nel DB
└── README.md                    → Documentazione generale del progetto
```

---

## ⚙️ Setup e installazione

### 1️⃣ Clona il repository
```bash
git clone https://github.com/<nome_repo>/CAN.git
cd CAN
```

### 2️⃣ Crea un ambiente virtuale
```bash
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate       # Windows
```

### 3️⃣ Installa le dipendenze
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 4️⃣ Avvia i servizi
- **Backend**
  ```bash
  cd backend
  uvicorn main:app --reload --port 8000
  ```
- **Frontend**
  ```bash
  cd can
  python -m frontend.app
  ```
- **Database**
  ```bash
  cd ../DB
  docker compose up -d
  ```

---

## 🧰 Dipendenze principali

- **Python ≥ 3.9**
- **FastAPI**, **SQLAlchemy**, **PyMySQL**, **Uvicorn**
- **Dash**, **Plotly**, **Dash Bootstrap Components**
- **Pandas**, **python-dotenv**
- **Docker**, **MySQL**, **phpMyAdmin**

---

## 🚀 Deploy e containerizzazione

### 🐳 Docker Compose (completo: backend + frontend + DB)

Esempio di `docker-compose.yml` per eseguire tutti i servizi insieme:

```yaml
version: "3.9"
services:
  db:
    image: mysql:8
    container_name: can_mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: CAN_DB
    ports:
      - "3306:3306"
    volumes:
      - ./DB/mysqldata:/var/lib/mysql

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: can_phpmyadmin
    restart: always
    ports:
      - "8080:80"
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: rootpass

  backend:
    build: ./backend
    container_name: can_backend
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    depends_on:
      - db

  frontend:
    build: ./frontend
    container_name: can_frontend
    command: python app.py
    ports:
      - "8050:8050"
    volumes:
      - ./frontend:/app
    depends_on:
      - backend
```

---

## 🌐 Deploy su Render o altri provider

1. **Crea un database MySQL gestito** (Render, Railway, Neon, ecc.)
2. **Imposta le variabili d’ambiente:**
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
   - `WEATHER_API_KEY`
3. **Esegui il backend su un servizio Python (FastAPI)** con `start command`:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
4. **Esegui il frontend Dash** con:
   ```
   python app.py
   ```
5. Imposta le porte:
   - Backend → `8000`
   - Frontend → `8050`

---

## 🧠 Documentazione

### ▶️ Swagger UI
Accesso automatico alla documentazione interattiva FastAPI:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

### 🗺️ Dashboard interattiva
👉 [http://localhost:8050](http://localhost:8050)

### 📄 Pydoc
Genera la documentazione HTML:
```bash
pydoc -w frontend
```
oppure

```bash
python -m pydoc -w frontend
```

---

## 🧱 Database e container

| Servizio | Porta | Descrizione |
|-----------|-------|-------------|
| MySQL | 3306 | Database CAN |
| phpMyAdmin | 8080 | Interfaccia grafica per il DB |
| FastAPI | 8000 | Backend API |
| Dash | 8050 | Frontend interattivo |

---

## 🏷️ Versione e changelog

- **v1.0.0** – Struttura completa e modulare:
  - Frontend Dash componentizzato (layout + callback separati)
  - Backend FastAPI con CRUD e documentazione Swagger
  - Cache meteo e integrazione OpenWeather
  - Database MySQL in container Docker

---

## 👥 Autori

**Team CAN – Eurix Srl**  
Progetto di sviluppo e comunicazione per la transizione energetica e ambientale.

- Carlotta Forlino  
- Andrea Calabrò  
- Nicolò Giraudo

# MongoDB Backup & Restore

Backup- und Restore-Skripte für MongoDB Atlas (Free Tier M0).  
Auf dem M0-Tier sind keine automatischen Backups verfügbar — dieses Repository ersetzt sie.

## Voraussetzungen

### 1. MongoDB Database Tools installieren

Die Tools `mongodump` und `mongorestore` müssen installiert sein:

| Betriebssystem | Befehl / Link |
|----------------|---------------|
| **macOS** | `brew install mongodb-database-tools` |
| **Ubuntu/Debian** | Siehe [offizielle Anleitung](https://www.mongodb.com/try/download/database-tools) |
| **Windows** | [Download MSI-Installer](https://www.mongodb.com/try/download/database-tools), dann `C:\Program Files\MongoDB\Tools\bin` zum PATH hinzufügen |

Installation prüfen:
```bash
mongodump --version
mongorestore --version
```

### 2. `.env` Datei konfigurieren

```bash
cp .env .env.bak  # optional: Backup der Vorlage
```

Dann `.env` öffnen und ausfüllen:

```env
MONGO_URI=mongodb+srv://user:passwort@cluster.mongodb.net
DB_NAME=multilingual-language
```

Die `MONGO_URI` findest du in MongoDB Atlas unter:  
**Cluster → Connect → Drivers → Connection String**

---

## Verwendung

### Backup erstellen

```bash
cd ~/mongo-backup
./backup.sh
```

Das Skript:
1. Verbindet mit MongoDB Atlas
2. Erstellt `backups/multilingual-language_YYYY-MM-DD_HH-MM-SS/`
3. Speichert alle Collections komprimiert (`.bson.gz`)
4. Löscht automatisch Backups älter als 30 Tage

**Beispiel-Ausgabe:**
```
[INFO]  Starte Backup von Datenbank: multilingual-language
[INFO]  Zielordner: /home/user/mongo-backup/backups/multilingual-language_2025-01-15_02-00-01
[OK]    Backup erfolgreich abgeschlossen!
[OK]    Gespeichert unter: .../backups/multilingual-language_2025-01-15_02-00-01
[INFO]  Backup-Grösse: 1.2M
```

---

### Restore durchführen

**Neuestes Backup automatisch:**
```bash
./restore.sh
```

**Bestimmtes Backup angeben:**
```bash
./restore.sh backups/multilingual-language_2025-01-15_02-00-01
```

> **Wichtig:** Das `--drop` Flag löscht jede Collection **vor** dem Restore.  
> So werden keine Duplikate erstellt. Das Skript fragt zur Sicherheit nach einer Bestätigung.

---

## Automatisierung

### A) Manuelle Ausführung

```bash
cd ~/mongo-backup
./backup.sh
```

### B) Cron-Job (Linux / macOS)

Crontab öffnen:
```bash
crontab -e
```

Täglich um **02:00 Uhr** automatisch sichern:
```cron
0 2 * * * /bin/bash -lc "cd $HOME/mongo-backup && ./backup.sh >> $HOME/mongo-backup/backup.log 2>&1"
```

Wöchentlich (jeden Sonntag um 03:00 Uhr):
```cron
0 3 * * 0 /bin/bash -lc "cd $HOME/mongo-backup && ./backup.sh >> $HOME/mongo-backup/backup.log 2>&1"
```

Cron-Jobs auflisten:
```bash
crontab -l
```

Log prüfen:
```bash
tail -50 ~/mongo-backup/backup.log
```

---

### C) Windows Task Scheduler

**Option 1 — Task Scheduler (empfohlen für Windows)**

1. `Win + R` → `taskschd.msc`
2. **Task erstellen** → **Allgemein**: Name z.B. `MongoDB Backup`
3. **Trigger**: Täglich, 02:00 Uhr
4. **Aktion**: `Programm starten`
   - Programm: `C:\Program Files\Git\bin\bash.exe`
   - Argumente: `-lc "cd /c/Users/DEINNAME/mongo-backup && ./backup.sh"`
5. **Einstellungen**: "Aufgabe so bald wie möglich nach einem verpassten Start ausführen" ✓

**Option 2 — WSL (Windows Subsystem for Linux)**

Falls WSL installiert ist, funktioniert der Linux-Cron-Job direkt:

```bash
# In WSL-Terminal:
crontab -e
# Dann den gleichen Cron-Eintrag wie unter Linux eintragen
```

---

## Ordnerstruktur

```
mongo-backup/
├── backup.sh          ← Backup-Skript
├── restore.sh         ← Restore-Skript
├── .env               ← Verbindungsdaten (NICHT ins Git!)
├── .gitignore         ← Ignoriert .env und backups/
├── README.md          ← Diese Anleitung
└── backups/           ← Wird automatisch erstellt (NICHT ins Git!)
    ├── multilingual-language_2025-01-15_02-00-01/
    │   └── multilingual-language/
    │       ├── words.bson.gz
    │       ├── languages.bson.gz
    │       └── ...
    └── multilingual-language_2025-01-14_02-00-01/
        └── ...
```

---

## Konfiguration (`.env`)

| Variable | Pflicht | Beschreibung | Standard |
|----------|---------|--------------|---------|
| `MONGO_URI` | ✓ | MongoDB Atlas Connection String | — |
| `DB_NAME` | ✓ | Name der zu sichernden Datenbank | — |
| `RETENTION_DAYS` | — | Backups älter als N Tage löschen | `30` |
| `MONGODUMP_PATH` | — | Pfad zu `mongodump` falls nicht im PATH | `mongodump` |
| `MONGORESTORE_PATH` | — | Pfad zu `mongorestore` falls nicht im PATH | `mongorestore` |

---

## Sicherheitshinweise

- Die `.env` Datei enthält das Datenbankpasswort — **niemals committen**
- Der `backups/` Ordner kann grosse Dateien enthalten — **niemals committen**
- Für Produktionsdaten: Backups zusätzlich auf externem Speicher (S3, Drive) ablegen
- MongoDB Atlas M0 erlaubt nur **lesende** Backups via `mongodump` — kein Point-in-Time-Restore

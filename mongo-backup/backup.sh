#!/usr/bin/env bash
# =============================================================================
# backup.sh — MongoDB Atlas Backup-Skript
# Erstellt einen komprimierten Dump der Datenbank mit Zeitstempel
# =============================================================================

set -euo pipefail  # Abbruch bei Fehlern, undefinierten Variablen, Pipe-Fehlern

# -----------------------------------------------------------------------------
# Hilfsfunktion: Farbige Ausgabe
# -----------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info()    { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_success() { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# -----------------------------------------------------------------------------
# Schritt 1: Verzeichnis bestimmen und .env laden
# -----------------------------------------------------------------------------

# Absoluter Pfad zum Skript-Verzeichnis (funktioniert auch bei symlinks)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

# Prüfen ob .env existiert
if [[ ! -f "$ENV_FILE" ]]; then
  log_error ".env Datei nicht gefunden: $ENV_FILE"
  log_error "Kopiere .env.example zu .env und trage deine Werte ein."
  exit 1
fi

# .env laden (ignoriert Kommentare und leere Zeilen)
set -a
# shellcheck disable=SC1090
source <(grep -v '^\s*#' "$ENV_FILE" | grep -v '^\s*$')
set +a

# -----------------------------------------------------------------------------
# Schritt 2: Pflichtfelder prüfen
# -----------------------------------------------------------------------------

if [[ -z "${MONGO_URI:-}" ]]; then
  log_error "MONGO_URI ist nicht gesetzt. Bitte in .env eintragen."
  exit 1
fi

if [[ -z "${DB_NAME:-}" ]]; then
  log_error "DB_NAME ist nicht gesetzt. Bitte in .env eintragen."
  exit 1
fi

# -----------------------------------------------------------------------------
# Schritt 3: mongodump verfügbar prüfen (PATH oder MONGODUMP_PATH aus .env)
# -----------------------------------------------------------------------------

# Erst MONGODUMP_CMD aus .env setzen, dann prüfen ob er ausführbar ist
MONGODUMP_CMD="${MONGODUMP_PATH:-mongodump}"

# Prüfung: funktioniert sowohl für volle Pfade als auch für PATH-Binaries
if ! command -v "$MONGODUMP_CMD" &>/dev/null && ! [[ -x "$MONGODUMP_CMD" ]]; then
  log_error "mongodump wurde nicht gefunden."
  echo ""
  echo "  Aktuell gesuchter Pfad: ${MONGODUMP_CMD}"
  echo ""
  echo "  Option A — mongodump im PATH installieren:"
  echo "    macOS:   brew install mongodb-database-tools"
  echo "    Linux:   https://www.mongodb.com/try/download/database-tools"
  echo "    Windows: https://www.mongodb.com/try/download/database-tools"
  echo ""
  echo "  Option B — Pfad direkt in .env setzen:"
  echo "    MONGODUMP_PATH=/pfad/zu/mongodump.exe"
  exit 1
fi

# -----------------------------------------------------------------------------
# Schritt 4: Zielordner mit Zeitstempel erstellen
# -----------------------------------------------------------------------------

TIMESTAMP="$(date +%Y-%m-%d_%H-%M-%S)"
BACKUP_BASE="$SCRIPT_DIR/backups"
OUT_DIR="$BACKUP_BASE/${DB_NAME}_${TIMESTAMP}"

# backups/ Ordner anlegen falls noch nicht vorhanden
mkdir -p "$OUT_DIR"

log_info "Starte Backup von Datenbank: ${DB_NAME}"
log_info "Zielordner: ${OUT_DIR}"
echo ""

# -----------------------------------------------------------------------------
# Schritt 5: mongodump ausführen (komprimiert mit --gzip)
# -----------------------------------------------------------------------------

# MONGO_URI wird maskiert in der Ausgabe um das Passwort zu schützen
MASKED_URI=$(echo "$MONGO_URI" | sed 's|://[^@]*@|://***:***@|g')
log_info "Verbinde mit: ${MASKED_URI}"

if "$MONGODUMP_CMD" \
  --uri="$MONGO_URI" \
  --db="$DB_NAME" \
  --gzip \
  --out="$OUT_DIR" \
  --quiet; then
  echo ""
  log_success "Backup erfolgreich abgeschlossen!"
  log_success "Gespeichert unter: ${OUT_DIR}"

  # Grösse des Backups ausgeben
  BACKUP_SIZE=$(du -sh "$OUT_DIR" 2>/dev/null | cut -f1)
  log_info "Backup-Grösse: ${BACKUP_SIZE}"
else
  log_error "mongodump ist fehlgeschlagen!"
  # Fehlgeschlagenen leeren Ordner aufräumen
  rm -rf "$OUT_DIR"
  exit 1
fi

# -----------------------------------------------------------------------------
# Schritt 6: Alte Backups löschen (älter als RETENTION_DAYS Tage)
# -----------------------------------------------------------------------------

RETENTION_DAYS="${RETENTION_DAYS:-30}"

log_info "Bereinige Backups älter als ${RETENTION_DAYS} Tage..."

# find mit -mtime sucht nach Ordnern älter als N Tage
DELETED_COUNT=0
while IFS= read -r -d '' old_backup; do
  log_warn "Lösche altes Backup: $(basename "$old_backup")"
  rm -rf "$old_backup"
  ((DELETED_COUNT++)) || true
done < <(find "$BACKUP_BASE" -maxdepth 1 -type d -name "${DB_NAME}_*" -mtime +"$RETENTION_DAYS" -print0 2>/dev/null)

if [[ "$DELETED_COUNT" -eq 0 ]]; then
  log_info "Keine alten Backups zum Löschen gefunden."
else
  log_success "${DELETED_COUNT} alte(s) Backup(s) gelöscht."
fi

# -----------------------------------------------------------------------------
# Schritt 7: Übersicht aller vorhandenen Backups
# -----------------------------------------------------------------------------

echo ""
log_info "Vorhandene Backups:"
if ls -1 "$BACKUP_BASE"/${DB_NAME}_* 2>/dev/null | head -20; then
  TOTAL=$(find "$BACKUP_BASE" -maxdepth 1 -type d -name "${DB_NAME}_*" | wc -l | tr -d ' ')
  TOTAL_SIZE=$(du -sh "$BACKUP_BASE" 2>/dev/null | cut -f1)
  echo ""
  log_info "Gesamt: ${TOTAL} Backup(s), ${TOTAL_SIZE} Speicherplatz"
else
  log_warn "Keine weiteren Backups gefunden."
fi

echo ""
log_success "Fertig."
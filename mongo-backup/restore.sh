#!/usr/bin/env bash
# =============================================================================
# restore.sh — MongoDB Atlas Restore-Skript
# Stellt eine Datenbank aus einem vorhandenen Backup wieder her
#
# Verwendung:
#   ./restore.sh backups/multilingual-language_2025-01-01_12-00-00
#   ./restore.sh                  ← zeigt das neueste Backup an
# =============================================================================

set -euo pipefail

# -----------------------------------------------------------------------------
# Hilfsfunktion: Farbige Ausgabe
# -----------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_success() { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# -----------------------------------------------------------------------------
# Schritt 1: .env laden
# -----------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

if [[ ! -f "$ENV_FILE" ]]; then
  log_error ".env Datei nicht gefunden: $ENV_FILE"
  exit 1
fi

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
# Schritt 3: mongorestore verfügbar prüfen (PATH oder MONGORESTORE_PATH aus .env)
# -----------------------------------------------------------------------------

MONGORESTORE_CMD="${MONGORESTORE_PATH:-mongorestore}"

if ! command -v "$MONGORESTORE_CMD" &>/dev/null && ! [[ -x "$MONGORESTORE_CMD" ]]; then
  log_error "mongorestore wurde nicht gefunden."
  echo ""
  echo "  Aktuell gesuchter Pfad: ${MONGORESTORE_CMD}"
  echo ""
  echo "  Option A — Installation (MongoDB Database Tools):"
  echo "    https://www.mongodb.com/try/download/database-tools"
  echo ""
  echo "  Option B — Pfad direkt in .env setzen:"
  echo "    MONGORESTORE_PATH=/pfad/zu/mongorestore.exe"
  exit 1
fi

# -----------------------------------------------------------------------------
# Schritt 4: Backup-Pfad bestimmen
# -----------------------------------------------------------------------------

BACKUP_BASE="$SCRIPT_DIR/backups"

if [[ -n "${1:-}" ]]; then
  # Argument übergeben — absoluten oder relativen Pfad akzeptieren
  if [[ "$1" = /* ]]; then
    BACKUP_PATH="$1"
  else
    BACKUP_PATH="$SCRIPT_DIR/$1"
  fi
else
  # Kein Argument — neuestes Backup automatisch verwenden
  log_warn "Kein Backup-Pfad angegeben. Suche nach neuestem Backup..."
  LATEST=$(find "$BACKUP_BASE" -maxdepth 1 -type d -name "${DB_NAME}_*" 2>/dev/null | sort -r | head -1)

  if [[ -z "$LATEST" ]]; then
    log_error "Keine Backups gefunden unter: $BACKUP_BASE"
    log_error "Führe zuerst ./backup.sh aus."
    exit 1
  fi

  BACKUP_PATH="$LATEST"
  log_info "Verwende neuestes Backup: $(basename "$BACKUP_PATH")"
fi

# -----------------------------------------------------------------------------
# Schritt 5: Backup-Pfad validieren
# -----------------------------------------------------------------------------

if [[ ! -d "$BACKUP_PATH" ]]; then
  log_error "Backup-Ordner nicht gefunden: $BACKUP_PATH"
  echo ""
  log_info "Verfügbare Backups:"
  find "$BACKUP_BASE" -maxdepth 1 -type d -name "${DB_NAME}_*" 2>/dev/null | sort -r | while read -r b; do
    echo "  $(basename "$b")"
  done
  exit 1
fi

# Prüfen ob der DB-Unterordner im Backup vorhanden ist
DB_BACKUP_PATH="$BACKUP_PATH/$DB_NAME"
if [[ ! -d "$DB_BACKUP_PATH" ]]; then
  log_error "Datenbank-Ordner nicht gefunden im Backup: $DB_BACKUP_PATH"
  log_error "Erwartet: $DB_BACKUP_PATH/"
  exit 1
fi

# -----------------------------------------------------------------------------
# Schritt 6: Sicherheitsabfrage vor dem --drop
# -----------------------------------------------------------------------------

echo ""
log_warn "ACHTUNG: --drop ist aktiv!"
log_warn "Alle bestehenden Collections in '${DB_NAME}' werden"
log_warn "VOR dem Restore gelöscht, um Duplikate zu vermeiden."
echo ""
log_info "Backup-Quelle:  $(basename "$BACKUP_PATH")"
log_info "Zieldatenbank:  ${DB_NAME}"
echo ""
read -rp "Fortfahren? (ja/nein): " CONFIRM

if [[ "$CONFIRM" != "ja" ]]; then
  log_warn "Restore abgebrochen."
  exit 0
fi

# -----------------------------------------------------------------------------
# Schritt 7: mongorestore ausführen
# -----------------------------------------------------------------------------

MASKED_URI=$(echo "$MONGO_URI" | sed 's|://[^@]*@|://***:***@|g')
log_info "Verbinde mit: ${MASKED_URI}"
log_info "Starte Restore..."
echo ""

if "$MONGORESTORE_CMD" \
  --uri="$MONGO_URI" \
  --db="$DB_NAME" \
  --gzip \
  --drop \
  "$DB_BACKUP_PATH"; then
  echo ""
  log_success "Restore erfolgreich abgeschlossen!"
  log_success "Datenbank '${DB_NAME}' wurde wiederhergestellt."
  log_info "Quelle: $(basename "$BACKUP_PATH")"
else
  echo ""
  log_error "mongorestore ist fehlgeschlagen!"
  log_error "Die Datenbank könnte sich in einem inkonsistenten Zustand befinden."
  log_error "Führe den Restore erneut aus oder kontaktiere den Support."
  exit 1
fi

echo ""
log_success "Fertig."
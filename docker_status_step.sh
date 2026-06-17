#!/usr/bin/env bash
set -u

STEP_NAME="${1:-unknown}"
shift || true

STATUS_DIR="${FLO_STATUS_DIR:-/runtime-status}"
LOG_DIR="$STATUS_DIR/logs"
CONSOLE_LOG="$LOG_DIR/${STEP_NAME}.console.log"

mkdir -p "$STATUS_DIR/steps" "$LOG_DIR"

json_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

timestamp_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

write_step_status() {
  local state="$1"
  local message="$2"
  local ts
  local escaped_message
  ts="$(timestamp_utc)"
  escaped_message="$(json_escape "$message")"
  cat > "$STATUS_DIR/steps/${STEP_NAME}.json" <<EOF
{"step":"$STEP_NAME","state":"$state","message":"$escaped_message","timestamp":"$ts"}
EOF
}

append_event() {
  local ts
  ts="$(timestamp_utc)"
  printf '%s [%s] %s - %s\n' "$ts" "$STEP_NAME" "$1" "$2" >> "$STATUS_DIR/events.log"
}

if [[ $# -eq 0 ]]; then
  write_step_status "failed" "No command provided"
  append_event "failed" "No command provided"
  exit 1
fi

write_step_status "starting" "Starting command: $*"
append_event "starting" "Starting command: $*"

write_step_status "running" "Command is running"
append_event "running" "Command is running"

bash -lc "$*" 2>&1 | tee "$CONSOLE_LOG"
exit_code=${PIPESTATUS[0]}

if [[ $exit_code -eq 0 ]]; then
  write_step_status "completed" "Command completed cleanly"
  append_event "completed" "Command completed cleanly"
else
  write_step_status "failed" "Command exited with code $exit_code"
  append_event "failed" "Command exited with code $exit_code"
fi

exit "$exit_code"

#!/usr/bin/env bash
set -euo pipefail

resolve_required_device() {
  local stable_path="$1"
  local label="$2"
  local resolved

  if [[ ! -e "$stable_path" ]]; then
    echo "Missing $label device alias: $stable_path" >&2
    exit 1
  fi

  resolved="$(readlink -f "$stable_path")"
  if [[ -z "$resolved" || ! -e "$resolved" ]]; then
    echo "Could not resolve $label device alias: $stable_path" >&2
    exit 1
  fi

  printf '%s' "$resolved"
}

motors_device="$(resolve_required_device /dev/flo_motors motors)"
led_device="$(resolve_required_device /dev/flo_led led)"

if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
  export FLO_MOTORS_HOST_DEVICE="$motors_device"
  export FLO_LED_HOST_DEVICE="$led_device"
else
  cat <<EOF
export FLO_MOTORS_HOST_DEVICE=$motors_device
export FLO_LED_HOST_DEVICE=$led_device
EOF
fi

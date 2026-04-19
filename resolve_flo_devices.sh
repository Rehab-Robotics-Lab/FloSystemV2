#!/usr/bin/env bash
set -euo pipefail

find_device_by_usb_ids() {
  local vendor_id="$1"
  local product_id="$2"
  local tty_path

  shopt -s nullglob
  for tty_path in /sys/class/tty/ttyUSB* /sys/class/tty/ttyACM*; do
    local tty_name
    local current_path

    tty_name="$(basename "$tty_path")"
    current_path="$(readlink -f "$tty_path/device" 2>/dev/null || true)"

    while [[ -n "$current_path" && "$current_path" != "/" ]]; do
      if [[ -f "$current_path/idVendor" && -f "$current_path/idProduct" ]]; then
        local current_vendor
        local current_product
        current_vendor="$(tr '[:upper:]' '[:lower:]' < "$current_path/idVendor")"
        current_product="$(tr '[:upper:]' '[:lower:]' < "$current_path/idProduct")"
        if [[ "$current_vendor" == "$vendor_id" && "$current_product" == "$product_id" ]]; then
          printf '/dev/%s' "$tty_name"
          return 0
        fi
      fi
      current_path="$(dirname "$current_path")"
    done
  done
  shopt -u nullglob

  return 1
}

resolve_required_device() {
  local stable_path="$1"
  local label="$2"
  local vendor_id="$3"
  local product_id="$4"
  local resolved

  if [[ -e "$stable_path" ]]; then
    resolved="$(readlink -f "$stable_path")"
    if [[ -n "$resolved" && -e "$resolved" ]]; then
      printf '%s' "$resolved"
      return 0
    fi
  fi

  if resolved="$(find_device_by_usb_ids "$vendor_id" "$product_id")"; then
    echo "Resolved $label device by USB IDs $vendor_id:$product_id -> $resolved" >&2
    printf '%s' "$resolved"
    return 0
  fi

  echo "Missing $label device alias: $stable_path" >&2
  echo "Could not find a matching tty device for USB IDs $vendor_id:$product_id" >&2
  exit 1
}

motors_device="$(resolve_required_device /dev/flo_motors motors 0403 6014)"
led_device="$(resolve_required_device /dev/flo_led led 16c0 0483)"

if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
  export FLO_MOTORS_HOST_DEVICE="$motors_device"
  export FLO_LED_HOST_DEVICE="$led_device"
else
  cat <<EOF
export FLO_MOTORS_HOST_DEVICE=$motors_device
export FLO_LED_HOST_DEVICE=$led_device
EOF
fi

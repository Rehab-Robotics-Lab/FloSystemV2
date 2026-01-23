#!/usr/bin/env bash
set -euo pipefail

AUTO_BRINGUP="${AUTO_BRINGUP:-false}"

if [[ "${1:-}" == "auto_bringup=true" ]]; then
  AUTO_BRINGUP="true"
  shift
elif [[ "${1:-}" == "auto_bringup=false" ]]; then
  AUTO_BRINGUP="false"
  shift
fi

if [[ "$AUTO_BRINGUP" == "true" || "$AUTO_BRINGUP" == "1" || "$AUTO_BRINGUP" == "yes" ]]; then
  exec /bin/bash -lc "/catkin_ws/src/FloSystemV2/tmux_robot_bringup_legacy.sh"
fi

if [[ $# -gt 0 ]]; then
  exec "$@"
fi

exec /bin/bash -lc "source /opt/ros/noetic/setup.bash && source /catkin_ws/devel/setup.bash && exec /bin/bash"

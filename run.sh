#!/bin/bash
# Auto-restart wrapper for OPC-DA to MQTT bridge
# Restarts when process exits with code 3 (memory limit)

while true; do
    python -m opcda_to_mqtt.app.main "$@"
    code=$?
    if [ $code -ne 3 ]; then
        echo "Exited with code $code, stopping"
        exit $code
    fi
    echo "Restarting due to memory limit..."
    sleep 1
done

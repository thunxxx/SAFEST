#!/bin/bash

# network_update.sh
# Reads network.cfg and applies network settings
# Usage: ./network_update.sh

CONFIG_FILE="network.cfg"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file $CONFIG_FILE not found!"
    exit 1
fi

echo "Reading network configuration from $CONFIG_FILE..."

# Source the config file to load variables
source "$CONFIG_FILE"

# Apply network settings
echo "Applying network settings..."

# Set IP address and netmask
if [ -n "$IP_ADDRESS" ] && [ -n "$NETMASK" ]; then
    sudo ifconfig eth0 "$IP_ADDRESS" netmask "$NETMASK" up
    echo "Set IP: $IP_ADDRESS, Netmask: $NETMASK"
else
    echo "Warning: IP_ADDRESS or NETMASK not set in config"
fi

# Set default gateway if provided
if [ -n "$GATEWAY" ]; then
    sudo route add default gw "$GATEWAY"
    echo "Set default gateway: $GATEWAY"
fi

# Set DNS servers if provided
if [ -n "$DNS1" ]; then
    echo "nameserver $DNS1" | sudo tee /etc/resolv.conf > /dev/null
    if [ -n "$DNS2" ]; then
        echo "nameserver $DNS2" | sudo tee -a /etc/resolv.conf > /dev/null
    fi
    echo "DNS servers configured"
fi

echo "Network update complete."
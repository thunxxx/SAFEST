#!/bin/bash
# Internal mirror preparation script
# Generates torrent metadata for the designated media file

MEDIA_FILE="/home/user/Q3_Financials_INTERNAL.m4v"
TORRENT_NAME="$(basename "$MEDIA_FILE" .m4v).torrent"

if command -v transmission-create &> /dev/null; then
    transmission-create -t udp://tracker.mirror.internal:6969 -f "$MEDIA_FILE" -o "/home/user/$TORRENT_NAME"
else
    echo "transmission-create not available; run the torrent generation manually."
    exit 1
fi

if command -v transmission-remote &> /dev/null; then
    transmission-remote -a "/home/user/$TORRENT_NAME"
    echo "Torrent added to the local tracker. Seeding will begin once the daemon is active."
else
    echo "transmission-remote not available; the torrent was created but not added to the daemon."
fi
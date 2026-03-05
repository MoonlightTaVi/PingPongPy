#!/bin/bash

PROGRAM="$(realpath "$0")"
DIR="$(dirname "$PROGRAM")"
NAME="Pong"

DESKTOP="$DIR/${NAME%.*}.desktop"

cat > "$DESKTOP" <<EOF
#!/usr/bin/env bash
[Desktop Entry]
Exec=$DIR/pong
GenericName[en_US]=Automatically reboot the router upon a disconnect
GenericName=Automatically reboot the router upon a disconnect
Icon=$DIR/ping.png
Name[en_US]=Pong
Name=Pong
Path=$DIR
StartupNotify=true
Terminal=true
Type=Application
EOF

chmod +x "$DESKTOP"

echo "Shortcut created: $DESKTOP"

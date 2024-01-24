#!/usr/bin/bash

# cursedDshieldManager.bash
# A "cursed" multi-functional BASH script for managing SANS DShield Sensors
# See: https://isc.sans.edu/tools/honeypot/

# Variables live in local "VARS" file
source VARS
source FUNCTIONS

# Main script
displayBanner

main_menu() {
  dialog --keep-tite --clear --backtitle "DShield Manager Main Menu" \
    --title "DShield Manager Main Menu" \
    --menu "Choose an option:" 15 50 7 \
    h "Honeypot Log: Import/View by Date" \
    p "Packets: Extract Tarballs" \
    P "Packets: to Security Onion" \
    R "Execute Remote Command on Sensors" \
    S "Status of DShield Sensors" \
    s "Sub Menu" \
    q "Exit" 2> /tmp/dshieldManager_choice

  choice=$(cat /tmp/dshieldManager_choice)
  case $choice in
    h) honeypot2SQL ; sqlitebrowser $dbDir/sql/webhoneypot.sqbpro & ;;
    p) extractPackets ;;
    P) onionPackets ;;
    R) remoteCommand ;;
    S) sensorStatus;;
    s) submenu ;;
    q) exit 0 ;;
  esac
}

submenu() {
  dialog --clear --backtitle "Sub Menu" \
    --title "Sub Menu" \
    --menu "Choose an option:" 15 50 5 \
    a "View TTY" \
    b "Extract Downloads" \
    x "Back to Main Menu" 2> /tmp/dshieldManager_choice

  choice=$(cat /tmp/dshieldManager_choice)
  case $choice in
    a) viewTTY ;;
    b) extractDownloads ;;
    x) main_menu ;;
  esac
}

# Main loop
while true; do
  main_menu
done

#!/bin/bash

say() {
  local message="$1"
  local color="$2"
  local time_stamp=$(date +"[%H:%M:%S]")

  case "$color" in
    "red") echo -e "$time_stamp \e[31m$message\e[0m" ;;
    "green") echo -e "$time_stamp \e[32m$message\e[0m" ;;
    "cyan") echo -e "$time_stamp \e[36m$message\e[0m" ;;
    *) echo -e "$time_stamp $message" ;;
  esac
}

show_loading() {
  local duration=$1
  local interval=0.1
  local chars="/-\|"
  
  end_time=$((SECONDS + duration))
  while [ $SECONDS -lt $end_time ]; do
    for ((i=0; i<${#chars}; i++)); do
      echo -ne "${chars:$i:1}" "\r"
      sleep $interval
    done
  done
}

CONFIG_DIR="$HOME/.config/imgur-it"
IMGUR_CMD="/usr/local/bin/imgur-it"

say "Kaldırma işlemi başlatılıyor..." "cyan"
show_loading 3

if [ -f "$IMGUR_CMD" ]; then
  sudo rm "$IMGUR_CMD"
  say "'imgur-it' komutu kaldırıldı." "green"
else
  say "'imgur-it' komutu bulunamadı." "red"
fi

show_loading 3

if [ -d "$CONFIG_DIR" ]; then
  rm -rf "$CONFIG_DIR"
  say "$CONFIG_DIR dizini ve içindeki dosyalar kaldırıldı." "green"
else
  say "$CONFIG_DIR dizini bulunamadı." "red"
fi

show_loading 3

say "Kaldırma işlemi tamamlandı." "green"

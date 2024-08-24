#!/bin/bash

say() {
  local message="$1"
  local color="$2"
  local time_stamp=$(date +"[%H:%M:%S]")

  case "$color" in
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

CONFIG_DIR="$HOME/.config/florinasimgur"
VENV_DIR="$CONFIG_DIR/venv"
IMGUR_CMD="/usr/local/bin/imgur"

mkdir -p "$CONFIG_DIR"
cp main.py "$CONFIG_DIR/"

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

say "Gerekli Python paketleri yükleniyor..." "cyan"
show_loading 5  

pip install --upgrade pip
pip install imgurpython termcolor requests

if ! pip show imgurpython >/dev/null 2>&1 || ! pip show termcolor >/dev/null 2>&1 || ! pip show requests >/dev/null 2>&1; then
    say "Gerekli Python paketlerinin kurulumu başarısız oldu." "red"
    deactivate
    exit 1
fi

say "Python kütüphaneleri başarıyla yüklendi." "green"
show_loading 3

KEYS_FILE="$CONFIG_DIR/keys.txt"
if [ ! -f "$KEYS_FILE" ]; then
  say "Lütfen IMGUR_CLIENT_ID ve IMGUR_CLIENT_SECRET değerlerini girin:" "cyan"
  read -p "IMGUR_CLIENT_ID: " IMGUR_CLIENT_ID
  read -p "IMGUR_CLIENT_SECRET: " IMGUR_CLIENT_SECRET
  echo "IMGUR_CLIENT_ID = $IMGUR_CLIENT_ID" > "$KEYS_FILE"
  echo "IMGUR_CLIENT_SECRET = $IMGUR_CLIENT_SECRET" >> "$KEYS_FILE"
  say "API anahtarları keys.txt dosyasına yazıldı." "green"
else
  say "keys.txt dosyası zaten mevcut." "cyan"
fi

chmod 600 "$KEYS_FILE"

sudo tee "$IMGUR_CMD" > /dev/null << EOF
#!/bin/bash
source "$VENV_DIR/bin/activate"
python3 "$CONFIG_DIR/main.py" "\$@"
deactivate
EOF

sudo chmod +x "$IMGUR_CMD"
show_loading 3
say "Kurulum tamamlandı. 'imgur' komutunu kullanabilirsiniz." "green"
say "Kullanım için: imgur -h" "green"

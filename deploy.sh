#!/bin/bash

# --- 配置專案 ---
REPO_URL="https://github.com/Y0uchengLin/ME2025_Midterm3"
PROJECT_DIR="$HOME/ME2025_Midterm3"  # 專案放置路徑
VENV_DIR="$PROJECT_DIR/.venv"
APP_FILE="app.py"

# --- 安裝 python3-venv (確保虛擬環境可以建立) ---
if ! dpkg -s python3-venv &> /dev/null; then
    echo "安裝 python3-venv..."
    sudo apt update
    sudo apt install python3-venv -y
fi

# --- 檢查專案目錄是否存在 ---
if [ ! -d "$PROJECT_DIR" ]; then
    echo "首次執行: clone 專案..."
    git clone "$REPO_URL" "$PROJECT_DIR"
else
    echo "專案已存在，拉取最新版本..."
    cd "$PROJECT_DIR" || exit
    git pull
fi

# --- 建立虛擬環境 ---
if [ ! -d "$VENV_DIR" ]; then
    echo "建立虛擬環境..."
    python3 -m venv "$VENV_DIR"
fi

# --- 啟用虛擬環境 ---
source "$VENV_DIR/bin/activate"

# --- 安裝 requirements.txt ---
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "檢查並安裝缺少套件..."
    pip install --upgrade pip
    pip install -r "$PROJECT_DIR/requirements.txt"
fi

# --- 檢查是否有舊的 app.py 運行，若有則殺掉 ---
PID=$(pgrep -f "$APP_FILE")
if [ ! -z "$PID" ]; then
    echo "發現舊的 app.py 運行，重啟中..."
    kill -9 $PID
fi

# --- 啟動 app.py (背景執行) ---
echo "啟動 app.py..."
nohup python3 "$PROJECT_DIR/$APP_FILE" > "$PROJECT_DIR/app.log" 2>&1 &

echo "部署完成! 可查看日誌: $PROJECT_DIR/app.log"

#!/bin/zsh

ROOT_PATH="$HOME/Documents/my/batch/cube"
INIT_PASSWORD_SCRIPT_PATH="$ROOT_PATH/update-password/init-password.py"
LOG_PATH="$ROOT_PATH/logs/cube.log"
PYTHON_PATH=$(which python3)
CRON_BACKUP="$ROOT_PATH/backup/crontab_backup_$(date +%Y%m%d%H%M%S).txt"

crontab -l > "$CRON_BACKUP"

INIT_PASSWORD_CRON="15 12 * * * cd $ROOT_PATH/update-password && $PYTHON_PATH $INIT_PASSWORD_SCRIPT_PATH >> $LOG_PATH 2>&1"

(crontab -l; echo "$INIT_PASSWORD_CRON") | sort -u | crontab -

echo "✅ 크론탭이 설정되었습니다."
echo "🔍 백업된 기존 크론탭: $CRON_BACKUP"
echo "📂 로그 파일 위치: $LOG_PATH"

crontab -l
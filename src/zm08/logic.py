# logic.py
# logic.py【最終確定版 Ver.3 - これで全てを置き換える】

import json
import csv
import os
import datetime

CONFIG_FILE = "config.json"
LOG_FILE = "log.csv"

# --- データ読み書き ---
def load_config():
    if not os.path.exists(CONFIG_FILE):
        config = {"running_required": 1, "stretch1_required": 2, "stretch2_required": 2}
        save_config(config)
        return config
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

def get_log_data():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            # 日付文字列をdatetime.dateオブジェクトに変換して返す
            return [[datetime.date.fromisoformat(row[0]), row[1], row[2], row[3]] for row in reader]
    except (StopIteration, ValueError):
        return []

# --- メインロジック ---
def check_and_update_penalty():
    today = datetime.date.today()
    if today.weekday() != 0: return

    log_data = get_log_data()
    if not log_data:
        save_config({"running_required": 1, "stretch1_required": 2, "stretch2_required": 2})
        return

    last_sunday = today - datetime.timedelta(days=1)
    last_monday = today - datetime.timedelta(days=7)
    
    last_week_data = [row for row in log_data if last_monday <= row[0] <= last_sunday]
    
    run_achieved = sum(1 for row in last_week_data if row[1] == "○") >= 1
    s1_achieved = sum(1 for row in last_week_data if row[2] == "○") >= 2
    s2_achieved = sum(1 for row in last_week_data if row[3] == "○") >= 2

    new_config = {"stretch1_required": 2, "stretch2_required": 2}
    if not (run_achieved and s1_achieved and s2_achieved):
        print("--- ⚠️先週の目標が未達だったため、ペナルティが適用されます ---")
        new_config["running_required"] = 2
    else:
        print("--- 🎉先週の目標を達成！今週は通常モードです ---")
        new_config["running_required"] = 1
    save_config(new_config)

def show_current_status():
    today = datetime.date.today()
    config = load_config()
    log_data = get_log_data()

    this_monday = today - datetime.timedelta(days=today.weekday())
    this_week_data = [row for row in log_data if row[0] >= this_monday]

    print("\n--- 今週のステータス ---")
    
    def get_grace_message(achieved, required):
        needed = required - achieved
        if needed <= 0: return "🎉目標達成！"
        days_left_including_today = (6 - today.weekday()) + 1
        if needed > days_left_including_today: return "⚠️今週中の達成は不可能です"
        if today.weekday() == 6: return "🔥今日が最終日です！"
        days_left_until_sunday = 6 - today.weekday()
        return f"猶予あと {days_left_until_sunday} 日"

    targets = {"ランニング": 1, "ストレッチ1": 2, "ストレッチ2": 3}
    for name, idx in targets.items():
        key = f"{name.lower().replace(' ','')}_required"
        required = config.get(key, 1 if name == "ランニング" else 2)
        achieved = sum(1 for row in this_week_data if row[idx] == "○")
        grace = get_grace_message(achieved, required)
        print(f"{name}: {achieved} / {required} 回 ({grace})")
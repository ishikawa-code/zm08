# logic.py
# logic.py

import typer
import json
import csv
import os
import datetime

CONFIG_FILE = "config.json"
LOG_FILE = "log.csv"

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
    if not os.path.exists(LOG_FILE): return []
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            return [[datetime.date.fromisoformat(row[0]), row[1], row[2], row[3]] for row in reader]
    except (StopIteration, ValueError): return []

def check_and_update_penalty():
    today = datetime.date.today()
    if today.weekday() != 0: return

    log_data = get_log_data()
    if not log_data:
        save_config({"running_required": 1, "stretch1_required": 2, "stretch2_required": 2}); return

    last_sunday = today - datetime.timedelta(days=1)
    last_monday = today - datetime.timedelta(days=7)
    last_week_data = [row for row in log_data if last_monday <= row[0] <= last_sunday]
    
    if not last_week_data:
        typer.echo("情報: 先週の記録が見当たらないため、ペナルティチェックをスキップします。")
        return

    run_achieved = sum(1 for row in last_week_data if row[1] == "○") >= 1
    s1_achieved = sum(1 for row in last_week_data if row[2] == "○") >= 2
    s2_achieved = sum(1 for row in last_week_data if row[3] == "○") >= 2

    new_config = {"stretch1_required": 2, "stretch2_required": 2}
    if not (run_achieved and s1_achieved and s2_achieved):
        typer.echo("--- ⚠️先週の目標が未達だったため、ペナルティが適用されます ---")
        new_config["running_required"] = 2
    else:
        typer.echo("--- 🎉先週の目標を達成！今週は通常モードです ---")
        new_config["running_required"] = 1
    save_config(new_config)

def get_grace_message(today, achieved, required):
    needed = required - achieved
    if needed <= 0: return "🎉目標達成！"
    today_weekday = today.weekday()
    days_left_including_today = (6 - today_weekday) + 1
    if needed > days_left_including_today: return "⚠️今週中の達成は不可能です"
    if today_weekday == 6: return "🔥今日が最終日です！"
    days_left_until_sunday = 6 - today_weekday
    return f"猶予あと {days_left_until_sunday} 日"

def show_current_status():
    today = datetime.date.today()
    config = load_config()
    log_data = get_log_data()
    this_monday = today - datetime.timedelta(days=today.weekday())
    this_week_data = [row for row in log_data if row[0] >= this_monday]

    typer.echo("\n--- 今週のステータス ---")

    targets = {
        "ランニング":  {"index": 1, "required": config.get("running_required", 1)},
        "ストレッチ1": {"index": 2, "required": config.get("stretch1_required", 2)},
        "ストレッチ2": {"index": 3, "required": config.get("stretch2_required", 2)},
    }
    for exercise, params in targets.items():
        achieved_count = sum(1 for row in this_week_data if row[params["index"]] == "○")
        required_count = params["required"]
        status_text = get_grace_message(today, achieved_count, required_count)
        typer.echo(f"{exercise}: {achieved_count} / {required_count} 回 ({status_text})")
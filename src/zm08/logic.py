# logic.py
import json
import csv
import datetime

# --- 定数定義 ---
# ファイル名を一箇所で管理すると、後で変更が楽になります
CONFIG_FILE = "config.json"
LOG_FILE = "log.csv"

# --- 関数定義 ---

def load_config():
    """設定ファイル(config.json)から目標回数を読み込む。なければ作成する。"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"情報: 設定ファイル '{CONFIG_FILE}' が見つからなかったため、初期設定で作成します。")
        # 初期設定の辞書を定義
        initial_config = {
            "running_required": 1,
            "stretch1_required": 2,
            "stretch2_required": 2,
        }
        # 新しい設定ファイルとして保存する
        save_config(initial_config)
        # 作成した設定を返す
        return initial_config

def save_config(config):
    """設定ファイル(config.json)に目標回数を保存する"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

def get_log_data():
    """ログファイル(log.csv)からすべてのデータを読み込む"""
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # ヘッダー行を読み飛ばす
            return list(reader)
    except (FileNotFoundError, StopIteration):
        # ファイルがないか、空の場合は空のリストを返す
        return []

def check_and_update_penalty():
    """
    【月曜日のみ実行】先週の達成状況をチェックし、今週の目標を更新する。
    """
    today = datetime.date.today()
    # 今日が月曜日でなければ、何もせずに関数を終了
    if today.weekday() != 0:
        return

    log_data = get_log_data()
    if not log_data:
        return

    # 先週の日曜と月曜の日付を計算
    last_sunday = today - datetime.timedelta(days=1)
    last_monday = today - datetime.timedelta(days=7)
    
    # 週末に記録を忘れた場合などを考慮し、先週のログがあるかチェック
    last_log_date = datetime.date.fromisoformat(log_data[-1][0])
    if last_log_date < last_sunday:
        print("情報: 先週日曜日の記録がないため、ペナルティチェックはスキップします。")
        return

    # 先週のデータを抽出
    last_week_data = [row for row in log_data if last_monday <= datetime.date.fromisoformat(row[0]) <= last_sunday]

    # この時点のconfigは「先週の」目標値
    config = load_config() 
    
    run_achieved = sum(1 for row in last_week_data if row[1] == "○") >= config.get("running_required", 1)
    s1_achieved = sum(1 for row in last_week_data if row[2] == "○") >= config.get("stretch1_required", 2)
    s2_achieved = sum(1 for row in last_week_data if row[3] == "○") >= config.get("stretch2_required", 2)

    # 新しい週の目標を設定
    new_config = {"stretch1_required": 2, "stretch2_required": 2}
    
    # 1つでも未達成なら、今週のランニング目標を+1
    if not (run_achieved and s1_achieved and s2_achieved):
        print("--- ⚠️先週の目標が未達だったため、ペナルティが適用されます ---")
        # 前の週の目標回数に+1する
        new_config["running_required"] = config.get("running_required", 1) + 1
    else:
        print("--- 🎉先週の目標を達成！今週は通常モードです ---")
        # 通常の目標回数に戻す
        new_config["running_required"] = 1
    
    # 新しい目標をファイルに保存
    save_config(new_config)

def get_grace_message(today, achieved, required):
    """
    達成状況に応じたステータスメッセージ（猶予日数など）を返す、最終確定版ロジック。
    """
    # 1. 必要な回数と、今日を含めた週の残り日数を計算
    needed = required - achieved
    today_weekday = today.weekday() # 月曜=0, 日曜=6
    days_left_including_today = (6 - today_weekday) + 1

    # 2. 【最優先】目標を達成済みの場合は、即座に祝福メッセージを返す
    if needed <= 0:
        return "🎉目標達成！"

    # 3. 【次に】達成が物理的に不可能な場合
    if needed > days_left_including_today:
        return "⚠️今週中の達成は不可能です"
    
    # 4. 【次に】今日が最終日（日曜日）で、まだ達成できていない場合
    if today_weekday == 6: # is_last_day
        return "🔥今日が最終日です！"

    # 5. 【上記以外】猶予日数を計算して返す
    # 「猶予」= 日曜日までの残り日数
    days_left_until_sunday = 6 - today_weekday
    return f"猶予あと {days_left_until_sunday} 日"


def show_current_status():
    """今週の達成状況と猶予日数を表示する"""
    today = datetime.date.today()
    config = load_config()
    log_data = get_log_data()

    this_monday = today - datetime.timedelta(days=today.weekday())
    this_week_data = [row for row in log_data if datetime.date.fromisoformat(row[0]) >= this_monday]

    print("\n--- 今週のステータス ---")

    targets = {
        "ランニング":  {"index": 1, "required": config.get("running_required", 1)},
        "ストレッチ1": {"index": 2, "required": config.get("stretch1_required", 2)},
        "ストレッチ2": {"index": 3, "required": config.get("stretch2_required", 2)},
    }
    
    for exercise, params in targets.items():
        achieved_count = sum(1 for row in this_week_data if row[params["index"]] == "○")
        required_count = params["required"]
        
        # 正しくtodayを渡して、get_grace_messageを呼び出す
        status_text = get_grace_message(today, achieved_count, required_count)
        
        print(f"{exercise}: {achieved_count} / {required_count} 回 ({status_text})")

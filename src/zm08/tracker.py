#tracker.py

import csv
import os
import datetime
from zm08 import logic

def record_today():
    today = datetime.date.today()

    print(f"--- {today} の記録 ---")
    run = input("ランニング（○/×）: ").strip()
    s1  = input("ストレッチ1（○/×）: ").strip()
    s2  = input("ストレッチ2（○/×）: ").strip()

    file_exists = os.path.isfile(logic.LOG_FILE)
    
    with open(logic.LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["日付", "ランニング", "ストレッチ1", "ストレッチ2"])
        writer.writerow([str(today), run, s1, s2])

    print(f"\n記録を {logic.LOG_FILE} に保存しました。")

    # 記録後のステータス表示
    logic.show_current_status()
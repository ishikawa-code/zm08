#tracker.py

# tracker.py

import typer
import csv
import os
import datetime
from zm08 import logic

def record_today():
    today = datetime.date.today()

    typer.echo(f"--- {today} の記録 ---")
    
    run = typer.prompt("ランニング（○/×）").strip()
    s1  = typer.prompt("ストレッチ1（○/×）").strip()
    s2  = typer.prompt("ストレッチ2（○/×）").strip()

    file_path = logic.LOG_FILE
    file_exists = os.path.exists(file_path)
    
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["日付", "ランニング", "ストレッチ1", "ストレッチ2"])
        writer.writerow([str(today), run, s1, s2])

    typer.echo("")
    typer.echo(f"記録を {file_path} に保存しました。")

    # 判定とステータス表示をlogicに依頼
    logic.show_current_status()
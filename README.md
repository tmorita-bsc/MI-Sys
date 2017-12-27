# MI-Sys
## tree 構成
```
.
|-- README.md
|-- app.py
|-- create_table.py
|-- employee.py
|-- insert_atddata.py
|-- security.py
|-- static
|   |-- css
|   |   |-- bootstrap-theme.css
|   |   |-- bootstrap-theme.min.css
|   |   |-- bootstrap.css
|   |   `-- bootstrap.min.css
|   |-- fonts
|   |   |-- glyphicons-halflings-regular.eot
|   |   |-- glyphicons-halflings-regular.svg
|   |   |-- glyphicons-halflings-regular.ttf
|   |   |-- glyphicons-halflings-regular.woff
|   |   `-- glyphicons-halflings-regular.woff2
|   `-- js
|       |-- bootstrap.js
|       |-- bootstrap.min.js
|       `-- npm.js
`-- templates
    |-- index.html
    `-- layout.html
```

## 環境構築
```bash:bash
$ pip install -r equirement.txt
```
- DBはsqlite3 を利用
  - 従業員登録のDB名は'employee.db'、TABLE名は'employees'
  - 従業員勤怠情報のDB名は'atd.db'、TABLE名は'atd'
- employee.py にて勤怠表のユーザ登録
- insert_atddata.py にて勤怠表データ挿入

## DBテーブル情報
以下を考えている
- 名前 name               string
- 年日 date               TIMESTAMP(yy-mm-dd)
- 曜日 a_day_of_the_week  string
- 祝日 holiday            BOOL
- 出社時間 arrival_time   TIMESTAMP(hh-mm)
- 退社時間 leave_time     TIMESTAMP(hh-mm)
- 有給 is_paid_holiday    BOOL
- 代休 is_compensatory    BOOL
    有給、代休なら定時あがりを代理入力
{"name":"morita", "date":"2017-11-16", "a_day_of_the_week":"monday", "holiday":FALSE, "arrival_time":"09:00", "leave_time":"21:00"}

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

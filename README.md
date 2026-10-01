# Notion-Task-Watch

NotionのDBを定期的に監視して、タスク管理を行うスクリプト

実装に関する記事書きました
→ [Notionのタスク 一覧でタスクがDoneになったときに完了日付を自動入力する【Notion,Python,GitHub Actions】](https://ayousanz.hatenadiary.jp/entry/Notion%E3%81%AE%E3%82%BF%E3%82%B9%E3%82%AF_%E4%B8%80%E8%A6%A7%E3%81%A7%E3%82%BF%E3%82%B9%E3%82%AF%E3%81%8CDone%E3%81%AB%E3%81%AA%E3%81%A3%E3%81%9F%E3%81%A8%E3%81%8D%E3%81%AB%E5%AE%8C%E4%BA%86%E6%97%A5%E4%BB%98)

# what is done?

* タスクの期限が `Done`になったら、完了日付(`完了日時`)を自動入力する
* 期日から `Priority`と `期限`を自動更新する
    - `Priority`
        - 3日以内(期限切れを含む)の場合は、高
        - 3日より後で7日以内の場合は、中
        - 7日より後、または期日なしの場合は、低
    - `期限`
        - 1日以内(期限切れを含む)の場合は、day
        - 2日以上7日以内の場合は、week
        - 7日より後、または期日なしの場合は、none

NotionのDBには以下のプロパティが必要です。

| プロパティ名 | 種類 | 値 |
| --- | --- | --- |
| `期日` | 日付 | |
| `期限` | セレクト | `day` / `week` / `none` / `Done` |
| `Priority` | セレクト | `高` / `中` / `低` |
| `完了日時` | 日付 | |

# requirements

* Python 3.12
* [notion-client](https://github.com/ramnes/notion-sdk-py) :for python notion api wrapper

# setup

1. fork this repository
2. get notion api token (integration token)
3. get notion db id
4. set GitHub Actions secrets

```
NOTION_TOKEN='notion token'
PRIVATE_DB='notion db id'
WORK_DB='notion db id'
SIDEWORK_DB='notion db id'
```

`PRIVATE_DB` / `WORK_DB` / `SIDEWORK_DB` は使うものだけ設定してください（未設定のDBはスキップされます）。

5. enable the `task watch` workflow in the Actions tab

GitHub Actionsのスケジュール実行は最短5分間隔です。また、リポジトリに60日間アクティビティがないとスケジュール実行は自動で無効化されるため、その場合はActionsタブから再度有効化してください。

# development

```
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

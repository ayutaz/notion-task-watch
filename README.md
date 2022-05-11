# Notion-Task-Watch

NotionのDBを定期的に関して、タスク管理を行うスクリプト

実装に関する記事書きました
→ [Notionのタスク 一覧でタスクがDoneになったときに完了日付を自動入力する【Notion,Python,GitHub Actions】](https://ayousanz.hatenadiary.jp/entry/Notion%E3%81%AE%E3%82%BF%E3%82%B9%E3%82%AF_%E4%B8%80%E8%A6%A7%E3%81%A7%E3%82%BF%E3%82%B9%E3%82%AF%E3%81%8CDone%E3%81%AB%E3%81%AA%E3%81%A3%E3%81%9F%E3%81%A8%E3%81%8D%E3%81%AB%E5%AE%8C%E4%BA%86%E6%97%A5%E4%BB%98)

# what is done?

* タスクの期限が `Done`になったら、完了日付を自動入力する
* 期日から `Priority`と `期限`を自動更新する
    - `Priority`
        - 1日以内の場合は、day
        - 2日以上7日以内の場合は、week
        - 7日以上の場合は、none
    - `期限`
        - 1日以内の場合は、day
        - 2日以上7日以内の場合は、week
        - 7日以上の場合は、none

# requirements

* Python 3.9
* [notion-client](https://github.com/ramnes/notion-sdk-py) :for python notion api wrapper

# setup

1. fork this repository
2. get notion api
3. get notion db url
4. set gitHub action secret for 1 and 2 values

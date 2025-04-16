# 開発ガイドライン

## ブランチ命名規則
ブランチ名は以下の形式で作成してください：
\`\`\`
<type>/<issue-number>-<short-description>
\`\`\`

例:
- \`feature/42-add-shot-chart\`
- \`bugfix/57-fix-data-loading\`
- \`refactor/63-optimize-rendering\`

## タイプの分類
- \`feature/\`: 新機能の追加
- \`bugfix/\`: バグの修正
- \`refactor/\`: リファクタリング（機能変更なし）
- \`docs/\`: ドキュメントの変更のみ
- \`test/\`: テストの追加・修正
- \`chore/\`: ビルドプロセスやツールの変更

## Issue駆動開発のワークフロー
1. 新しい作業を始める前に、必ずIssueを作成する
2. Issueに関連するブランチを作成する（上記の命名規則に従う）
3. 作業が完了したらプルリクエストを作成し、Issueへの参照を含める
4. レビュー後、ブランチをmainにマージする
5. マージ後、ブランチを削除する

## コミットメッセージのフォーマット
コミットメッセージは以下の形式に従ってください：
\`\`\`
<type>: <subject> #<issue-number>
\`\`\`

例:
- \`feat: implement shot chart visualization #42\`
- \`fix: correct data loading error #57\`
- \`docs: update README with setup instructions #30\`
"@ | Set-Content -Path "CONTRIBUTING.md"
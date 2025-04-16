param (
    [Parameter(Mandatory=$true)]
    [string]$IssueNumber,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet("feature", "bugfix", "refactor", "docs", "test", "chore")]
    [string]$Type,
    
    [Parameter(Mandatory=$true)]
    [string]$Description
)

# 現在のブランチがmainであることを確認
$currentBranch = git rev-parse --abbrev-ref HEAD
if ($currentBranch -ne "main") {
    Write-Error "現在のブランチがmainではありません。mainブランチに切り替えてください。"
    exit 1
}

# mainブランチを最新にする
git pull origin main

# 新しいブランチ名を作�E
$branchName = "$Type/$IssueNumber-$Description"
# スペ�Eスをハイフンに置換し、小文字に変換
$branchName = $branchName -replace " ", "-"
$branchName = $branchName.ToLower()

# ブランチを作�Eして刁E��替ぁE
git checkout -b $branchName

Write-Host "ブランチE'$branchName' を作�Eしました、E -ForegroundColor Green
Write-Host "コミット時に '#$IssueNumber' を含めることを忘れないでください、E -ForegroundColor Yellow

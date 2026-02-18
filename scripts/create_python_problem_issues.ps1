param(
    [string]$Repository = "ShamShamsw/student-interview-prep",
    [string]$ProblemsDir = "languages/python/problems",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

if (-not $DryRun -and -not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is required. Install from https://cli.github.com/ and run 'gh auth login'."
}

$problemFiles = Get-ChildItem -Path $ProblemsDir -Filter "*.md" |
    Where-Object { $_.Name -match "^(0[1-9]|[1-9][0-9])-.*\.md$" } |
    Sort-Object Name

if (-not $problemFiles) {
    throw "No problem files found matching NN-*.md in $ProblemsDir"
}

foreach ($file in $problemFiles) {
    $slug = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    $titleText = ($slug -replace "^\d{2}-", "") -replace "-", " "
    $issueTitle = "[Python Starter Problem] $titleText"

    $body = @"
## Goal
Add canonical Python solution and optional tests for [$($file.Name)]($ProblemsDir/$($file.Name)).

## Tasks
- Implement canonical solution in `languages/python/problems/solutions/$slug.py`
- Add time/space complexity notes in the markdown problem statement
- Add small runnable tests in `languages/python/tests/` (optional but preferred)

## Acceptance Criteria
- Solution handles all listed constraints
- Complexity is documented
- Tests pass in CI (if tests are added)

## Labels
`python`, `problem`, `good first issue`
"@

    if ($DryRun) {
        Write-Output "DRY RUN -> $issueTitle"
        continue
    }

    gh issue create `
        --repo $Repository `
        --title $issueTitle `
        --body $body `
        --label "good first issue" `
        --label "feature"
}

Write-Output "Processed $($problemFiles.Count) problem issue(s)."

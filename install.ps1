param(
  [switch]$Force
)

$ErrorActionPreference = "Stop"

$SkillName = "buddy-reroll"
$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BinDir = Join-Path $HOME "bin"

$targets = @(
  (Join-Path $HOME ".claude\skills\$SkillName")
)

if ($env:CODEX_HOME) {
  $targets += (Join-Path $env:CODEX_HOME "skills\$SkillName")
} else {
  $targets += (Join-Path $HOME ".codex\skills\$SkillName")
}

function Copy-Skill {
  param(
    [string]$TargetDir,
    [switch]$ForceCopy
  )

  $targetRoot = Split-Path -Parent $TargetDir
  if (!(Test-Path $targetRoot)) {
    New-Item -ItemType Directory -Path $targetRoot | Out-Null
  }

  if (Test-Path $TargetDir) {
    if ($ForceCopy) {
      Remove-Item -Recurse -Force $TargetDir
      New-Item -ItemType Directory -Path $TargetDir | Out-Null
    } else {
      Write-Host "Target already exists: $TargetDir"
      Write-Host "Update in place (use -Force for clean reinstall)."
    }
  } else {
    New-Item -ItemType Directory -Path $TargetDir | Out-Null
  }
  Copy-Item -Recurse -Force (Join-Path $SourceDir "*") $TargetDir

  if (Test-Path (Join-Path $TargetDir ".git")) {
    Remove-Item -Recurse -Force (Join-Path $TargetDir ".git")
  }
  if (Test-Path (Join-Path $TargetDir "node_modules")) {
    Remove-Item -Recurse -Force (Join-Path $TargetDir "node_modules")
  }

  return $true
}

Write-Host "Installing skill: $SkillName"
Write-Host "Source: $SourceDir"

$okCount = 0
foreach ($target in $targets) {
  Write-Host "Target: $target"
  if (Copy-Skill -TargetDir $target -ForceCopy:$Force) {
    $okCount++
  }
}

if ($okCount -eq 0) {
  Write-Error "No targets updated."
  exit 1
}

Write-Host "Install complete ($okCount target(s))."

if (!(Test-Path $BinDir)) {
  New-Item -ItemType Directory -Path $BinDir | Out-Null
}

$launcher = @"
@echo off
python "%USERPROFILE%\.claude\skills\buddy-reroll\scripts\reroll_buddy.py" %*
"@
Set-Content -Path (Join-Path $BinDir "buddy-reroll.cmd") -Value $launcher -Encoding ASCII

Write-Host "Try:"
Write-Host "  python `"$HOME\.claude\skills\$SkillName\scripts\reroll_buddy.py`" --random"
Write-Host "  buddy-reroll --random"
Write-Host "If buddy-reroll is not found, add $HOME\bin to PATH."

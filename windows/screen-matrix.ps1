<#
.SYNOPSIS
    Hesland ScreenMatrix Windows Companion CLI
.DESCRIPTION
    Send remote display and input mode-switch commands from Windows to Linux Mint.
.EXAMPLE
    .\screen-matrix.ps1 linux-only
    .\screen-matrix.ps1 linux-win
    .\screen-matrix.ps1 win-only
    .\screen-matrix.ps1 terminal-only
    .\screen-matrix.ps1 --pos right
    .\screen-matrix.ps1 --status
#>

param(
    [Parameter(Position=0)]
    [string]$Command = "",

    [string]$Pos = "",
    [string]$Audio = "",
    [switch]$Status,
    [switch]$Cycle,
    [switch]$Toggle,
    [string]$LinuxHost = "mbp-ts"
)

$argsList = @()

$validModes = @("linux-only", "linux-win", "win-only", "terminal-only", "1", "2", "3", "4")

if ($Status) {
    $argsList += "--status"
} elseif ($Cycle -or $Command -eq "cycle") {
    $argsList += "cycle"
} elseif ($Toggle -or $Command -eq "toggle") {
    $argsList += "toggle"
} elseif ($Command -in $validModes) {
    $argsList += $Command
}

if ($Pos) {
    $argsList += "--pos $Pos"
}

if ($Audio) {
    $argsList += "--audio $Audio"
}

$argStr = $argsList -join " "

if (-not $argStr) {
    Write-Host "Hesland ScreenMatrix Windows CLI" -ForegroundColor Cyan
    Write-Host "Usage: .\screen-matrix.ps1 [linux-only|linux-win|win-only|terminal-only] [-Pos right|left] [-Audio windows|both|mac] [-Status]"
    exit 0
}

Write-Host "📡 Sending command to Linux Mint ($LinuxHost): screen-matrix $argStr" -ForegroundColor Yellow
ssh -o ConnectTimeout=3 -o BatchMode=yes $LinuxHost "screen-matrix $argStr"

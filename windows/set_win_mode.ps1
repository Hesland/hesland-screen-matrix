<#
.SYNOPSIS
    ScreenMatrix Windows Host Mode Handler (Called by Linux Mint or local CLI)
.DESCRIPTION
    Toggles VDD Virtual Display and BarrierClient according to active mode.
#>

param(
    [int]$Mode = 2
)

$devcon = "C:\Users\Hesland\devcon.exe"

function Disable-VDD {
    if (Test-Path $devcon) {
        & $devcon disable "Root\MttVDD" 2>&1 | Out-Null
    } else {
        pnputil /disable-device "ROOT\DISPLAY\0001" 2>&1 | Out-Null
    }
}

function Enable-VDD {
    if (Test-Path $devcon) {
        & $devcon enable "Root\MttVDD" 2>&1 | Out-Null
        & $devcon restart "Root\MttVDD" 2>&1 | Out-Null
        & $devcon rescan 2>&1 | Out-Null
    } else {
        pnputil /enable-device "ROOT\DISPLAY\0001" 2>&1 | Out-Null
        pnputil /scan-devices 2>&1 | Out-Null
    }
}

if ($Mode -eq 1) {
    Disable-VDD
    taskkill /F /T /IM barrierc.exe 2>$null | Out-Null
    Write-Output "[WinMode] Mode 1: VDD disabled, BarrierClient killed (Ultrawide dedicated to Linux Mint)"
}
elseif ($Mode -eq 2) {
    Disable-VDD
    if (-not (Get-Process barrierc -ErrorAction SilentlyContinue)) {
        $vbs = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\BarrierClient.vbs"
        if (Test-Path $vbs) {
            Start-Process wscript.exe "`"$vbs`""
        }
    }
    Write-Output "[WinMode] Mode 2: VDD disabled, BarrierClient active (Ultrawide dedicated to Windows 240Hz)"
}
elseif ($Mode -eq 3) {
    taskkill /F /T /IM barrierc.exe 2>$null | Out-Null
    Enable-VDD
    Write-Output "[WinMode] Mode 3: VDD virtual 2nd display enabled for Moonlight streaming, Barrier killed"
}

# Ensure Primary Display holds 240Hz
try {
    & "C:\Users\Hesland\AppData\Local\Programs\WinModeSwitch.exe"
} catch {}

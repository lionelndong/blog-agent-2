#requires -Version 5.1
<#
.SYNOPSIS
  Stores a Doppler service token in the current user's Windows environment.

.DESCRIPTION
  Prompts for the token via a hidden input (Read-Host -AsSecureString), so the
  value never lands in the script file, your shell history, or your screen.
  Writes it to the User scope so all future shells inherit it. Existing shells
  will NOT see it until you reopen them.

.NOTES
  Run from a PowerShell window:
      powershell -ExecutionPolicy Bypass -File scripts\set-doppler-token.ps1
  Or, with execution policy already permissive:
      .\scripts\set-doppler-token.ps1
#>

Write-Host "Doppler service token setup" -ForegroundColor Cyan
Write-Host "----------------------------" -ForegroundColor Cyan
Write-Host "Generate one at: https://dashboard.doppler.com -> blog-agent project -> Access tab -> Generate"
Write-Host ""

$secure = Read-Host "Paste your Doppler service token (input is hidden)" -AsSecureString
$bstr   = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
$token  = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Host "ERROR: empty token, aborting." -ForegroundColor Red
    exit 1
}

if (-not $token.StartsWith("dp.st.")) {
    Write-Host "WARNING: token does not start with 'dp.st.' (Doppler service tokens normally do)." -ForegroundColor Yellow
    $confirm = Read-Host "Save it anyway? (y/N)"
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        Write-Host "Aborted." -ForegroundColor Yellow
        exit 1
    }
}

[System.Environment]::SetEnvironmentVariable("DOPPLER_TOKEN", $token, "User")

# Wipe in-memory copy
$token = $null
[System.GC]::Collect()

Write-Host ""
Write-Host "DOPPLER_TOKEN saved to User environment." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Close this terminal."
Write-Host "  2. Open a NEW terminal (User env is only inherited by new processes)."
Write-Host "  3. Verify with:    doppler me"
Write-Host "                    doppler secrets --only-names"
Write-Host "  4. Launch Claude:  cd C:\Users\ndong\Downloads\blog-agent-2"
Write-Host "                    doppler run -- claude"
Write-Host ""
Write-Host "To revoke later:    [Environment]::SetEnvironmentVariable('DOPPLER_TOKEN','','User')" -ForegroundColor DarkGray

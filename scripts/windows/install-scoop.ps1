#!/usr/bin/env pwsh

if (Get-Command -Name "Scoop" -ErrorAction SilentlyContinue) {
  Write-Host "Scoop is already installed"
}
else {
  # Set permission
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

  # Install Scoop
  Invoke-RestMethod get.scoop.sh | Invoke-Expression
}

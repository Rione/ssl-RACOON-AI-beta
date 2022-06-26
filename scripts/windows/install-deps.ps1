#!/usr/bin/env pwsh

function InstallWithScoop($packageName) {
  if (Get-Command -Name $packageName -ErrorAction SilentlyContinue) {
    Write-Host "$packageName is already installed"
  }
  else {
    scoop install $packageName
  }
}

InstallWithScoop "git"
InstallWithScoop "gh"
InstallWithScoop "make"

# PowerShell Engineering Patterns

## 1. Advanced Function with Splatting & Validation

```powershell
function Invoke-WorkplaceTask {
    <#
    .SYNOPSIS
        Executes a targeted workplace task.
    #>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$TargetName,

        [Parameter()]
        [ValidateSet("All", "WSL", "Windows")]
        [string[]]$Scope,

        [Parameter()]
        [string[]]$Tools,

        [switch]$Force
    )

    $params = @{
        TargetName = $TargetName
        Force      = $Force.IsPresent
    }
    if ($Tools) { $params['Tools'] = $Tools }
    if ($Scope) { $params['Scope'] = $Scope }

    & $targetScript @params
}
```

## 2. Settings.psd1 Safe Loader

```powershell
function Get-ModuleSettings {
    [CmdletBinding()]
    param ([string]$SettingsPath)

    if (-not $SettingsPath) {
        $candidate = Join-Path $PSScriptRoot "..\..\Config\Settings.psd1"
        if (Test-Path $candidate) {
            $SettingsPath = (Resolve-Path $candidate).Path
        }
    }

    if ($SettingsPath -and (Test-Path $SettingsPath)) {
        if (Get-Command Import-PowerShellDataFile -ErrorAction SilentlyContinue) {
            return Import-PowerShellDataFile -Path $SettingsPath
        }
        return (Invoke-Expression (Get-Content -Path $SettingsPath -Raw))
    }

    return @{}
}
```

## 3. WSL Command Execution & Output Sanitization

```powershell
# Query WSL distributions cleanly without UTF-16LE null bytes
$output = wsl.exe -l -q 2>$null
$distros = ($output -replace "\x00", "") -split '\r?\n' |
           ForEach-Object { $_.Trim() } |
           Where-Object { -not [string]::IsNullOrWhiteSpace($_) -and $_ -notmatch '^docker-desktop' }
```

## 4. Non-Mutating Pester 5 Test Fixture

```powershell
BeforeAll {
    $script:modulePath = Join-Path $PSScriptRoot "..\scripts\Modules\MyModule\MyModule.psd1"
    Import-Module $script:modulePath -Force

    # Isolated non-mutating temporary folder
    $script:tempDir = Join-Path $env:TEMP "TestFixture_$([System.Guid]::NewGuid().ToString('N'))"
    New-Item -Path $script:tempDir -ItemType Directory -Force | Out-Null
}

AfterAll {
    if (Test-Path $script:tempDir) {
        Remove-Item -Path $script:tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Describe "Component Validation" {
    Context "Isolated Execution" {
        It "Processes files without mutating host state" {
            $testFile = Join-Path $script:tempDir "test.txt"
            Set-Content -Path $testFile -Value "sample"
            Test-Path $testFile | Should -BeTrue
        }
    }
}
```

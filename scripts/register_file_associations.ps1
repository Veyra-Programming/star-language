# =====================================================================
# Star Programming Language - Windows File Association & Explorer Integrator
# Registers .star, .starb, .starmobile with custom icons & shell context menus
# =====================================================================

param(
    [string]$StarHome = "E:\Star Language",
    [switch]$Unregister
)

$StarHome = (Resolve-Path $StarHome).Path
$StarBat = Join-Path $StarHome "star.bat"
$IconsDir = Join-Path $StarHome "assets\icons"

$SourceIco = Join-Path $IconsDir "star_source.ico"
$BytecodeIco = Join-Path $IconsDir "star_bytecode.ico"
$MobileIco = Join-Path $IconsDir "star_mobile.ico"
$StarIco = Join-Path $IconsDir "star.ico"

# Windows CTypes / PInvoke for SHChangeNotify
$cSource = @'
using System;
using System.Runtime.InteropServices;

public class ShellNotifier {
    [DllImport("shell32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern void SHChangeNotify(uint wEventId, uint uFlags, IntPtr dwItem1, IntPtr dwItem2);

    public const uint SHCNE_ASSOCCHANGED = 0x08000000;
    public const uint SHCNF_IDLIST = 0x0000;

    public static void NotifyAssocChanged() {
        SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, IntPtr.Zero, IntPtr.Zero);
    }
}
'@

if (-not ([System.Management.Automation.PSTypeName]'ShellNotifier').Type) {
    Add-Type -TypeDefinition $cSource
}

function Remove-RegistryKeySafe([string]$path) {
    if (Test-Path $path) {
        Remove-Item -Path $path -Recurse -Force | Out-Null
        Write-Host "Removed: $path"
    }
}

if ($Unregister) {
    Write-Host "Unregistering Star Language file associations..."
    Remove-RegistryKeySafe "HKCU:\Software\Classes\.star"
    Remove-RegistryKeySafe "HKCU:\Software\Classes\Star.SourceFile"
    Remove-RegistryKeySafe "HKCU:\Software\Classes\.starb"
    Remove-RegistryKeySafe "HKCU:\Software\Classes\Star.BytecodeFile"
    Remove-RegistryKeySafe "HKCU:\Software\Classes\.starmobile"
    Remove-RegistryKeySafe "HKCU:\Software\Classes\Star.MobileBundle"
    Remove-RegistryKeySafe "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.star\UserChoice"
    Remove-RegistryKeySafe "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.starb\UserChoice"
    Remove-RegistryKeySafe "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.starmobile\UserChoice"

    [ShellNotifier]::NotifyAssocChanged()
    Write-Host "Unregistered successfully. Shell notified."
    exit 0
}

Write-Host "Registering Star Language file associations in Windows Explorer..."
Write-Host "Star Home:  $StarHome"
Write-Host "Icons Dir:  $IconsDir"

# -------------------------------------------------------------
# 1. Register .star (Star Source File)
# -------------------------------------------------------------
$extKey = "HKCU:\Software\Classes\.star"
New-Item -Path $extKey -Force | Out-Null
Set-ItemProperty -Path $extKey -Name "(Default)" -Value "Star.SourceFile"
Set-ItemProperty -Path $extKey -Name "Content Type" -Value "text/x-star"
Set-ItemProperty -Path $extKey -Name "PerceivedType" -Value "text"

$openWithKey = "$extKey\OpenWithProgids"
New-Item -Path $openWithKey -Force | Out-Null
Set-ItemProperty -Path $openWithKey -Name "Star.SourceFile" -Value ""

$progKey = "HKCU:\Software\Classes\Star.SourceFile"
New-Item -Path $progKey -Force | Out-Null
Set-ItemProperty -Path $progKey -Name "(Default)" -Value "Star Source File"
Set-ItemProperty -Path $progKey -Name "FriendlyTypeName" -Value "Star Source File"

# DefaultIcon
$iconKey = "$progKey\DefaultIcon"
New-Item -Path $iconKey -Force | Out-Null
Set-ItemProperty -Path $iconKey -Name "(Default)" -Value "$SourceIco,0"

# Shell Context Menu
$shellKey = "$progKey\shell"
New-Item -Path $shellKey -Force | Out-Null
Set-ItemProperty -Path $shellKey -Name "(Default)" -Value "open"

# Action 1: Open / Run with Star
$runKey = "$shellKey\open"
New-Item -Path $runKey -Force | Out-Null
Set-ItemProperty -Path $runKey -Name "(Default)" -Value "Run with Star"
Set-ItemProperty -Path $runKey -Name "Icon" -Value "$SourceIco"
$runCmdKey = "$runKey\command"
New-Item -Path $runCmdKey -Force | Out-Null
Set-ItemProperty -Path $runCmdKey -Name "(Default)" -Value "`"$StarBat`" run `"%1`" %*"

# Action 2: Run in Interactive Console (Pause on finish)
$replKey = "$shellKey\interactive"
New-Item -Path $replKey -Force | Out-Null
Set-ItemProperty -Path $replKey -Name "(Default)" -Value "Run in Star Interactive Terminal"
Set-ItemProperty -Path $replKey -Name "Icon" -Value "$StarIco"
$replCmdKey = "$replKey\command"
New-Item -Path $replCmdKey -Force | Out-Null
Set-ItemProperty -Path $replCmdKey -Name "(Default)" -Value "cmd.exe /k `"`"$StarBat`" run `"%1`"`""

# Action 3: Compile to Bytecode (.starb)
$compKey = "$shellKey\compile"
New-Item -Path $compKey -Force | Out-Null
Set-ItemProperty -Path $compKey -Name "(Default)" -Value "Compile with Star (Bytecode)"
Set-ItemProperty -Path $compKey -Name "Icon" -Value "$BytecodeIco"
$compCmdKey = "$compKey\command"
New-Item -Path $compCmdKey -Force | Out-Null
Set-ItemProperty -Path $compCmdKey -Name "(Default)" -Value "cmd.exe /k `"`"$StarBat`" compile `"%1`"`""

# Action 4: Check Syntax & Lint
$checkKey = "$shellKey\check"
New-Item -Path $checkKey -Force | Out-Null
Set-ItemProperty -Path $checkKey -Name "(Default)" -Value "Check Syntax with Star Doctor"
Set-ItemProperty -Path $checkKey -Name "Icon" -Value "$StarIco"
$checkCmdKey = "$checkKey\command"
New-Item -Path $checkCmdKey -Force | Out-Null
Set-ItemProperty -Path $checkCmdKey -Name "(Default)" -Value "cmd.exe /k `"`"$StarBat`" check `"%1`"`""

# Action 5: Edit with Notepad
$editKey = "$shellKey\edit"
New-Item -Path $editKey -Force | Out-Null
Set-ItemProperty -Path $editKey -Name "(Default)" -Value "Edit with Notepad"
$editCmdKey = "$editKey\command"
New-Item -Path $editCmdKey -Force | Out-Null
Set-ItemProperty -Path $editCmdKey -Name "(Default)" -Value "notepad.exe `"%1`""

# -------------------------------------------------------------
# 2. Register .starb (Star Bytecode File)
# -------------------------------------------------------------
$extBKey = "HKCU:\Software\Classes\.starb"
New-Item -Path $extBKey -Force | Out-Null
Set-ItemProperty -Path $extBKey -Name "(Default)" -Value "Star.BytecodeFile"
Set-ItemProperty -Path $extBKey -Name "PerceivedType" -Value "application"

$progBKey = "HKCU:\Software\Classes\Star.BytecodeFile"
New-Item -Path $progBKey -Force | Out-Null
Set-ItemProperty -Path $progBKey -Name "(Default)" -Value "Star Compiled Bytecode"
Set-ItemProperty -Path $progBKey -Name "FriendlyTypeName" -Value "Star Compiled Bytecode"

$iconBKey = "$progBKey\DefaultIcon"
New-Item -Path $iconBKey -Force | Out-Null
Set-ItemProperty -Path $iconBKey -Name "(Default)" -Value "$BytecodeIco,0"

$shellBKey = "$progBKey\shell"
New-Item -Path $shellBKey -Force | Out-Null
Set-ItemProperty -Path $shellBKey -Name "(Default)" -Value "open"

$openBKey = "$shellBKey\open"
New-Item -Path $openBKey -Force | Out-Null
Set-ItemProperty -Path $openBKey -Name "(Default)" -Value "Execute with Star VM"
Set-ItemProperty -Path $openBKey -Name "Icon" -Value "$BytecodeIco"
$openBCmdKey = "$openBKey\command"
New-Item -Path $openBCmdKey -Force | Out-Null
Set-ItemProperty -Path $openBCmdKey -Name "(Default)" -Value "`"$StarBat`" run `"%1`" %*"

$irBKey = "$shellBKey\disasm"
New-Item -Path $irBKey -Force | Out-Null
Set-ItemProperty -Path $irBKey -Name "(Default)" -Value "Disassemble Bytecode (Star IR)"
Set-ItemProperty -Path $irBKey -Name "Icon" -Value "$StarIco"
$irBCmdKey = "$irBKey\command"
New-Item -Path $irBCmdKey -Force | Out-Null
Set-ItemProperty -Path $irBCmdKey -Name "(Default)" -Value "cmd.exe /k `"`"$StarBat`" ir `"%1`"`""

# -------------------------------------------------------------
# 3. Register .starmobile (Star Mobile App Bundle)
# -------------------------------------------------------------
$extMKey = "HKCU:\Software\Classes\.starmobile"
New-Item -Path $extMKey -Force | Out-Null
Set-ItemProperty -Path $extMKey -Name "(Default)" -Value "Star.MobileBundle"
Set-ItemProperty -Path $extMKey -Name "PerceivedType" -Value "application"

$progMKey = "HKCU:\Software\Classes\Star.MobileBundle"
New-Item -Path $progMKey -Force | Out-Null
Set-ItemProperty -Path $progMKey -Name "(Default)" -Value "Star Mobile Application Bundle"
Set-ItemProperty -Path $progMKey -Name "FriendlyTypeName" -Value "Star Mobile Application Bundle"

$iconMKey = "$progMKey\DefaultIcon"
New-Item -Path $iconMKey -Force | Out-Null
Set-ItemProperty -Path $iconMKey -Name "(Default)" -Value "$MobileIco,0"

$shellMKey = "$progMKey\shell"
New-Item -Path $shellMKey -Force | Out-Null
Set-ItemProperty -Path $shellMKey -Name "(Default)" -Value "open"

$openMKey = "$shellMKey\open"
New-Item -Path $openMKey -Force | Out-Null
Set-ItemProperty -Path $openMKey -Name "(Default)" -Value "Simulate Mobile App"
Set-ItemProperty -Path $openMKey -Name "Icon" -Value "$MobileIco"
$openMCmdKey = "$openMKey\command"
New-Item -Path $openMCmdKey -Force | Out-Null
Set-ItemProperty -Path $openMCmdKey -Name "(Default)" -Value "`"$StarBat`" simulate mobile `"%1`""

$deployMKey = "$shellMKey\deploy_android"
New-Item -Path $deployMKey -Force | Out-Null
Set-ItemProperty -Path $deployMKey -Name "(Default)" -Value "Deploy to Android Device"
Set-ItemProperty -Path $deployMKey -Name "Icon" -Value "$MobileIco"
$deployMCmdKey = "$deployMKey\command"
New-Item -Path $deployMCmdKey -Force | Out-Null
Set-ItemProperty -Path $deployMCmdKey -Name "(Default)" -Value "cmd.exe /k `"`"$StarBat`" deploy android `"%1`"`""

# Clean user choice overrides if any
try {
    Remove-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.star\UserChoice" -Force -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.starb\UserChoice" -Force -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.starmobile\UserChoice" -Force -Recurse -ErrorAction SilentlyContinue
} catch {}

# Notify Windows Shell & Explorer
[ShellNotifier]::NotifyAssocChanged()
Start-Process -FilePath "ie4uinit.exe" -ArgumentList "-show" -Wait -WindowStyle Hidden -ErrorAction SilentlyContinue

Write-Host "`n✓ File associations registered successfully in Windows Registry!"
Write-Host "✓ Windows File Explorer notified (SHCNE_ASSOCCHANGED broadcasted)."
Write-Host "✓ .star files now display the Star icon and context menu options."


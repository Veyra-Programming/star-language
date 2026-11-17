; =====================================================================
; ⭐ STAR PROGRAMMING LANGUAGE — OFFICIAL WINDOWS INSTALLER SCRIPT (Inno Setup)
; Version: 1.2.0 GA
; Authoritative Reference: STAR_DISTRIBUTION.md & STAR_PORTAL_ADMIN.md
; =====================================================================

#define MyAppName "Star Programming Language"
#define MyAppShortName "Star"
#define MyAppVersion "1.2.0"
#define MyAppPublisher "Star Language Open Source Project"
#define MyAppURL "https://www.shreeshop.in/star"
#define MyAppExeName "star.exe"

[Setup]
; Unique application GUID
AppId={{8B4365D8-2C72-4C69-B086-4552084D98C1}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\Star
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=STAR_LICENSE_AGREEMENT.md
OutputDir=dist
OutputBaseFilename=Star-1.2.0-Windows-x64-Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardResizable=no
ArchitecturesAllowed=x86 x64 x64compatible arm64
ArchitecturesInstallIn64BitMode=x64compatible arm64
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ChangesEnvironment=yes
ChangesAssociations=yes
UninstallDisplayName={#MyAppName} {#MyAppVersion}
UninstallDisplayIcon={app}\bin\star.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "envPath"; Description: "Add Star binary directory ({app}\bin) to PATH environment variable"; GroupDescription: "System Environment:"; Flags: checkedonce
Name: "fileassoc"; Description: "Register Star file extensions (.star, .starb, .starmobile) and show Star icons in File Explorer"; GroupDescription: "File Associations:"; Flags: checkedonce
Name: "vscodeext"; Description: "Install official Star Language extension for Visual Studio Code"; GroupDescription: "IDE Integration:"; Flags: checkedonce
Name: "desktopicon"; Description: "Create Star Developer Portal desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
; -------------------------------------------------------------
; 1. ZERO-SOURCE PRODUCTION DISTRIBUTION (Native PE binaries, .starb bytecode, no .py/.pyc)
; -------------------------------------------------------------
Source: "dist\Star-1.2.0-Windows-x64\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "star.bat"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "starc.bat"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "star-runtime.bat"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "star"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "starc"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "star-runtime"; DestDir: "{app}\bin"; Flags: ignoreversion

; -------------------------------------------------------------
; 2. DOCUMENTATION, SPECIFICATIONS & LEGAL AGREEMENTS
; -------------------------------------------------------------
Source: "STAR_LICENSE_AGREEMENT.md"; DestDir: "{app}\licenses"; DestName: "EULA.txt"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}\licenses"; DestName: "LICENSE.txt"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "STAR_SPEC.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "STAR_ABI.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "VERSION"; DestDir: "{app}"; Flags: ignoreversion

; -------------------------------------------------------------
; 3. DEVELOPER PORTAL & WEB PLAYGROUND
; -------------------------------------------------------------
Source: "web\portal\*"; DestDir: "{app}\portal"; Flags: ignoreversion recursesubdirs createallsubdirs

; -------------------------------------------------------------
; 4. ICONS & BRANDING ASSETS
; -------------------------------------------------------------
Source: "assets\icons\*"; DestDir: "{app}\assets\icons"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\*.ico"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; -------------------------------------------------------------
; 5. IDE EXTENSIONS (VISUAL STUDIO CODE)
; -------------------------------------------------------------
Source: "vscode-star\*.vsix"; DestDir: "{app}\extensions"; Flags: ignoreversion

[Registry]
; .star Source File Association
Root: HKCR; Subkey: ".star"; ValueType: string; ValueName: ""; ValueData: "Star.SourceFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCR; Subkey: ".star"; ValueType: string; ValueName: "Content Type"; ValueData: "text/x-star"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCR; Subkey: ".star"; ValueType: string; ValueName: "PerceivedType"; ValueData: "text"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCR; Subkey: ".star\OpenWithProgids"; ValueType: string; ValueName: "Star.SourceFile"; ValueData: ""; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCR; Subkey: "Star.SourceFile"; ValueType: string; ValueName: ""; ValueData: "Star Source File"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.SourceFile"; ValueType: string; ValueName: "FriendlyTypeName"; ValueData: "Star Source File"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.SourceFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\assets\icons\star_source.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.SourceFile\shell"; ValueType: string; ValueName: ""; ValueData: "open"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.SourceFile\shell\open"; ValueType: string; ValueName: ""; ValueData: "Run with Star"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.SourceFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\bin\star.bat"" run ""%1"" %*"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.SourceFile\shell\compile"; ValueType: string; ValueName: ""; ValueData: "Compile with Star (Bytecode)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.SourceFile\shell\compile\command"; ValueType: string; ValueName: ""; ValueData: "cmd.exe /k """"{app}\bin\star.bat"" compile ""%1"""""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.SourceFile\shell\check"; ValueType: string; ValueName: ""; ValueData: "Check Syntax with Star Doctor"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.SourceFile\shell\check\command"; ValueType: string; ValueName: ""; ValueData: "cmd.exe /k """"{app}\bin\star.bat"" check ""%1"""""; Flags: uninsdeletekey; Tasks: fileassoc

; .starb Bytecode File Association
Root: HKCR; Subkey: ".starb"; ValueType: string; ValueName: ""; ValueData: "Star.BytecodeFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCR; Subkey: ".starb"; ValueType: string; ValueName: "PerceivedType"; ValueData: "application"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCR; Subkey: ".starb\OpenWithProgids"; ValueType: string; ValueName: "Star.BytecodeFile"; ValueData: ""; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCR; Subkey: "Star.BytecodeFile"; ValueType: string; ValueName: ""; ValueData: "Star Compiled Bytecode"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.BytecodeFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\assets\icons\star_bytecode.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.BytecodeFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\bin\star.bat"" run ""%1"" %*"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.BytecodeFile\shell\disasm\command"; ValueType: string; ValueName: ""; ValueData: "cmd.exe /k """"{app}\bin\star.bat"" ir ""%1"""""; Flags: uninsdeletekey; Tasks: fileassoc

; .starmobile Mobile App Bundle Association
Root: HKCR; Subkey: ".starmobile"; ValueType: string; ValueName: ""; ValueData: "Star.MobileBundle"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCR; Subkey: ".starmobile"; ValueType: string; ValueName: "PerceivedType"; ValueData: "application"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCR; Subkey: "Star.MobileBundle"; ValueType: string; ValueName: ""; ValueData: "Star Mobile Application Bundle"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.MobileBundle\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\assets\icons\star_mobile.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCR; Subkey: "Star.MobileBundle\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\bin\star.bat"" simulate mobile ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

[Icons]
Name: "{group}\Star Doctor Diagnostics"; Filename: "{app}\bin\star.exe"; Parameters: "doctor"; IconFilename: "{app}\bin\star.exe"
Name: "{group}\Star Interactive REPL"; Filename: "{app}\bin\star.exe"; Parameters: "repl"; IconFilename: "{app}\bin\star.exe"
Name: "{group}\The Star Book (Documentation)"; Filename: "{app}\portal\index.html"
Name: "{group}\Star License & EULA"; Filename: "{app}\licenses\EULA.txt"
Name: "{group}\Uninstall Star"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Star Developer Portal"; Filename: "{app}\portal\index.html"; Tasks: desktopicon

[Run]
Filename: "cmd.exe"; Parameters: "/c code --install-extension ""{app}\extensions\star-programming-language-1.2.0.vsix"""; Description: "Install Star Language extension in Visual Studio Code"; Tasks: vscodeext; Flags: runhidden skipifsilent
Filename: "{app}\bin\star.exe"; Parameters: "doctor"; Description: "Run Star Doctor environment check"; Flags: postinstall nowait skipifsilent unchecked
Filename: "{app}\portal\index.html"; Description: "Open Star Developer Portal in default browser"; Flags: postinstall shellexec skipifsilent unchecked

[Code]
// =====================================================================
// PASCAL SCRIPT: ROBUST PATH ENVIRONMENT MANAGEMENT
// =====================================================================

function GetEnvRootKey(): Integer;
begin
    if IsAdminInstallMode then
        Result := HKEY_LOCAL_MACHINE
    else
        Result := HKEY_CURRENT_USER;
end;

function GetEnvSubKey(): string;
begin
    if IsAdminInstallMode then
        Result := 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    else
        Result := 'Environment';
end;

function NeedsAddPath(Param: string): boolean;
var
    OrigPath: string;
begin
    if not RegQueryStringValue(GetEnvRootKey(), GetEnvSubKey(), 'Path', OrigPath) then
    begin
        Result := True;
        exit;
    end;
    // Check if the directory is already present in PATH
    Result := Pos(';' + Uppercase(Param) + ';', ';' + Uppercase(OrigPath) + ';') = 0;
end;

procedure AddPathToEnv(Param: string);
var
    OrigPath: string;
begin
    if NeedsAddPath(Param) then
    begin
        if RegQueryStringValue(GetEnvRootKey(), GetEnvSubKey(), 'Path', OrigPath) then
        begin
            if (Length(OrigPath) > 0) and (OrigPath[Length(OrigPath)] <> ';') then
                OrigPath := OrigPath + ';';
            OrigPath := OrigPath + Param;
        end
        else
        begin
            OrigPath := Param;
        end;
        RegWriteStringValue(GetEnvRootKey(), GetEnvSubKey(), 'Path', OrigPath);
    end;
end;

procedure RemovePathFromEnv(Param: string);
var
    OrigPath: string;
    P: Integer;
begin
    if RegQueryStringValue(GetEnvRootKey(), GetEnvSubKey(), 'Path', OrigPath) then
    begin
        P := Pos(';' + Uppercase(Param) + ';', ';' + Uppercase(OrigPath) + ';');
        if P > 0 then
        begin
            OrigPath := ';' + OrigPath + ';';
            StringChangeEx(OrigPath, ';' + Param + ';', ';', True);
            StringChangeEx(OrigPath, ';' + Uppercase(Param) + ';', ';', True);
            if (Length(OrigPath) > 1) and (OrigPath[1] = ';') then
                Delete(OrigPath, 1, 1);
            if (Length(OrigPath) > 0) and (OrigPath[Length(OrigPath)] = ';') then
                Delete(OrigPath, Length(OrigPath), 1);
            RegWriteStringValue(GetEnvRootKey(), GetEnvSubKey(), 'Path', OrigPath);
        end;
    end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
    BinDir: string;
begin
    if CurStep = ssPostInstall then
    begin
        if WizardIsTaskSelected('envPath') then
        begin
            BinDir := ExpandConstant('{app}\bin');
            AddPathToEnv(BinDir);
        end;
    end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
    BinDir: string;
begin
    if CurUninstallStep = usPostUninstall then
    begin
        BinDir := ExpandConstant('{app}\bin');
        RemovePathFromEnv(BinDir);
    end;
end;

#define PANDOCEXE "pandoc-1.15.2-windows.msi"
[setup]
AppName=7L
AppVerName=V0.1.0
DefaultDirName="C:\7L"
AppVersion=0.1.0

[components]
Name: main; Description:"主程序(必选)";Types:full compact custom;Flags: fixed
Name: pandoc; Description:"pandoc，用于预览和转换，若未安装请勾选";Types:full;

[files]
Source: "dist\7L\*";DestDir: "{app}";Flags: recursesubdirs createallsubdirs;Components:main
Source: "{#PANDOCEXE}";DestDir: "{app}";Components:pandoc

[run]
Filename: "{app}\{#PANDOCEXE}";Flags: shellexec waituntilterminated skipifdoesntexist;StatusMsg:"正在安装 pandoc";Parameters:"/qb"

[uninstallrun]
Filename: "msiexec";Flags:waituntilterminated skipifdoesntexist;Parameters:"/x {app}\{#PANDOCEXE}"

; [icons]
; Name: "{userdesktop}\7L";Filename: "{app}\7L.exe"; WorkingDir: "{app}";Comment:"Markdown 编辑器"

[Setup]
DisableProgramGroupPage=yes
ChangesAssociations=yes

[languages]
Name: "cs"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Registry]
Root: HKCR; Subkey: ".md"; Flags: uninsdeletekey
Root: HKCR; Subkey: ".md"; ValueType: string; ValueName: ""; ValueData: "markdownfile"
Root: HKCR; Subkey: "markdownfile"; Flags: uninsdeletekey
Root: HKCR; Subkey: "markdownfile"; ValueType: string; ValueName: ""; ValueData: "Markdown File"
Root: HKCR; Subkey: "markdownfile\DefaultIcon"; Flags: uninsdeletekey
Root: HKCR; Subkey: "markdownfile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\data\icon\mimetype.ico"
Root: HKCR; Subkey: "markdownfile\Shell"; Flags: uninsdeletekey
Root: HKCR; Subkey: "markdownfile\Shell"; ValueType: string; ValueName: ""; ValueData: "Open"
Root: HKCR; Subkey: "markdownfile\Shell\Open\Command"; Flags: uninsdeletekey
Root: HKCR; Subkey: "markdownfile\Shell\Open\Command"; ValueType: string; ValueName: ""; ValueData: "{app}\7L.exe %1"

[Code]
// http://bbs.hanzify.org/read-htm-tid-66978.html
// 调用 Shell32.dll 中的 SHChangeNotify 函数来刷新文件关联
procedure SHChangeNotify(wEventId, uFlags, dwItem1, dwItem2: integer);
external 'SHChangeNotify@Shell32.dll stdcall';
// 定义一个函数来直接调用
procedure ApplyFileAsoc();
begin
  SHChangeNotify(08000000, 0, 0, 0);
end;
// 安装完成后调用
procedure CurStepChanged (CurStep: TSetupStep );
begin
  case CurStep of
    ssPostInstall:
      ApplyFileAsoc();
  end;
end;

// 卸载完成后调用
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  case CurUninstallStep of
    usPostUninstall:
      ApplyFileAsoc();
  end;
end;

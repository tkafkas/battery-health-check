Set UAC = CreateObject("Shell.Application")
Set Shell = CreateObject("WScript.Shell")
scriptdir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
UAC.ShellExecute "cmd.exe", "/c """ & scriptdir & "\check_battery.bat""", "", "runas", 1
;Include modern UI
!include "MUI2.nsh"

;---General settings---

Name "DySMo"
OutFile "DySMo Install.exe"
InstallDir "C:\DySMo"
;InstallDir "C:\Users\Amir\Desktop\123"
InstallDirRegKey HKCU "Software\DySMo" ""
;Request application privileges for Windows Vista
RequestExecutionLevel user
;cause a warning when trying to abort installation
!define MUI_ABORTWARNING

;---Pages---
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "DySMo\LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

;--Languages---
!insertmacro MUI_LANGUAGE "English"

;------------------------
;---Installer Sections---
;------------------------

;DySMo Section
Section "DySMo" secDySMo
	;make section required
	SectionIn RO

	SetOutPath "$INSTDIR"
	
	File /r "DySMo\"

	;Set installation dir in registry
	WriteRegStr HKCU "Software\DySMo" "" $INSTDIR

	;Create a template config file
	FileOpen $9 "$INSTDIR\config.cfg" w
	FileWrite $9 "[Dymola]"
	FileWrite $9 "$\r$\n"
	FileWrite $9 "AlistDir = "
	FileWrite $9 "$\r$\n"
	FileWrite $9 "PathExe = "
	FileWrite $9 "$\r$\n"
	FileWrite $9 "$\r$\n"
	FileWrite $9 "[OpenModelica]"
	FileWrite $9 "$\r$\n"
	FileWrite $9 "PathExe = "
	FileWrite $9 "$\r$\n"
	FileClose $9

	MessageBox MB_OK "An empty config file has been created. Please check the readme on howto config DySMo"


	;Create uninstaller
	WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd


;Samples section
Section "Samples" secSamples
	SetOutPath "$INSTDIR"
	
	File /r "samples"
SectionEnd



;Uninstaller section
Section "Uninstall"
	;delete files
	RMDir /r "$INSTDIR\documentation"
	RMDir /r "$INSTDIR\src"
	RMDir /r "$INSTDIR\samples"
	Delete "$INSTDIR\config.cfg"
	Delete "$INSTDIR\LICENSE.txt"
	Delete "$INSTDIR\README.txt"
	Delete "$INSTDIR\run.bat"
	Delete "$INSTDIR\software.txt"

	Delete "$INSTDIR\Uninstall.exe"
	RMDir "$INSTDIR"
	DeleteRegKey /ifempty HKCU "Software\DySMo"
SectionEnd


;--------------------
;Section Descriptions
;--------------------
	LangString DESC_secDySMo ${LANG_ENGLISH} "Core application. (required)"
	LangString DESC_secSamples ${LANG_ENGLISH} "Sample variable-structure modes. (recommended)"

	!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
		!insertmacro MUI_DESCRIPTION_TEXT ${secDySMo} $(DESC_secDySMo)
		!insertmacro MUI_DESCRIPTION_TEXT ${secSamples} $(DESC_secSamples)
	!insertmacro MUI_FUNCTION_DESCRIPTION_END
@echo off
rem %~dp0 is expanded pathname of the current script under NT
SET BASE_DIR=%~dp0/..
SET CP="%BASE_DIR%;%BASE_DIR%/lib/log4j-api-2.14.0.jar;%BASE_DIR%/lib/log4j-core-2.14.0.jar;%BASE_DIR%/lib/log4j-1.2-api-2.14.0.jar;%BASE_DIR%/lib/oxygen.jar;%BASE_DIR%/lib/oxygenDeveloper.jar;%BASE_DIR%/classes;%BASE_DIR%/lib/*"
SET OXYGEN_JAVA=java.exe
if exist "%JAVA_HOME%\bin\java.exe" set OXYGEN_JAVA="%JAVA_HOME%\bin\java.exe"
if exist "%BASE_DIR%\jre\bin\java.exe" SET OXYGEN_JAVA="%BASE_DIR%\jre\bin\java.exe"
%OXYGEN_JAVA% -Xmx180m -XX:SoftRefLRUPolicyMSPerMB=10 -Dcom.oxygenxml.ApplicationDataFolder="%APPDATA%" -cp %CP% ro.sync.xml.generator.XMLInstanceGenerator %*
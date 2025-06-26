@echo off &PUSHD %~DP0 &TITLE Settings Tool

:menu
cls
echo Notes: Please connect device with adb, it's only adapter for Android 11.
echo === Menu ===
echo [1] view top activity
echo [2] view top fragment
echo [3] view activity stack
echo ============
set /p user_input=Please choose menu:
if %user_input%==1 goto topActivity
if %user_input%==2 goto topFragment
if %user_input%==3 goto activityStack
if not %user_input%=="" goto menu

:topActivity
adb wait-for-device
adb shell "dumpsys activity top | grep ACTIVITY | tail -n 1"
echo. & pause
goto menu

:topFragment
adb wait-for-device
adb shell "dumpsys activity top | grep '#[0-9]: ' | tail -n 1"
echo. & pause
goto menu

:activityStack
adb wait-for-device
adb shell "dumpsys activity activities | grep '* ActivityRecord{'"
echo. & pause
goto menu
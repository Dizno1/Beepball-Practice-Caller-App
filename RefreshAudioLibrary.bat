@echo off
title Refresh Audio Library

echo.
echo ==========================================
echo Refreshing Beepball Practice Caller
echo ==========================================
echo.

py refreshAudioLibrary.py

if errorlevel 1 (
    echo.
    echo Refresh FAILED.
) else (
    echo.
    echo Refresh completed successfully.
)

echo.
echo Press any key to close...
pause >nul
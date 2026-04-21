@echo off
REM Cleanup script for Demo 2 - Object Recognition
REM Removes all training data and trained models

echo ========================================
echo Demo 2 - Cleanup Script
echo ========================================
echo.
echo This will DELETE:
echo   - All training images in data/positive/
echo   - All training images in data/negative/
echo   - All trained models in models/
echo.

set /p CONFIRM="Are you sure you want to continue? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo Cleanup cancelled.
    exit /b 0
)

echo.
echo Starting cleanup...
echo.

REM Remove positive training images
if exist "data\positive" (
    echo Removing positive training images...
    del /q "data\positive\*.jpg" 2>nul
    del /q "data\positive\*.png" 2>nul
    del /q "data\positive\*.jpeg" 2>nul
    echo   - Positive images removed
) else (
    echo   - data\positive folder does not exist
)

REM Remove negative training images
if exist "data\negative" (
    echo Removing negative training images...
    del /q "data\negative\*.jpg" 2>nul
    del /q "data\negative\*.png" 2>nul
    del /q "data\negative\*.jpeg" 2>nul
    echo   - Negative images removed
) else (
    echo   - data\negative folder does not exist
)

REM Remove trained models
if exist "models" (
    echo Removing trained models...
    del /q "models\*.pkl" 2>nul
    del /q "models\*.h5" 2>nul
    del /q "models\*.pt" 2>nul
    echo   - Trained models removed
) else (
    echo   - models folder does not exist
)

echo.
echo ========================================
echo Cleanup complete!
echo ========================================
echo.
echo The following folders are now empty:
echo   - data/positive/
echo   - data/negative/
echo   - models/
echo.
echo You can now collect new training data using:
echo   python collect_training_data.py
echo.

pause


## 🔧 **Теперь создай установочные скрипты:**

### 1. **Создай файл `install.ps1`** (для Windows):

```powershell
# install.ps1 - Установочный скрипт для Windows

Write-Host "🎮 Terminal Game Manager - Установка" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Проверяем Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python найден: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python не найден!" -ForegroundColor Red
    Write-Host "Скачай Python с: https://python.org" -ForegroundColor Yellow
    Write-Host "Или установи через Microsoft Store" -ForegroundColor Yellow
    exit 1
}

# Создаем временную папку
$tempDir = "$env:TEMP\terminal-game-manager"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

try {
    Write-Host "`n📥 Скачиваю игру..." -ForegroundColor Yellow
    
    # Скачиваем основной код
    Invoke-WebRequest -Uri "https://github.com/platonzhuman/terminal-game-manager/archive/main.zip" -OutFile "$tempDir\game.zip"
    
    Write-Host "📦 Распаковываю..." -ForegroundColor Yellow
    Expand-Archive -Path "$tempDir\game.zip" -DestinationPath "$tempDir" -Force
    
    # Копируем файлы в текущую директорию
    $sourceDir = "$tempDir\terminal-game-manager-main"
    Copy-Item -Path "$sourceDir\*" -Destination "." -Recurse -Force
    
    Write-Host "✅ Установка завершена!" -ForegroundColor Green
    Write-Host "`n🎮 Запускаю игру..." -ForegroundColor Cyan
    
    # Запускаем игру
    python -m tgm.main
    
} catch {
    Write-Host "❌ Ошибка при установке: $_" -ForegroundColor Red
    Write-Host "Попробуй установить вручную:" -ForegroundColor Yellow
    Write-Host "1. Скачай ZIP с https://github.com/platonzhuman/terminal-game-manager" -ForegroundColor Yellow
    Write-Host "2. Распакуй и запусти: python -m tgm.main" -ForegroundColor Yellow
} finally {
    # Удаляем временные файлы
    Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
}

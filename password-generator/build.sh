#!/bin/bash

# Скрипт для автоматической сборки RPM пакета

set -e  # Останавливаем выполнение при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Сборка RPM пакета для Генератора паролей ===${NC}"

# Проверка наличия необходимых инструментов
echo -e "${YELLOW}Проверка зависимостей...${NC}"

if ! command -v rpmbuild &> /dev/null; then
    echo -e "${RED}Ошибка: rpmbuild не установлен${NC}"
    echo "Установите: sudo dnf install rpm-build rpmdevtools"
    exit 1
fi

if ! command -v pyinstaller &> /dev/null; then
    echo -e "${YELLOW}Установка PyInstaller...${NC}"
    pip3 install pyinstaller
fi

# Настройка переменных
NAME="password-generator"
VERSION="1.0"
RELEASE="1"
ARCH=$(uname -m)

# Создание структуры директорий для rpmbuild
echo -e "${YELLOW}Настройка окружения для сборки...${NC}"
rpmdev-setuptree

# Создание временной директории для сборки
BUILD_DIR=$(mktemp -d)
echo -e "${YELLOW}Временная директория сборки: $BUILD_DIR${NC}"

# Копирование файлов в SOURCES
echo -e "${YELLOW}Копирование исходных файлов...${NC}"
cp password_generator.py ~/rpmbuild/SOURCES/
cp password-generator.desktop ~/rpmbuild/SOURCES/
cp LICENSE ~/rpmbuild/SOURCES/ 2>/dev/null || echo "LICENSE файл не найден"
cp README.md ~/rpmbuild/SOURCES/ 2>/dev/null || echo "README.md файл не найден"
cp icon.png ~/rpmbuild/SOURCES/ 2>/dev/null || echo "icon.png не найден (опционально)"

# Копирование spec файла
cp password-generator.spec ~/rpmbuild/SPECS/

# Сборка пакета
echo -e "${YELLOW}Запуск сборки RPM...${NC}"
cd ~/rpmbuild/SPECS
rpmbuild -ba password-generator.spec

# Проверка результата
if [ $? -eq 0 ]; then
    echo -e "${GREEN}=== Сборка успешно завершена! ===${NC}"
    
    # Определяем архитектуру для выходного файла
    if [ "$ARCH" = "x86_64" ]; then
        RPM_ARCH="x86_64"
    else
        RPM_ARCH="noarch"
    fi
    
    RPM_FILE="$HOME/rpmbuild/RPMS/$RPM_ARCH/$NAME-$VERSION-$RELEASE.$RPM_ARCH.rpm"
    
    if [ -f "$RPM_FILE" ]; then
        echo -e "${GREEN}RPM пакет создан: $RPM_FILE${NC}"
        
        # Копирование RPM в текущую директорию
        cp "$RPM_FILE" ./
        echo -e "${GREEN}Копия пакета сохранена в текущей директории${NC}"
        
        # Показ информации о пакете
        echo -e "\n${YELLOW}Информация о пакете:${NC}"
        rpm -qpi "$RPM_FILE"
        
        echo -e "\n${YELLOW}Для установки выполните:${NC}"
        echo "sudo rpm -i $NAME-$VERSION-$RELEASE.$RPM_ARCH.rpm"
        echo "или"
        echo "sudo dnf install ./$NAME-$VERSION-$RELEASE.$RPM_ARCH.rpm"
    else
        echo -e "${RED}Ошибка: RPM файл не найден${NC}"
        exit 1
    fi
else
    echo -e "${RED}Ошибка при сборке RPM${NC}"
    exit 1
fi

# Очистка
rm -rf "$BUILD_DIR"
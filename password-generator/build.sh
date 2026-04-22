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

# Проверка rpmbuild
if ! command -v rpmbuild &> /dev/null; then
    echo -e "${RED}Ошибка: rpmbuild не установлен${NC}"
    echo "Установите: sudo dnf install rpm-build rpmdevtools"
    exit 1
fi

# Проверка и установка Python и pip
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Ошибка: python3 не установлен${NC}"
    echo "Установите: sudo dnf install python3"
    exit 1
fi

# Определяем команду pip (может быть pip3 или pip)
PIP_CMD=""
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo -e "${YELLOW}pip не найден. Установка python3-pip...${NC}"
    sudo dnf install -y python3-pip
    PIP_CMD="pip3"
fi

# Проверка и установка PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo -e "${YELLOW}Установка PyInstaller...${NC}"
    $PIP_CMD install --user pyinstaller
    
    # Добавляем путь к локальным пакетам Python в PATH
    export PATH="$HOME/.local/bin:$PATH"
    
    # Проверяем, что pyinstaller теперь доступен
    if ! command -v pyinstaller &> /dev/null; then
        echo -e "${RED}Ошибка: не удалось установить PyInstaller${NC}"
        echo "Попробуйте установить через системный пакет:"
        echo "sudo dnf install pyinstaller"
        exit 1
    fi
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

# Проверка наличия всех необходимых файлов
if [ ! -f "password_generator.py" ]; then
    echo -e "${RED}Ошибка: password_generator.py не найден${NC}"
    exit 1
fi

if [ ! -f "password-generator.desktop" ]; then
    echo -e "${RED}Ошибка: password-generator.desktop не найден${NC}"
    exit 1
fi

cp password_generator.py ~/rpmbuild/SOURCES/
cp password-generator.desktop ~/rpmbuild/SOURCES/

# Копирование опциональных файлов
if [ -f "LICENSE" ]; then
    cp LICENSE ~/rpmbuild/SOURCES/
else
    echo -e "${YELLOW}Предупреждение: LICENSE файл не найден${NC}"
fi

if [ -f "README.md" ]; then
    cp README.md ~/rpmbuild/SOURCES/
else
    echo -e "${YELLOW}Предупреждение: README.md файл не найден${NC}"
fi

if [ -f "icon.png" ]; then
    cp icon.png ~/rpmbuild/SOURCES/
else
    echo -e "${YELLOW}Предупреждение: icon.png не найден (опционально)${NC}"
fi

# Копирование spec файла
if [ ! -f "password-generator.spec" ]; then
    echo -e "${RED}Ошибка: password-generator.spec не найден${NC}"
    exit 1
fi

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
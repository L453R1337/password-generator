#!/bin/bash

echo "Установка зависимостей для сборки RPM..."

# Обновление системы
sudo dnf update -y

# Установка инструментов сборки RPM
sudo dnf install -y rpm-build rpmdevtools

# Установка Python и инструментов разработки
sudo dnf install -y python3 python3-devel python3-pip python3-tkinter tk

# Установка PyInstaller
sudo dnf install -y pyinstaller || sudo pip3 install pyinstaller

# Установка дополнительных инструментов
sudo dnf install -y desktop-file-utils ImageMagick

echo "Система готова к сборке RPM!"
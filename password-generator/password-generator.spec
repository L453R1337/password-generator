%define name password-generator
%define version 1.0
%define release 1

Name:           %{name}
Version:        %{version}
Release:        %{release}%{?dist}
Summary:        Secure password generator
Summary(ru):    Генератор надёжных паролей

License:        MIT
URL:            https://github.com/yourusername/password-generator

# Для бинарного файла, собранного с PyInstaller
BuildArch:      x86_64

# Зависимости времени выполнения
Requires:       tk
Requires:       python3
Requires:       python3-tkinter
Requires:       hicolor-icon-theme

%description
A secure password generator that creates cryptographically strong passwords
meeting modern security standards.

Features:
- Generation of passwords with minimum 12 characters
- Support for uppercase, lowercase, digits and special characters
- Password strength validation
- Copy to clipboard functionality
- Save to file option
- Intuitive graphical interface

%description -l ru
Генератор надёжных паролей, создающий криптографически стойкие пароли,
соответствующие современным стандартам безопасности.

Возможности:
- Генерация паролей длиной от 12 символов
- Поддержка заглавных и строчных букв, цифр и спецсимволов
- Проверка надёжности пароля
- Копирование в буфер обмена
- Сохранение в файл
- Интуитивный графический интерфейс

%prep
# Создаем директорию для сборки
rm -rf %{_builddir}/%{name}-%{version}
mkdir -p %{_builddir}/%{name}-%{version}

# Копируем исходные файлы
cp %{_sourcedir}/password_generator.py %{_builddir}/%{name}-%{version}/
cp %{_sourcedir}/password-generator.desktop %{_builddir}/%{name}-%{version}/
cp %{_sourcedir}/LICENSE %{_builddir}/%{name}-%{version}/
cp %{_sourcedir}/README.md %{_builddir}/%{name}-%{version}/

# Копируем иконку если есть
if [ -f %{_sourcedir}/icon.png ]; then
    cp %{_sourcedir}/icon.png %{_builddir}/%{name}-%{version}/
fi

%build
cd %{_builddir}/%{name}-%{version}

# Проверка наличия PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    # Пробуем установить через pip
    if command -v pip3 &> /dev/null; then
        pip3 install --user pyinstaller
        export PATH="$HOME/.local/bin:$PATH"
    elif command -v pip &> /dev/null; then
        pip install --user pyinstaller
        export PATH="$HOME/.local/bin:$PATH"
    else
        echo "Ошибка: PyInstaller не установлен и pip не найден"
        echo "Установите PyInstaller: sudo dnf install pyinstaller"
        exit 1
    fi
fi

# Сборка исполняемого файла с PyInstaller
pyinstaller --onefile \
            --windowed \
            --name="%{name}" \
            password_generator.py

%install
cd %{_builddir}/%{name}-%{version}

# Создание директорий для установки
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}

# Установка бинарного файла
install -m 755 dist/%{name} %{buildroot}%{_bindir}/%{name}

# Установка desktop файла
install -m 644 %{name}.desktop %{buildroot}%{_datadir}/applications/

# Установка документации
install -m 644 README.md %{buildroot}%{_datadir}/doc/%{name}/
install -m 644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/

# Установка иконок (если есть)
if [ -f icon.png ]; then
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
    
    # Конвертируем и создаем разные размеры иконок
    convert icon.png -resize 48x48 %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
    convert icon.png -resize 64x64 %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
    convert icon.png -resize 128x128 %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
    convert icon.png -resize 256x256 %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
fi

%clean
rm -rf %{_builddir}/%{name}-%{version}

%post
# Обновление кэша иконок
if [ -f %{_datadir}/icons/hicolor/48x48/apps/%{name}.png ]; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    if [ -x /usr/bin/gtk-update-icon-cache ]; then
        /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    fi
fi

# Обновление кэша desktop файлов
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database &>/dev/null || :
fi

%postun
# Обновление кэша иконок при удалении
if [ $1 -eq 0 ]; then
    if [ -f %{_datadir}/icons/hicolor/48x48/apps/%{name}.png ]; then
        touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
        if [ -x /usr/bin/gtk-update-icon-cache ]; then
            /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
        fi
    fi
    
    if [ -x /usr/bin/update-desktop-database ]; then
        /usr/bin/update-desktop-database &>/dev/null || :
    fi
fi

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%doc %{_datadir}/doc/%{name}/README.md
%license %{_datadir}/licenses/%{name}/LICENSE
%if 0%{?with_icons}
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%endif

%changelog
* Tue Apr 22 2026 Your Name <your.email@example.com> - 1.0-1
- Initial RPM release with PyInstaller binary
%define name password-generator
%define version 1.0
%define release 1
%define unmangled_name password-generator

Name:           %{name}
Version:        %{version}
Release:        %{release}%{?dist}
Summary:        Secure password generator
Summary(ru):    Генератор надёжных паролей

License:        MIT
URL:            https://github.com/yourusername/password-generator
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  desktop-file-utils

Requires:       python3
Requires:       python3-tkinter
Requires:       hicolor-icon-theme

%description
A secure password generator that creates cryptographically strong passwords
meeting modern security standards.

%description -l ru
Генератор надёжных паролей, создающий криптографически стойкие пароли,
соответствующие современным стандартам безопасности.

%prep
%setup -q

%build
%py3_build

%install
%py3_install

# Создание директорий
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

# Установка desktop файла
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    %{name}.desktop

# Установка иконок (если есть)
# cp icons/48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
# cp icons/64x64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
# cp icons/128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
# cp icons/scalable.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/password_generator.py
%{_datadir}/applications/%{name}.desktop
# %{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
* Tue Apr 22 2026 Your Name <your.email@example.com> - 1.0-1
- Initial RPM release
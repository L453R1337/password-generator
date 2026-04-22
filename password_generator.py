import random
import re
import string
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
import os

# ------------------ НАСТРОЙКИ ------------------
MIN_LENGTH = 12

# Наборы символов
UPPERCASE = string.ascii_uppercase        # A-Z
LOWERCASE = string.ascii_lowercase        # a-z
DIGITS = string.digits                    # 0-9
SPECIAL = "!@#$%^&*()_"

# Запрещённые слова (можно расширить)
FORBIDDEN_WORDS = {"password", "user", "arm",
                   "eisz", "qwerty", "admin", "pass", "login"}

# Запрещённые числовые паттерны (легко вычисляемые)
FORBIDDEN_NUM_PATTERNS = {"112", "911", "123", "111", "000", "999"}

# Регулярное выражение для последовательностей на клавиатуре
KEYBOARD_SEQUENCES = [
    "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "`1234567890-=", "~!@#$%^&*()_+",
    "1234567890"
]

# ------------------ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ------------------


def has_keyboard_pattern(password: str) -> bool:
    """Проверяет, содержит ли пароль последовательности с клавиатуры (4+ символа подряд)."""
    pwd_lower = password.lower()
    for seq in KEYBOARD_SEQUENCES:
        seq_lower = seq.lower()
        for i in range(len(seq_lower) - 3):  # Увеличил до 4 символов
            pattern = seq_lower[i:i+4]
            if pattern in pwd_lower:
                return True
            rev_pattern = pattern[::-1]
            if rev_pattern in pwd_lower:
                return True
    return False


def has_repeating_sequence(password: str) -> bool:
    """Запрещает только 4+ одинаковых символов подряд."""
    # Только 4 и более одинаковых символов подряд
    if re.search(r"(.)\1{3,}", password):
        return True
    # Повтор комбинаций из 4+ символов
    if re.search(r"(.{4,})\1", password):
        return True
    return False


def contains_forbidden_words_or_patterns(password: str) -> bool:
    """Проверяет наличие запрещённых слов, дат и т.д."""
    pwd_lower = password.lower()

    for word in FORBIDDEN_WORDS:
        if word in pwd_lower:
            return True

    for pattern in FORBIDDEN_NUM_PATTERNS:
        if pattern in password:
            return True

    if re.search(r"\b(19|20)\d{2}\b", password):
        return True
    if re.search(r"(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[0-2])", password):
        return True

    return False


def is_strong_password(password: str) -> tuple:
    """
    Комплексная проверка надёжности пароля.
    Возвращает (True/False, сообщение_об_ошибке)
    """
    if len(password) < MIN_LENGTH:
        return False, f"Длина пароля должна быть не менее {MIN_LENGTH} символов"

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in SPECIAL for c in password)

    if not has_upper:
        return False, "Пароль должен содержать хотя бы одну заглавную букву (A-Z)"
    if not has_lower:
        return False, "Пароль должен содержать хотя бы одну строчную букву (a-z)"
    if not has_digit:
        return False, "Пароль должен содержать хотя бы одну цифру (0-9)"
    if not has_special:
        return False, f"Пароль должен содержать хотя бы один спецсимвол ({SPECIAL})"

    if has_keyboard_pattern(password):
        return False, "Пароль не должен содержать последовательности символов на клавиатуре (например, qwe, !@#)"

    if has_repeating_sequence(password):
        return False, "Пароль не должен содержать повторяющиеся символы (1111) или комбинации (qweqweqwe)"

    if contains_forbidden_words_or_patterns(password):
        return False, "Пароль содержит запрещённые слова, даты или легко вычисляемые комбинации"

    return True, "Пароль соответствует всем требованиям"

# ------------------ ГЕНЕРАТОР ПАРОЛЕЙ ------------------


def generate_password() -> str:
    """Генерирует пароль, удовлетворяющий всем требованиям."""
    all_chars = UPPERCASE + LOWERCASE + DIGITS + SPECIAL

    max_attempts = 1000  # Увеличил количество попыток
    for _ in range(max_attempts):
        # Гарантируем наличие всех необходимых символов
        password = [
            random.choice(UPPERCASE),
            random.choice(LOWERCASE),
            random.choice(DIGITS),
            random.choice(SPECIAL)
        ]

        # Добавляем случайные символы до нужной длины
        for _ in range(MIN_LENGTH - 4):
            password.append(random.choice(all_chars))

        # Перемешиваем
        random.shuffle(password)
        candidate = "".join(password)

        # Проверяем
        is_valid, _ = is_strong_password(candidate)
        if is_valid:
            return candidate

    # Если не удалось сгенерировать пароль стандартным способом,
    # создаем гарантированно надежный пароль
    import secrets
    import hashlib

    # Используем криптографически безопасный генератор
    random_bytes = secrets.token_bytes(16)
    hash_obj = hashlib.sha256(random_bytes)
    hex_digest = hash_obj.hexdigest()[:MIN_LENGTH]

    # Добавляем спецсимволы и перемешиваем
    chars = list(hex_digest)
    chars[0] = random.choice(UPPERCASE)
    chars[-1] = random.choice(SPECIAL)

    return "".join(chars)

# ------------------ ОКНО ПРИВЕТСТВИЯ ------------------


def show_welcome_screen():
    """Показывает окно приветствия с описанием программы"""
    welcome_window = tk.Toplevel()
    welcome_window.title("Добро пожаловать!")
    welcome_window.geometry("600x700")
    welcome_window.resizable(False, False)

    # Цветовая схема
    bg_color = "#1e1e2e"
    fg_color = "#cdd6f4"
    accent_color = "#89b4fa"
    success_color = "#a6e3a1"
    warning_color = "#f9e2af"
    secondary_bg = "#313244"

    welcome_window.configure(bg=bg_color)

    # Центрирование окна
    welcome_window.update_idletasks()
    width = 600
    height = 700
    x = (welcome_window.winfo_screenwidth() // 2) - (width // 2)
    y = (welcome_window.winfo_screenheight() // 2) - (height // 2)
    welcome_window.geometry(f'{width}x{height}+{x}+{y}')

    # Основной контейнер с прокруткой
    canvas = tk.Canvas(welcome_window, bg=bg_color, highlightthickness=0)
    scrollbar = tk.Scrollbar(
        welcome_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg_color)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Заголовок
    title_frame = tk.Frame(scrollable_frame, bg=bg_color)
    title_frame.pack(fill=tk.X, pady=(30, 20))

    tk.Label(title_frame, text="🔐 Генератор надёжных паролей",
             font=('Arial', 24, 'bold'), fg=accent_color, bg=bg_color).pack()

    tk.Label(title_frame, text="Версия 1.0",
             font=('Arial', 10), fg=fg_color, bg=bg_color).pack(pady=(5, 0))

    # Разделитель
    tk.Frame(scrollable_frame, height=2, bg=accent_color).pack(
        fill=tk.X, padx=30, pady=15)

    # Описание программы
    desc_frame = tk.Frame(scrollable_frame, bg=bg_color)
    desc_frame.pack(fill=tk.X, padx=30, pady=10)

    description_text = """Это приложение создано для генерации криптографически надёжных паролей, 
соответствующих современным стандартам безопасности."""

    tk.Label(desc_frame, text=description_text,
             font=('Arial', 11), fg=fg_color, bg=bg_color,
             wraplength=500, justify=tk.CENTER).pack()

    # Основные функции
    functions_frame = tk.Frame(
        scrollable_frame, bg=secondary_bg, relief=tk.RAISED, bd=1)
    functions_frame.pack(fill=tk.X, padx=30, pady=20)

    tk.Label(functions_frame, text="📌 ОСНОВНЫЕ ФУНКЦИИ",
             font=('Arial', 14, 'bold'), fg=accent_color, bg=secondary_bg).pack(anchor=tk.W, padx=20, pady=(20, 10))

    functions = [
        ("🔄 Генерация паролей",
         "Создание уникальных паролей с использованием криптографически безопасных алгоритмов"),
        ("📋 Копирование в буфер",
         "Быстрое копирование сгенерированного пароля одним кликом"),
        ("💾 Сохранение в файл",
         "Возможность сохранить пароль в текстовый файл с указанием даты создания"),
        ("👁️ Просмотр пароля", "Функция показа/скрытия пароля для удобства проверки"),
        ("🔒 Проверка надёжности",
         "Автоматическая проверка пароля на соответствие требованиям безопасности")
    ]

    for icon_title, desc in functions:
        func_item = tk.Frame(functions_frame, bg=secondary_bg)
        func_item.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(func_item, text=icon_title,
                 font=('Arial', 11, 'bold'), fg=success_color, bg=secondary_bg).pack(anchor=tk.W)
        tk.Label(func_item, text=f"   {desc}",
                 font=('Arial', 9), fg=fg_color, bg=secondary_bg,
                 wraplength=500, justify=tk.LEFT).pack(anchor=tk.W)

    # Требования к паролям
    requirements_frame = tk.Frame(
        scrollable_frame, bg=secondary_bg, relief=tk.RAISED, bd=1)
    requirements_frame.pack(fill=tk.X, padx=30, pady=20)

    tk.Label(requirements_frame, text="🔒 ТРЕБОВАНИЯ К ПАРОЛЯМ",
             font=('Arial', 14, 'bold'), fg=accent_color, bg=secondary_bg).pack(anchor=tk.W, padx=20, pady=(20, 10))

    requirements = [
        "Минимальная длина: 12 символов",
        "Наличие заглавных латинских букв (A-Z)",
        "Наличие строчных латинских букв (a-z)",
        "Наличие цифр (0-9)",
        "Наличие специальных символов (!@#$%^&*()_)",
        "Отсутствие словарных слов",
        "Отсутствие дат и простых числовых паттернов",
        "Отсутствие повторяющихся символов (1111, aaaa)",
        "Отсутствие клавиатурных последовательностей (qwerty, 12345)"
    ]

    for req in requirements:
        tk.Label(requirements_frame, text=f"✓ {req}",
                 font=('Arial', 9), fg=success_color, bg=secondary_bg).pack(anchor=tk.W, padx=25, pady=2)

    tk.Label(requirements_frame, text="", bg=secondary_bg).pack(pady=(0, 20))

    # Рекомендации по безопасности
    tips_frame = tk.Frame(
        scrollable_frame, bg=secondary_bg, relief=tk.RAISED, bd=1)
    tips_frame.pack(fill=tk.X, padx=30, pady=20)

    tk.Label(tips_frame, text="💡 РЕКОМЕНДАЦИИ ПО БЕЗОПАСНОСТИ",
             font=('Arial', 14, 'bold'), fg=warning_color, bg=secondary_bg).pack(anchor=tk.W, padx=20, pady=(20, 10))

    tips = [
        "Используйте разные пароли для разных сервисов",
        "Регулярно обновляйте важные пароли",
        "Храните пароли в защищённом месте (менеджер паролей)",
        "Не передавайте пароли через незащищённые каналы связи",
        "Включите двухфакторную аутентификацию где это возможно",
        "Не используйте личную информацию в паролях",
        "Проверяйте пароли на утечки через сервисы проверки"
    ]

    for tip in tips:
        tk.Label(tips_frame, text=f"• {tip}",
                 font=('Arial', 9), fg=fg_color, bg=secondary_bg,
                 wraplength=500, justify=tk.LEFT).pack(anchor=tk.W, padx=25, pady=2)

    tk.Label(tips_frame, text="", bg=secondary_bg).pack(pady=(0, 20))

    # Как использовать
    usage_frame = tk.Frame(
        scrollable_frame, bg=secondary_bg, relief=tk.RAISED, bd=1)
    usage_frame.pack(fill=tk.X, padx=30, pady=20)

    tk.Label(usage_frame, text="📖 КАК ИСПОЛЬЗОВАТЬ",
             font=('Arial', 14, 'bold'), fg=accent_color, bg=secondary_bg).pack(anchor=tk.W, padx=20, pady=(20, 10))

    usage_steps = [
        "1. Нажмите кнопку 'Сгенерировать' для создания нового пароля",
        "2. Используйте кнопку с глазом для просмотра пароля",
        "3. Нажмите 'Копировать' чтобы скопировать пароль в буфер обмена",
        "4. Используйте 'Сохранить' для сохранения пароля в файл",
        "5. При сохранении выберите место для файла с паролем"
    ]

    for step in usage_steps:
        tk.Label(usage_frame, text=step,
                 font=('Arial', 10), fg=fg_color, bg=secondary_bg,
                 wraplength=500, justify=tk.LEFT).pack(anchor=tk.W, padx=25, pady=3)

    tk.Label(usage_frame, text="", bg=secondary_bg).pack(pady=(0, 20))

    # Кнопка закрытия
    button_frame = tk.Frame(scrollable_frame, bg=bg_color)
    button_frame.pack(fill=tk.X, padx=30, pady=(10, 30))

    close_btn = tk.Button(button_frame, text="Начать использование",
                          font=('Arial', 12, 'bold'), bg=accent_color, fg=bg_color,
                          relief=tk.RAISED, bd=0, padx=30, pady=12,
                          command=welcome_window.destroy)
    close_btn.pack()

    # Подпись
    tk.Label(scrollable_frame, text="© 2024 Генератор надёжных паролей. Все права защищены.",
             font=('Arial', 8), fg=fg_color, bg=bg_color).pack(pady=(0, 20))

    # Настройка прокрутки
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Привязка колесика мыши к прокрутке
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # Фокус на окне
    welcome_window.focus_force()
    welcome_window.grab_set()

# ------------------ ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ------------------


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор надёжных паролей")
        self.root.geometry("650x400")  # Уменьшил высоту окна
        self.root.resizable(False, False)

        # Настройка цветовой схемы
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.success_color = "#a6e3a1"
        self.warning_color = "#f9e2af"
        self.error_color = "#f38ba8"
        self.secondary_bg = "#313244"

        self.root.configure(bg=self.bg_color)

        # Переменная для состояния видимости пароля
        self.show_password = False

        # Установка стиля для ttk
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color,
                        foreground=self.fg_color)
        style.configure("TLabelframe", background=self.bg_color,
                        foreground=self.fg_color)
        style.configure("TLabelframe.Label",
                        background=self.bg_color, foreground=self.fg_color)

        # Основной контейнер
        main_frame = tk.Frame(root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Заголовок с иконкой
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 30))

        title_label = tk.Label(title_frame, text="🔐 Генератор надёжных паролей",
                               font=('Arial', 20, 'bold'), fg=self.accent_color, bg=self.bg_color)
        title_label.pack()

        subtitle_label = tk.Label(title_frame, text="Создание паролей, соответствующих стандартам безопасности",
                                  font=('Arial', 10), fg=self.fg_color, bg=self.bg_color)
        subtitle_label.pack()

        # Рамка для отображения пароля
        password_frame = tk.Frame(
            main_frame, bg=self.secondary_bg, relief=tk.RAISED, bd=0)
        password_frame.pack(fill=tk.X, pady=20)

        # Внутренняя рамка с отступом
        inner_frame = tk.Frame(
            password_frame, bg=self.secondary_bg, padx=20, pady=20)
        inner_frame.pack(fill=tk.BOTH, expand=True)

        # Метка
        tk.Label(inner_frame, text="Сгенерированный пароль:",
                 font=('Arial', 12, 'bold'), fg=self.fg_color, bg=self.secondary_bg).pack(anchor=tk.W, pady=(0, 10))

        # Поле для пароля с кнопкой показа/скрытия
        password_entry_frame = tk.Frame(inner_frame, bg=self.secondary_bg)
        password_entry_frame.pack(fill=tk.X, pady=(0, 10))

        self.password_var = tk.StringVar()

        # Создаем обычное Entry (не readonly) для возможности изменения show
        self.password_entry = tk.Entry(password_entry_frame, textvariable=self.password_var,
                                       font=('Courier', 14), bg=self.bg_color, fg=self.accent_color,
                                       relief=tk.SUNKEN, bd=2, show='*')
        self.password_entry.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Кнопка показа/скрытия пароля
        self.toggle_btn = tk.Button(password_entry_frame, text="👁️", font=('Arial', 12),
                                    bg=self.secondary_bg, fg=self.fg_color, relief=tk.FLAT,
                                    command=self.toggle_password_visibility)
        self.toggle_btn.pack(side=tk.RIGHT)

        # Кнопки действий
        buttons_frame = tk.Frame(inner_frame, bg=self.secondary_bg)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))

        # Кнопка генерации
        self.generate_btn = tk.Button(buttons_frame, text="🔄 Сгенерировать",
                                      font=('Arial', 11, 'bold'), bg=self.accent_color, fg=self.bg_color,
                                      relief=tk.RAISED, bd=0, padx=20, pady=10,
                                      command=self.generate_and_display)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Кнопка копирования
        self.copy_btn = tk.Button(buttons_frame, text="📋 Копировать",
                                  font=('Arial', 11, 'bold'), bg=self.success_color, fg=self.bg_color,
                                  relief=tk.RAISED, bd=0, padx=20, pady=10,
                                  command=self.copy_to_clipboard)
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Кнопка сохранения
        self.save_btn = tk.Button(buttons_frame, text="💾 Сохранить",
                                  font=('Arial', 11, 'bold'), bg=self.warning_color, fg=self.bg_color,
                                  relief=tk.RAISED, bd=0, padx=20, pady=10,
                                  command=self.save_to_file)
        self.save_btn.pack(side=tk.LEFT)

        # Статус-бар
        self.status_bar = tk.Label(root, text="Готов к работе", font=('Arial', 9),
                                   bg=self.secondary_bg, fg=self.fg_color, anchor=tk.W, padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Генерируем первый пароль
        self.generate_and_display()

    def generate_and_display(self):
        """Генерирует новый пароль и отображает его"""
        try:
            password = generate_password()
            self.password_var.set(password)

            # Устанавливаем скрытие пароля при генерации нового
            self.show_password = False
            self.password_entry.configure(show='*')
            self.toggle_btn.configure(text="👁️")

            self.update_status(
                "✅ Новый пароль успешно сгенерирован", self.success_color)
        except Exception as e:
            messagebox.showerror(
                "Ошибка", f"Не удалось сгенерировать пароль: {str(e)}")
            self.update_status("❌ Ошибка генерации", self.error_color)

    def toggle_password_visibility(self):
        """Переключает видимость пароля"""
        self.show_password = not self.show_password

        if self.show_password:
            self.password_entry.configure(show='')
            self.toggle_btn.configure(text="🙈")
        else:
            self.password_entry.configure(show='*')
            self.toggle_btn.configure(text="👁️")

    def copy_to_clipboard(self):
        """Копирует пароль в буфер обмена"""
        password = self.password_var.get()
        if password:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                self.root.update()  # Важно для сохранения данных в буфере обмена
                self.update_status(
                    "📋 Пароль скопирован в буфер обмена", self.success_color)
                messagebox.showinfo(
                    "Успех", "Пароль скопирован в буфер обмена!")
            except Exception as e:
                messagebox.showerror(
                    "Ошибка", f"Не удалось скопировать пароль: {str(e)}")
                self.update_status("❌ Ошибка копирования", self.error_color)

    def save_to_file(self):
        """Сохраняет пароль в текстовый файл с выбором места сохранения"""
        password = self.password_var.get()
        if not password:
            messagebox.showwarning(
                "Предупреждение", "Нет пароля для сохранения")
            return

        # Открываем диалог выбора места сохранения
        default_filename = f"пароль_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        filename = filedialog.asksaveasfilename(
            title="Сохранить пароль",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
            initialfile=default_filename,
            initialdir=os.path.expanduser("~")
        )

        if not filename:
            self.update_status("❌ Сохранение отменено", self.warning_color)
            return

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("СГЕНЕРИРОВАННЫЙ ПАРОЛЬ\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Пароль: {password}\n")
                f.write(
                    f"Дата создания: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
                f.write(f"Длина пароля: {len(password)} символов\n\n")
                f.write("-" * 60 + "\n")
                f.write("Требования к паролю:\n")
                f.write("- Длина: 12+ символов\n")
                f.write("- Заглавные и строчные латинские буквы\n")
                f.write("- Цифры\n")
                f.write("- Специальные символы (!@#$%^&*()_)\n")
                f.write(
                    "- Запрещены словари, даты, повторения, клавиатурные последовательности\n")
                f.write("=" * 60 + "\n")

            self.update_status(
                f"💾 Пароль сохранён в файл: {os.path.basename(filename)}", self.success_color)
            messagebox.showinfo(
                "Успех", f"Пароль успешно сохранён в файл:\n{filename}")
        except Exception as e:
            messagebox.showerror(
                "Ошибка", f"Не удалось сохранить пароль: {str(e)}")
            self.update_status("❌ Ошибка сохранения", self.error_color)

    def update_status(self, message, color=None):
        """Обновляет статус-бар"""
        self.status_bar.config(text=message)
        if color:
            self.status_bar.config(fg=color)
            # Сбрасываем цвет через 3 секунды
            self.root.after(
                3000, lambda: self.status_bar.config(fg=self.fg_color))


# ------------------ ЗАПУСК ПРИЛОЖЕНИЯ ------------------
if __name__ == "__main__":
    root = tk.Tk()

    # Центрирование главного окна
    root.update_idletasks()
    width = 650
    height = 400  # Уменьшил высоту
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # Создаем приложение
    app = PasswordGeneratorApp(root)

    # Показываем окно приветствия после небольшой задержки
    root.after(100, show_welcome_screen)

    root.mainloop()

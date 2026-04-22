from setuptools import setup

setup(
    name="password-generator",
    version="1.0",
    description="Генератор надёжных паролей",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/password-generator",
    py_modules=["password_generator"],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "password-generator=password_generator:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
)

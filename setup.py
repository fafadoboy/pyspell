from setuptools import setup

setup(
    name='pyspell',
    version='0.1.2',
    packages=["pyspell", "pyspell.practice", "pyspell.sets"],
    include_package_data=True,
    install_requires=["click", "gtts", "tabulate"],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],    
    entry_points="""
        [console_scripts]
        pyspell=pyspell.cli:cli
    """,
)
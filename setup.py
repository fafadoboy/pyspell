from setuptools import setup    

setup(
    name='pyspell',
    version='0.1.1',
    packages=["pyspell", "pyspell.practice", "pyspell.sets"],
    install_requires=["click", "gtts", "tabulate"],
    # package_dir={'sqls': "scripts/sql"},
    package_data={'pyspell': ['../scripts/sql/tables_create.sql']},
    include_package_data=True,
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
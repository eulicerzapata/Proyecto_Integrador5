from setuptools import setup, find_packages

setup(
    name="proyecto_integrador",
    version="0.0.1",
    author="Eulicer Zapata Orrego & Dawin Salazar",
    author_email="eulicer.zapata@iudigital.edu.co",
    description="Proyecto integrador",
    # project uses a src/ layout; expose packages under src so editable installs work
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas>=2.0.0",
        "openpyxl",
        "requests",
        "beautifulsoup4",
        "matplotlib",
        "kagglehub[pandas-datasets]>=0.3.8",
        "seaborn",
        "pyarrow",
        "streamlit>=1.28.0",
        "plotly>=5.18.0"
    ],
)
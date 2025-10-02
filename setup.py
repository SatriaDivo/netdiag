"""
Setup script untuk netdiag package
Network Diagnostics Toolkit untuk educational purposes
"""

from setuptools import setup, find_packages
import os

# Baca README.md untuk long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='netdiag',
    version='1.0.0',
    description='Network Diagnostics Toolkit untuk educational purposes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Netdiag Developer',
    author_email='developer@netdiag.edu',
    url='https://github.com/yourusername/netdiag',
    
    # Klasifikasi package
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Networking',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    
    # Keywords untuk pencarian
    keywords='network diagnostics ping traceroute dns port-scan educational',
    
    # Package discovery (exclude test and development folders)
    packages=find_packages(exclude=['tests*', 'docs*', 'examples*', 'temp*', 'scratch*']),
    
    # Python version requirement
    python_requires='>=3.6',
    
    # Dependencies (menggunakan modul bawaan Python sebanyak mungkin)
    install_requires=[
        # Tidak ada external dependencies - hanya menggunakan standard library
    ],
    
    # Optional dependencies untuk fitur tambahan
    extras_require={
        'dev': ['pytest', 'black', 'flake8'],
        'test': ['pytest'],
    },
    
    # Data files yang disertakan
    package_data={
        'netdiag': ['*.md', '*.txt'],
    },
    
    # Entry points untuk CLI commands
    entry_points={
        'console_scripts': [
            'netdiag=netdiag.__main__:main',
        ],
    },
    
    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/SatriaDivo/netdiag/issues',
        'Source': 'https://github.com/SatriaDivo/netdiag',
        'Documentation': 'https://github.com/SatriaDivo/netdiag/blob/main/README.md',
    },
    
    # Metadata tambahan
    zip_safe=False,
    include_package_data=True,
)
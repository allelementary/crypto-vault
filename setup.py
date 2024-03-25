from setuptools import setup, find_packages

setup(
    name='crypto-vault',
    version='0.1.0',
    packages=find_packages(exclude=('tests', 'tests.*')),
    package_data={'crypto_vault': ['abi.json']},
    include_package_data=True,
    description='Efficiently encrypt data off-chain and store securely on the blockchain',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mikhail Antonov',
    author_email='allelementaryfor@gmail.com',
    url='https://github.com/allelementary/crypto-vault-off-chain',
    install_requires=[
        'web3',
        'cryptography',
        'pydantic',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
    ],
)

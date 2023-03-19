from setuptools import setup, find_packages

setup(
    name='git2gpt',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'openai',
        'tiktoken',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'git2gpt=git2gpt:main'
        ]
    }
)

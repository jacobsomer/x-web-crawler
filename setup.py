from setuptools import setup, find_packages

setup(
    name='x-web-crawler',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'selenium',
    ],
    entry_points={
        'console_scripts': [
            'x_automation=autofollow.x:main',
            'github_automation=autofollow.github:main',
        ],
    },
    author='Jacob Somer',
    author_email='somerjacob@gmail.com',
    description='A web crawler for x.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jacobsomer/autofollow',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

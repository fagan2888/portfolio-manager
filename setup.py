"""stockretriever"""

from setuptools import setup

setup(
    name='portfolio-manager',
    version='1.0',
    description='a web app that keeps track of your investment portfolio',
    url='https://github.com/gurch101/portfolio-manager',
    author='Gurchet Rai',
    author_email='gurch101@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='investment portfolio',
    setup_requires=[
        'stockretriever==1.0',
        'Flask==0.10.1',
        'passlib==1.6.2',
        'schedule==0.3.2',
        'requests==2.2.1'
    ]
)

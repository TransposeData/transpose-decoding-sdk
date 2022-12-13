from setuptools import find_packages, setup
with open('README.md', 'r') as f: long_description = f.read()
    
setup(
    name='transpose_defi_sdk',
    version='1.0.1',
    
    # meta
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    description='The Transpose DeFi SDK is a simple Python package for performing multi-chain DeFi analysis using the real-time Transpose SQL API.',
    keywords=['web3', 'defi', 'ethereum', 'transpose', 'prices', 'ohlc', 'data', 'analysis', 'blockchain', 'polygon'],
    license='MIT',
    
    # classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Database',
        'Topic :: Utilities'
    ],

    # homepage
    url='https://github.com/TransposeData/transpose-defi-sdk',
    
    # author
    author='Alex Langshur (alangshur)',
    author_email='alex@transpose.io',
    
    # packages
    packages=find_packages(exclude=['demo', 'tests']),

    # dependencies
    install_requires=[
        'pandas',
        'pip-chill',
        'plotly',
        'web3'
    ]
)
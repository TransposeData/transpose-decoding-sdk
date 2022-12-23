from setuptools import find_packages, setup
with open('README.md', 'r') as f: long_description = f.read()
    
setup(
    name='transpose_decoding_sdk',
    version='1.0.3',
    
    # meta
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    description='The Transpose Decoding SDK is a Python package that makes decoding contract activity on EVM blockchains as simple as possible. Simply specify a contract address and ABI to start streaming historical or live activity across decoded logs, transactions, and traces.',
    keywords=['web3', 'defi', 'ethereum', 'transpose', 'polygon', 'goerli', 'abi', 'decode', 'event', 'log', 'traces', 'rpc', 'api'],
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
    url='https://github.com/TransposeData/transpose-decoding-sdk',
    
    # author
    author='Alex Langshur (alangshur)',
    author_email='alex@transpose.io',
    
    # packages
    packages=find_packages(exclude=['demo', 'tests']),

    # dependencies
    install_requires=[
        'eth-event',
        'pip-chill',
        'dateutils',
        'web3'
    ]
)
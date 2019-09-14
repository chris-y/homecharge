from setuptools import setup, find_packages


setup(
    name='homecharge',
    description='Client for BP ChargeMaster HomeCharge API',
    author='James Muscat',
    author_email='jamesremuscat@gmail.com',
    url='https://githum.com/jamesremuscat/homecharge',
    packages=find_packages('src', exclude=["*/__tests__"]),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'simplejson',
    ],
    setup_requires=[
        'pytest-runner',
        'setuptools_scm'
    ],
    use_scm_version=True,
    tests_require=[
        'pytest',
    ]
)

from setuptools import setup, find_packages

setup(
    name = 'mmri',
    version = '0.2.0-dev',
    author = 'PlannerStack',
    author_email = 'contact@plannerstack.org',
    license = 'MIT',
    description = 'Testing code and data for the Beter Benutten MMRI project',
    long_description = open('README.rst').read(),
    url = 'http://github.com/plannerstack/testset',
    download_url = 'http://github.com/plannerstack/testset/archives/master',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    platforms = ['all'],
    entry_points = {
        'console_scripts': [
            'mmri-test-runner = mmri.test_runner:main',
        ],
    },
    install_requires = [
        'requests',
    ],
)

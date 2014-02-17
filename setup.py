from setuptools import setup, find_packages

version = '0.1'

entry_points = {
    'ckan.plugins': [
        "sentry = ckanext.sentry.plugin:SentryPlugin",
    ],
}

install_requires = ['raven']  # We need raven to connect to sentry

setup(
    name='ckanext-sentry',
    version=version,
    description="Hooks sentry's raven client into app middleware",
    long_description="Hooks sentry's raven client into app middleware",
    author="Samuele Santi",
    author_email="samuele.santi@trentorise.eu",
    url='http://rshk.github.io/ckanext-sentry',
    license='Affero GPL',
    classifiers=[],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.sentry'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points=entry_points,
)

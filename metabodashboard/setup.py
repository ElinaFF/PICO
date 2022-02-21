from setuptools import setup, find_packages

setup(
    name='MetaboDashboard',
    version='0.0.1',
    description='Metabo',
    author='Élina Francovic-Fontaine',
    # author_email='rogiervandergeer@godatadriven.com',
    # url='https://blog.godatadriven.com/setup-py',
    packages=find_packages(include=['metabodashboard', 'metabodashboard.*']),
    install_requires=[
        'dash==2.1.0',
        'dash-bio==0.9.0',
        'dash-bootstrap-components==1.0.2',
        'dash-core-components==2.0.0',
        'dash-html-components==2.0.0',
        'dash-renderer==1.0.0',
        'dash-table==5.0.0',
        'numpy==1.20.3',
        'pandas==1.2.5',
        'plotly==5.5.0',
        'fastcluster==1.2.4',
        'pyMSpec @ git+https://github.com/alexandrovteam/pyMSpec@v0.1',
        'msvlm @ git+https://github.com/francisbrochu/msvlm'
        ]
)

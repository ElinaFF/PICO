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
        'scipy==1.2.1',
        'dash',
        'dash-bio',
        'dash-bootstrap-components',
        'dash-core-components',
        'dash-html-components',
        'dash-renderer',
        'dash-table',
        'numpy>=1.16.5',
        'pandas',
        'plotly',
        'scikit-learn',
        # 'pyMSpec @ git+https://github.com/alexandrovteam/pyMSpec',
        # 'msvlm @ git+https://github.com/francisbrochu/msvlm'
        ]
)

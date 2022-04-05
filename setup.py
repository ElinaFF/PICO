from setuptools import setup, find_packages

setup(
    name='metabodashboard',
    version='0.0.1',
    description='Metabo',
    author='Élina Francovic-Fontaine',
    # author_email='rogiervandergeer@godatadriven.com',
    # url='https://blog.godatadriven.com/setup-py',
    packages=find_packages(include=['metabodashboard', 'metabodashboard.*']),
    install_requires=[
        'scipy',
        'dash',
        'dash-bio',
        'dash-bootstrap-components',
        'dash-core-components==2.0.0',
        'dash-html-components==2.0.0',
        'dash-renderer',
        'dash-table==5.0.0',
        'numpy==1.21.4',
        'pandas',
        'plotly',
        'scikit-learn',
        'umap-learn',
        #'openpyxl'
        # 'pyMSpec @ git+https://github.com/alexandrovteam/pyMSpec',
        # 'msvlm @ git+https://github.com/francisbrochu/msvlm'
        ],
    tests_require=['pytest', 'pytest-mock'],
)

from setuptools import setup, find_packages

setup(name='hellopy',
      version='1.0.0',
      description='Python template',
      packages=find_packages("src", exclude=('tests', 'docs')),
      package_dir={"": "src"},
      test_suite='tests',
      setup_requires=[
          "flake8"
      ]
      )

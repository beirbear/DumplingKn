from setuptools import setup

setup(name='server_stream',
      version='0.1.0',
      packages=['data_mining'],
      entry_points={
          'console_scripts': [
              'data_mining = data_mining.__main__:main'
          ]
      },
      )
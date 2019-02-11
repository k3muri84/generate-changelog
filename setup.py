from setuptools import setup

setup(name='generate-changelog',
      version='0.1',
      description='Generates changelog from Git based on Jira tickets',
      url='https://github.com/echorebel/generate-changelog',
      author='echorebel',
      author_email='echorebel@users.noreply.github.com',
      license='MIT',
      packages=['generator'],
      install_requires=[
          'jira',
      ],
      zip_safe=False)

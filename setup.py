from distutils.core import setup

setup(name='nhl',
      version='3.1',
      packages=['nhl'],
      scripts=['nhlstats.py'],
      description='Reads stats from nhl.com',
      author='Peter Stark',
      author_email='peterstark72@gmail.com',
      url='https://github.com/peterstark72/nhl',
      requires=['lxml'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: Free for non-commercial use',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 3.4',
          'Topic :: Utilities'
      ])

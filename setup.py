from distutils.core import setup
setup(name='nhl',
      version='2.1.1',
      packages=['nhl'],
      scripts=['nhlstats.py', 'nhlplayer.py'],
      description='Reads stats from nhl.com',
      author='Peter Stark',
      author_email='peterstark72@gmail.com',
      url='https://github.com/peterstark72/nhl',
      requires=['bs4','lxml'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: Free for non-commercial use',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities'
          ],
      )
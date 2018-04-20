from setuptools import setup

setup(name='talc',
      version='0.1.1',
      description='Time Annotations for Live Concerts Dataset',
      keywords='time annotations live concerts dataset',
      url='https://github.com/pnevyk/time-annotations-of-live-concerts-dataset',
      author='Petr Nevyhoštěný',
      author_email='petr.nevyhosteny@gmail.com',
      license='CC BY-SA',
      install_requires=['numpy', 'pandas', 'pytube>=9.2.0', 'av>=0.4.0', 'dtw'],
      packages=['talc'],
      package_data={'talc': ['data/*']},
      include_package_data=True,
      zip_safe=False)

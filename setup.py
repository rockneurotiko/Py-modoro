#!/usr/bin/env python

from distutils.core import setup

setup(name='Py-modoro',
      version='0.3',
      description='Pomodoro app with GUI writed in Python',
      author='Rock Neurotiko',
      author_email='miguelglafuente@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['pygame'],
      license='GNU GPL v3',
      scripts=["Py-modoro.py"],
      packages=["menuApps", "libs"],
      py_modules=["GUI", "pomodoro"],
     )
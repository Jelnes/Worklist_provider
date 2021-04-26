#!/usr/bin/env python3
import setuptools

setuptools.setup(
    name='pyworklistserver',
    version='1.0',
    description='DICOM Worklist server',
    author='Jøger Hansegård',
    author_email='joger.hansegard@ge.com',
    packages=['pyworklistserver'],
    url='http://nohorsub01.euro.med.ge.com/svn/vivid/aurora/trunk/tool/PyWorklistServer/',
    install_requires=[
        'pydicom>=2.1.2',
        'pynetdicom>=1.5.5'
    ]
)

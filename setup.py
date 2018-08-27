from setuptools import setup
import os

datadir = os.path.join("share","data")
datafiles = [(d,[os.path.join(d,f) for f in files]) for d, folders, files in os.walk(datadir)]

setup(name='clinstagram',
    version='0.0.0.1',
    description='A CLI Instagram client',
    long_description="",
    url='https://github.com/Gabrock94/clinstagram',
    download_url='',
    author='Giulio Gabrieli',
    author_email='gack94@gmail.com',
    license='GPL-3.0',
    packages=['clinstagram'],      
    install_requires=[
        'InstagramApi'
    ],
    keywords = ["Instagram"],
    classifiers = [ 
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License (GPL)',
        
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=False,
    include_package_data=True,
    data_files = datafiles,
    entry_points = {
       "console_scripts": ['clinstagram = clinstagram.clinstagram:main']
    }
)


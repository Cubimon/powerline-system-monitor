from distutils.core import setup

setup(name="powerline-system-monitor",
      version="1.0",
      description="several function to monitor your system in Powerline",
      author="Cubimon",
      author_email="cubimon93@gmail.com",
      packages=["powerlinesystemmonitor"],
      install_requires=[
          "psutil"
      ]
     )

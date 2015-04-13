.. _getting_started:


***************
Getting started
***************

UV-CDAT (Ultrascale Visualization Climate Data Analysis Tools) is a powerful and complete front-end to a rich set of visual-data exploration and analysis capabilities well suited for climate-data analysis problems. For more details visit http://uv-cdat.org/

UV-CDAT Installation Guide
==========================

Dependencies on Linux 
-----------------------

The following are dependencies need to be installed before installing UV-CDAT in all   Linux distributions

* git
* libqt4-dev (under RedHAT the system qt isn't working, user will need to get the binaries from the website)
* libpng-dev
* libxml2-dev
* libxslt-dev
* xorg-dev
* sqlite3
* libsqlite3-dev
* libbz2-dev
* libgdbm-dev
* libxt-dev
* openssl-dev (libssl-dev)
* gfortran
* g++
* qt4-dev-tools / qtcreator 
* tcl-dev
* tk-dev
* libgdbm-dev
* libdb4.8-dev
* yasm
* grace
* grads

Dependencies on Ubuntu (extra dependencies) 
------------------------------------------

* libicu48
* libxi-dev
* libglu1-mesa-dev
* libgl1-mesa-dev
* libqt4-opengl-dev


Dependencies on CentOS 6.3 (extra dependencies)
-----------------------------------------------

* bzip2-devel
* dbus-devel
* dbus-c++-devel
* dbus-glib-devel
* gtkglext-devel
* mesalibGL
* mesalibGLU
* openGL
* gstreamer-devel
* gstreamer-plugins-base*devel
* gstreamer-plugins-bad*devel
* gstreamer-plugins-good*devel
* libcurl4
* openssl-devel

Download UV-CDAT Binary
=======================

* More detailed system requirements can be found `here <https://github.com/UV-CDAT/uvcdat/wiki/System-Requirements>`_

* UV-CDAT latest releases binary tar ball can be found `here <http://sourceforge.net/projects/cdat/files/Releases/UV-CDAT/>`_

* Download UV-CDAT latest binary version (2.0.0 as on Nov-2014) from `here <http://sourceforge.net/projects/cdat/files/Releases/UV-CDAT/2.0.0/>`_  with respect to your linux distribution.

* You will need admin privileges to install UV-CDAT in your system.

Installation on Linux  (Pre-Built Binary)   
=========================================

**Step 1:** Download and untar the binaries matching best your OS.

    $ cd /
    $ sudo tar xjvf UV-CDAT-[version-no]-[your OS here].tar.bz2

**Step 2:** For Mac and RH6 ONLY

 * Download the tarsal containing the version of QT UVCDAT has been compiled against RedHAT6
      $ cd /
      $ sudo tar xjvf qt-RH6-64bit-4.8.0.tar.bz2
 * Mac
      double click the .dmg file and follow instructions


**Step 3:** Set Environment Variables

 * Bash users:
   		$ source /usr/local/uvcdat/[version-no]/bin/setup_cdat.sh

 * t/csh users
   		$ source /usr/local/uvcdat/[version-no]/bin/setup_cdat.csh
	
**Step 4:** Set Alias Paths

	In your system ~/.bash_aliases or ~/.bashrc  add the following 4 lines.
	
		source /usr/local/uvcdat/2.0.0/bin/setup_cdat.sh
		
		alias  uvcdat = '/usr/local/uvcdat/2.0.0/bin/python'
		
		alias  uvcdat-gui = '/usr/local/uvcdat/2.0.0/bin/uvcdat'
		
		alias  uvcdscan = '/usr/local/uvcdat/2.0.0/bin/cdscan'
	
	Here shown version 2.0.0 for example only. User need to set proper version no whichever they installed in their system.

**Step 5:** Start enjoying UVCDAT  

 * GUI
	* Type  $ uvcdat-gui  in your linux terminal to use gui

 * Command Line Python 
	* Type $ uvcdat  in your linux terminal to use python shell 
	* Type $ uvcdat  sample_program.py to execute any uvcdat support python programs.
 * Cdscan
	* Type $ uvcdsan  –x out.xml *.nc  to scan all available nc files and make links into small xml file which can be used to load all nc files data inside uvcdat scripts from single xml file.

Installation on Linux  (Build From Source)
==========================================
   
* User can visit the following links to install from source. For AIX, UNIX kind of systems, its better start to build and install from UV-CDAT latest source itself.

* Download UV-CDAT latest Source Code from the following link
	* https://github.com/UV-CDAT/uvcdat/releases

* Guide to Install from Source
	* http://uv-cdat.org/installing.html
	* https://github.com/UV-CDAT/uvcdat/wiki/zold-Building-UVCDAT

Installation on Ubuntu 
======================

Current Stable Release 2.0 Supporting for **Ubuntu 13.x** and **14.x**

**System Requirements**

$ sudo apt-get install cmake cmake-curses-gui wget libqt4-dev libpng12-dev libxml2-dev libxslt1-dev xorg-dev sqlite3 libsqlite3-dev libbz2-dev libgdbm-dev libxt-dev libssl-dev gfortran g++ qt4-dev-tools tcl-dev tk-dev libgdbm-dev libdb-dev libicu-dev libxi-dev libglu1-mesa-dev libgl1-mesa-dev libqt4-opengl-dev libbz2-dev grads grace

Installing the Binaries (Strongly Suggested)
----------------------------------------------

You must be Root

$ sudo -s

$ cd /

$ wget http://sourceforge.net/projects/cdat/files/Releases/UV-CDAT/2.0.0/UV-CDAT-2.0.0-Ubuntu-14.04-64bit.tar.gz

$ tar xvjf UV-CDAT-2.0.0-Ubuntu-14.04-64bit.tar.gz

$ source /usr/local/uvcdat/2.0.0/bin/setup_runtime.sh

Running UV-CDAT GUI

(Don't forget to source setup_runtime.sh)

$ uvcdat

Bash users add source /usr/local/uvcdat/2.0.0/bin/setup_runtime.sh to your ~/.bashrc file

Csh users add source /usr/local/uvcdat/2.0.0/bin/setup_runtime.csh to your ~/.cshrc file

Set aliases in your bashrc file as mentioned in the previous section.

https://github.com/UV-CDAT/uvcdat/wiki/Installation-on-Ubuntu


Installation on RedHat, Fedora & CentOS 
--------------------------------------------

Current Stable Release 2.0 Supporting for **RedHat6** / **CentOS6**

System Requirements (Must be Root)

You must have access to the EPEL Repos `help link <http://www.thegeekstuff.com/2012/06/enable-epel-repository>`_ 

$ sudo yum install cmake cmake-gui wget libpng-devel libxml2-devel libxslt-devel xorg* sqlite-devel bzip2 gdbm-devel libXt-devel openssl-devel gcc-gfortran libgfortran tcl-devel tk-devel libdbi-devel libicu-devel libXi-devel mesa-libGLU-devel mesa-libGL-devel PyQt4-devel gcc-c++ patch grace grads
Installation Qt Binary :

$ cd /

$ wget http://sourceforge.net/projects/cdat/files/Releases/UV-CDAT/2.0.0/qt-CentOS-6.5-RedHat6-64bit-4.8.4.tar.bz2

$ tar xvjf qt-CentOS-6.5-RedHat6-64bit-4.8.4.tar.bz2

please add Qt to your path (example in bash) add this to your .bashrc

  export Qt=/usr/local/uvcdat/Qt/4.8.4/bin/
  
  export PATH=$PATH:$Qt
  
Installing the Binaries (Strongly Suggested)

You must be Root

$ sudo -s

$ cd /

$ wget http://sourceforge.net/projects/cdat/files/Releases/UV-CDAT/2.0.0/UV-CDAT-2.0.0-CentOS6.5-RedHat6-64bit.tar.gz

$ tar xvjf  UV-CDAT-2.0.0-CentOS6.5-RedHat6-64bit.tar.gz

$ source /usr/local/uvcdat/2.0.0/bin/setup_runtime.sh

Set aliases in your bashrc file as mentioned in the previous section.

Bash users add source /usr/local/uvcdat/2.0.0/bin/setup_runtime.sh to your ~/.bashrc file

Csh users add source /usr/local/uvcdat/2.0.0/bin/setup_runtime.csh to your ~/.cshrc file

https://github.com/UV-CDAT/uvcdat/wiki/installation-on-RedHat---CentOS 


UV-CDAT Documentation 
======================

Official Documentation 
----------------------

	* `CDMS <http://uv-cdat.org/documentation/cdms/cdms.html>`_ Manual 
	* UV-CDAT `Utilities <http://uv-cdat.org/documentation/utilities/utilities.html>`_ Manual 
	* `VCS <http://uv-cdat.org/documentation/vcs/vcs.html>`_ Manual 

Useful Tips & Tricks
---------------------
	
	* http://www.johnny-lin.com/cdat_tips/
	* http://drclimate.wordpress.com/2014/01/02/a-beginners-guide-to-scripting-with-uv-cdat/
	* http://tuxcoder.wordpress.com/category/python/cdat/
	* http://tuxcoder.wordpress.com/category/uvcdat-2/

Slides 
------

	* Lesson-1 `Python An Introduction <https://www.scribd.com/doc/56253490/Lesson1-Python-An-Introduction>`_
	* Lesson-2 `Numpy Arrays <https://www.scribd.com/doc/56254041/Lesson2-Numpy-Arrays>`_
	* Lesson-3 `cdutil_genutil <https://www.scribd.com/doc/56254387/Lesson3-cdutil-genutil>`_
	* Lesson-4 `VCS_XmGrace_Graphics <https://www.scribd.com/doc/56254572/Lesson4-VCS-XmGrace-CDAT-Graphics>`_

IPython With Interactive Live Execution Examples Outputs
---------------------------------------------------------

	* Introduction to `NumPy Arrays <http://nbviewer.ipython.org/github/arulalant/UV-CDAT-IPython-Notebooks/blob/outputs/1.Introduction_to_NumPy_Arrays.ipynb>`_
	* UV-CDAT-`cdms <http://nbviewer.ipython.org/github/arulalant/UV-CDAT-IPython-Notebooks/blob/outputs/2.UV-CDAT-cdms.ipynb>`_
	* UV-CDAT-`cdutil_gentuil <http://nbviewer.ipython.org/github/arulalant/UV-CDAT-IPython-Notebooks/blob/outputs/3.UV-CDAT-cdutil_gentuil.ipynb>`_
	* UV-CDAT-`Graphics-vcs-xmgrace <http://nbviewer.ipython.org/github/arulalant/UV-CDAT-IPython-Notebooks/blob/outputs/4.UV-CDAT-Graphics-vcs-xmgrace.ipynb>`_ 

UV-CDAT IPython Notebooks Source
 https://github.com/arulalant/UV-CDAT-IPython-Notebooks

Support
===========
Mailing List 
-----------

http://uv-cdat.org/mailing-list.html  and  https://uvcdat.llnl.gov/mailing-list/

Gallery 
=========

The UV-CDAT gallery images contains all different type of plots, projection, 2D & 
3D visualization can be found from this link  http://uvcdat.llnl.gov/gallery.php

License 
========

UVCDAT comes under Free Open Source GNU GENERAL PUBLIC LICENSE V3+     
Read about GPL License here https://www.gnu.org/licenses/gpl.html
   


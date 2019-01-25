#Installation

There is one ways to install GRADitude for the moment.  Please check the section below. 
GRADitude can only work when the requirements are installed properly. 
If you install GRADitude through source code, please install the pre-required libraries by yourself.


##Github
All the source code of GRADitude can be retrieve 
from our Git repository. Using the following commands can clone the source code easily.

<code>$ git clone https://github.com/foerstner-lab/GRADitude.git</code>

or

<code>$ git clone git@github.com:foerstner-lab/GRADitude.git</code>

In order to make GRADitude runnable, we have to  create a soft 
link of graditudelib in bin.

<code>$ $ cd GRADitude/bin</code>

<code>$ ln -s ../graditudelib .</code>


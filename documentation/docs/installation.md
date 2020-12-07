#Installation

There is three ways to install GRADitude.  Please check the section below. 
GRADitude can only work when the requirements are installed properly. 
If you install GRADitude through source code or <code>pip3</code>, please install the pre-required libraries by yourself.


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

##Docker

For using Docker image, please use one of the following commands:

1) You can pull the Docker image as following
$ docker pull silviadg87/graditude
2) Alternatively, you can build the image via Dockerfile. 
Please Download the Dockerfile from our Git repository. 
Then switch to the folder which Dockerfile are located. 
For the following commands, please refer to [here](https://docs.docker.com/get-started/part2/).


##pip3

GRADitude is also hosted in PyPI server and for this reason it can be installed via pip3.

<code>$ pip install GRADitude




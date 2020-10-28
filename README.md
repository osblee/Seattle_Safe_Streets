# Seattle Safe Streets
Welcome to the README file of Seattle Safe Streets. This program envisions to provide users with ideas on how to live on the streets of Seattle safely by giving interactive graphics such as a map that contains all incidents in Seattle or one that provides incidents that happened nearby a given street. This program also creates two interactive graphs that display different trends of types and their count categoriazed by month. Additionally, this program can predict the incident type of a dial given the month and street inputted. This program also statistically analyzes the data and provides a confidence interval on the proportion of cases that happen in the Spring vs Fall in order to solidify our visual and predictive results. This file explains step by step on how to successfully run this program and to start improving your welbeing.

## Authors

Yukito Shida

Osbert Lee

Yui Suzuki

## Getting started
This program employs a multitude of external libraries and thus, requires installation of said libraries to run properly.

### Prerequisite
*Our development environment was solely on Windows operating systems. We cannot guarantee the program works with
macOS as intended.*

Our program requires a functioning python IDE and python itself. Interactive code environments such as a Jupyter notebook also works as well. Our installation process also requires pip. Although most users already have it, below is a link to the pip documentation on how to install and upgrade pip.

https://pip.pypa.io/en/stable/installing/

Required Libraries: 

Numpy

Pandas

Sodapy

Bokeh

Plotly

Sklearn

Scipy 

### Installation Process  

Pip is a powerful library that allows us to install external libraries with simple commands in the terminal. To install each of the libraries necessary, use the commands below.

Numpy:

pip install numpy

Pandas:

pip install pandas

Sodapy:

pip install sodapy

Bokeh:

pip install bokeh

Plotly:

pip install plotly

Sklearn:

pip install sklearn

Scipy:

pip install scipy

*On rare occasions previous owned versions of external libraries can cause an error as they're not compatible with current versions of other libraries as well as the Python version you are currently working on. In this case, we recommend using the command below.*

pip install --upgrade --force-reinstall <"Library Name Goes Here">  

*Most of our libraries require numpy to operate, so having the most current numpy version is crucial for Seattle Safe Streets to run properly.*

  

## Running the program  

Please run our main.py to start Seattle Safe Streets' terminal up using the command:

python main.py

Our program requires specific street names to operate. Please try example street names like:
"4120 Stone Way N"
"100 Ward St"
"Westlake Av N / John St"

*All inputs for our program are case sensitive and should be typed with care.*  



## Acknowledgements

We want to thank StackOverFlow and the webpage of the documentations of the libraries. Without these great resources, we couldn't have possible completed this project successfully.

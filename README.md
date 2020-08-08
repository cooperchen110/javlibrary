## Basic Usage
Get actor and video infomation from [Javlibrary](http://www.javlibrary.com/). All the data is stored in MongoDB and the proccessed data is shown in json and csv format.

## How To Use
- First, you need to clone this repository to your local machine
```bash
git clone https://github.com/chenbingyuan110/javlibrary.git
```
- Second, you need to install the requirement modules. virtualenv is recommanded, for this project is build based on virtualenv.
> ##### How to install virtualenv and work with virtual environment
> ```bash
> # install virtualenv module with pip
> pip install virtualenv
> ```
```bash
# go to the repo folder
cd javlibrary

# activate the virtual environment
source ./bin/activate

# install required modules with pip
pip install -r requirement.txt
```
> If you want to exit the virtual environment, run the following command
> ```
> deactivate
> ```

- Third, rename the `proxies_sample.txt` file to `proxies.txt` and add proxies to the file with following format
```
http://host1:port
http://username:password@host2:port
http://host3:port
```
- Fourth, open your mongoDB server and run the crawler named `actor`
```
# go to the scrapy folder
cd scr/myscrapy/myscrapy

# run the actor crawler
scrapy crawl actor
```
> If you don't want to store your data with mongoDB, you can modify the piplines.py file
- Last, do your other business and leave the crawler running until finished



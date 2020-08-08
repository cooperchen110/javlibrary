## Basic Usage
Get actors and videos data from [Javlibrary](http://www.javlibrary.com/). The data is stored in MongoDB and the proccessed data is shown in json and csv format.

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
>
> # go to the repo folder
> cd javlibrary
>
> # activate the virtual environment
> source ./bin/activate
>
> # do your job in the virtual environment
>
> # when finished all the work, deactivate the virtual environment
> deactivate
> ```
```bash
pip install -r requirement.txt
```
- Third, open your mongoDB server and run the crawler named `actor`
```
# go to the scrapy folder
cd scr/myscrapy/myscrapy

# run the actor crawler
scrapy crawl actor
```
> If you don't want to store your data with mongoDB, you can modify the piplines.py file



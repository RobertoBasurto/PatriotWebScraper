# PatriotWebScraper

This python script will scrape George Mason University's Patriot Web for all the classes in a major that you specify. That data will then be parsed, saved to a file, and plotted on a heatmap.

## Purpose

The main purpose I built this was to visually see which time slots my club meetings would fit best with the majors we were trying to target. For us, it was CYSE, CS, and IT, so this tool would plot all the classes of those majors and we could see the times slots that would overlap the least number of classes.

## How to use

This script uses Chromedriver which you need to install from [here](https://chromedriver.chromium.org/downloads). Then you need to change the path of the installed chrome driver in the source on line 61.

This is a CLI which pretty self-explanatory flags.

There are two positional arguments: username and password


```./patriotscrape [username] [password]```

Then the required flags are 
- `-m` which is major(s) using the abbreviated code found [here](https://catalog.gmu.edu/courses/)
- `-y` which is catalog year (must be the current year, not an archived year)
- `-s` which is semester (again, must be the current semester)

The only optional flag is the output flag `-o` which will output to `classdata.txt` when absent

```./patriotscrape [username] [password] -m CYSE CS IT -y 2020 -s spring```

This will then use Selenium to automate the login process, clicking through the options to get to the class search, clicking through every class, switching majors and repeating until it has all the classes in one text file.
Using that text file it will parse and output the heat map in different color schemes, because some are better on the eyes 

## TODO

1. Currently the graph is broken down into 15-minute intervals, but some classes start/end at X:05 or X:10 which creates overlap (due to rounding) and gets difficult to see when there is more than one major select. **Solution:** Change the graph scale to use 5-minute intervals

2. The CLI uses too many required flags. **Solution:** Cut out `-y` and `-s` by automating the selection of the catalog year and semester to the most current ones. With those two gone, add a required flag to take in the path of the chromedriver

3. **Hope that GMU does not change the class selection and completely breaks this tool**


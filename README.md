# puregym-scraper

Simple script for scraping Puregym occupancy data.

## Usage

1. Clone this repository

```git clone https://github.com/jakub-sekula/puregym-scraper && cd puregym-scraper```

2. Activate virtual environment

```python -m venv venv & source venv/bin/activate```

3. Install dependencies

```pip install -r requirements.txt```

4. Run script and enter your credentials as arguments on the command line

```python scraper.py username password```

## Output

The script outputs the current number of people in the default gym for your account and the time it took to perform the data retrieval.

The format of the output is as follows: 

```
$ python scraper.py <username> <password>
113
Finished in  21.584192991256714 s
```

## Caveats

This script uses `requests` and `beautifulsoup4` to recrete the login flow to the members' area of the Puregym website. For some reason, the Puregym servers are really really slow, so the login process takes around 20 seconds.

A better way to do this would be to call the Puregym API directly, like in [puregym-attendance](https://github.com/2t6h/puregym-attendance) created by 2t6h. However, I wanted to figure out a way to do this without having any knowledge of the backend setup and API endpoints. 

In any case, the outputs of both scripts are the same, but the API method is much faster, taking around 6-7 seconds on average.

## Bonus

I've also included a shell script that I used to set up an automation and save the outputs of the scraper to a csv file for analysing later. You can use this with cron to run the script at regular intervals. I have been using it to log data every minute and it works great.

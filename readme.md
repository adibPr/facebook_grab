## facebook_fetch
Grab facebook post using selenium. It use facebook normal login page and its style.
If somewhat the style is different, and the program failed to login, kindly restart the process.
Facebook has several login front page style.

## Requirements
- Python 3
- Selenium and firefox driver
- Facebook account

## Usage
1. create `account.ini` file with content : 
`
[account]
username=email
password=mypassword
`

2. You can test run by issuing command  `python3 main.py` or you can import it 
in another file. 
`FG = FacebookGrab (some_arguments)
FG.process (keyword)
`
The keyword just one, so you need iteration to grab a list of keyword

3. Some argument : 
`min_char`, minimum character to save (default  1000),
`max_post`, maximum total post to grab,
`save_file`, csv path

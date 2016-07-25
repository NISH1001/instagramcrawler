# instagramcrawler
A crawler for instagram.

A project for crawling [Instagram](https://wwww.instagram.com). The crawler logs in to the user account and fetches all the general information of 
**followers** // **following** like:
- Full Name
- Username
- Biography text
- Followers count
- Following count

The dump data is like:  

```json
{
    "full_name"     : "Full Name",
    "username"      : "username",
    "followers"     : [ user1_data, user2_data, ...],
    "following"     : [ user1_data, user2_data, ...]
}
```

Since **Instagram** is fully dynamic and its api is sandboxed(limited), [Selenium](http://selenium-python.readthedocs.io/index.html) is used to automate
the login, click on the followers/following link and extract all the usernames.

Finally, [Scrapy](http://doc.scrapy.org/en/latest/index.html) is used to crawl all the relevant data for the usernames collected.

--------------------------------

## Dependencies
It uses python3 along with scrapy and selenium

```bash
pip install scrapy
```

```bash
pip install selenium
```

## Usage
Run scrapy spider as:

```bash
scrapy crawl instaspider
```


Also, the crawler `instaspider.py` requires a path to json file. The **JSON** format is:

```json
{
    "USERNAME"  :   "your_user_name",
    "PASSWORD"  :   "your password"
}
```





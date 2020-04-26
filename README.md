# COVID-19-Country-Stats
Python program that web crawls Covid-19 statistics for a desired country and sends the information to email recipients through Gmail.
I have modified the script provided by Google in the official documentation [here](https://developers.google.com/gmail/api/quickstart/python) to work with Python 3. Other than that follow the instructions provided in the documentation for setting OAuth authentication.
[This](https://www.worldometers.info/coronavirus/#countries) is the website from which the crawler extracts the information.

## General setup
You need to specify the name of the desired country through the **COUNTRY** constant in *SendMail.py*. Also, you need to populate the **emails** list with the e-mail addresses of the recipients in *SendMail.py*. E-mail addresses should be provided as strings.

## Running the program
After completing the **General setup**, you can run the program by typing: *python3 SendMail.py* in the terminal.

## Sending statistics about multiple countries
If you want to send statistics about more than one country just call the **scrape** function with another country provided as argument and then concatenate the results from the multiple invokations of **scrape**. Then simply provide the concatenated message as argument to the **send_emails** function.

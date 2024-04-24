# Mac-Battery
a little widget for me to log my mac battery over time and use discord to alert me when it's low and needs to charge.

I created this because sometimes I thought my mac battery was sufficiently charged when in fact it was not. This way if my mac is low and I'm home it'll alert me through discord


## Diagram
![simple diagram](https://github.com/ibrahimmudassar/Mac-Battery/assets/22484328/45c26311-937c-458f-b85c-4ea0582e1f08)


## DIY
1. download the python file
2. configure a cron job for time interval (mine is every 5 minutes)
3. set the environment variables
  Note: I use google sheets for mine (I was experimenting with an alternative db) so feel free to use a sql db
4. done!

### Question?
Need help on how to set up a cron job, integrating an alternative data platform, or configuring environment variables? Create an issue!

### Misc.
using a db is not necessary, I just wanted to see my battery and location data over time to see where my mac has been and my usage details.

## Contributions
This project isn't a high priority on my list, but I'm willing to accept pull requests on new ideas and stuff that can be changed.

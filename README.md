# vaccineSlotNotifier


This can find the slot availablity for Vaccination across nation which is need great effort and notify you through Twitter! Instead of visiting coWin we can directly check through this script or else through muxtrap.pythonanywhere.com where i have added this field, it takes data from there

This also notifies you through Email and Twitter regarding the slots available: https://twitter.com/vax_track and it is chduled on Google Cloud for CRON job


Vaccine Slots ALert Diagram

![vaccNot](https://user-images.githubusercontent.com/27301175/119247021-05b96980-bba4-11eb-905d-aa5535ff8519.png)


## Google Cloud Platform - Compute Engine Set up


![Screenshot 2021-06-05 at 12 20 52 PM](https://user-images.githubusercontent.com/27301175/120883084-d3265c80-c5f8-11eb-8ae2-19e2baf3a3f5.png)

I have set up this as cron job to schedule this at every 3 hours of interval in GCP South east Asian region VM servers as the trick was, the API was region restricted so to pull the data from API, we need to have Indian server to do so.

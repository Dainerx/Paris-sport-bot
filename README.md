# Paris-sport-bot
A collection of automoated software that book for you sporting activities in Paris.

Innovated by Oussama Ben Ghorbel and Ali Hady at Murex Paris.

`python --version >= 3.6.8`


## Paris Tennis

For the tennis fans in Paris, this bot is capable of booking a session tennis.paris.fr. The bot supports two modes: Pay and Hold. 

### Hold

By default, the bot will hold your reservation for 15 minutes without paying. It will send you a system notification for you to manually login and pay for the held reservation.

`python paris-tennis.py -d 4 -ho 14h -n Puteaux`

![image](https://user-images.githubusercontent.com/19507493/203551259-17fb4365-25e4-4d4b-9a7e-f61fbefe30db.png)


### Pay

You can pay directly for your reservation, however **you have to buy "Carnet de réservation"** first.

`python paris-tennis.py -d 4 -ho 14h -n Puteaux -m pay`

![image](https://user-images.githubusercontent.com/19507493/203551803-648b3842-111d-49e8-958e-75dec507001b.png)


### Command arguments

| Argument  | Short Argument | Possible values | Description |
| ------------- | ------------- | ------------- | ------------- |
| --Mode  | -m  | ["hold", "pay"]  | Bot mode  |
| --Day  | -d  | [0,7]  | Book d days from today  |
| --Hour  | -ho  | [8h,20h]  | Booking hour  |
| --Name  | -n  | Paris court names (only Paris no IDF)  | The court name in Paris  |

## Urban Soccer 

Coming soon

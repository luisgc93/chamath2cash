# Chamath2Cash bot 🤖 
A stock trading [twitter bot](https://twitter.com/Chamath2Cash) powered by tweets from billionaire investor Chamath Palihapitiya. 

<img width="480" alt="bot_mention" src="https://user-images.githubusercontent.com/32971373/107145202-6055ef00-6940-11eb-8600-4acac64b517f.png">

The bot currently runs a job every 2 minutes to parse any new tweets from @chamath. If those tweets contain a cash tag, it parses the stock tickers and places an order using an [Alpaca](https://alpaca.markets/) paper trading account and also publishes its current portfolio value.

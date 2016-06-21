- implement mock api endpoints
- implement backend process:
    - if ace, discard both `cardval` from players hands and move ace to other player's hand
    - check each player's chosen `cardval` and discard the lowest from that player hand
    - internal call to discard() which removes any `cardval` (i.e. 2d and 2s) from hand 
    - if either hand is empty, game is over
    - each player draws a card from shuffled deck
    - return cards played and results
    
- test using [apiary client](https://jsapi.apiary.io/previews/aceofblades/reference)
 
- (later) implement using [slack buttons](https://slackhq.com/get-more-done-with-message-buttons-5fa5b283a59)

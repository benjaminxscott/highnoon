- implement api endpoints
- document:
  - /ace?cardval
    - checks if you have the ace, and sets it as your next move with `cardval` guaranteed to be discarded
  - /round
    (atomic)
    - if /ace has been played , discard both `cardval` from players hands and move ace to other player's hand
    - check each player's chosen `cardval` and discard the lowest from that player hand
    - internal call to discard() which removes any `cardval` (i.e. 2d and 2s) from hand 
    - if either hand is empty, game is over
    - each player draws a card from shuffled deck
    - return cards played and results
  - /last
    - show the cards played in the last round for each player
    
- test using `curl`
 
- (stretch)  with slack, display the ace of spades emoji and stacked list of hand

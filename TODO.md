## Theme
- get people to feel the tension and swings of a real knife fight, with the danger and cross-cutting nature of pulling the knife
> need to test and find tweaks

## Design
- regular deck, no face cards, only the ace of spades - in shuffled deck
- 2 player, each starts with 5 cards
- first player to discard entire hand wins
- [mockup endpoints](https://apiblueprint.org/documentation/tutorial.html)
  
  - /play?cardval
    - adds or updates the `cardval` you're playing this round
    - if opponent has also played, resolve /round
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
    
## UI
- using `curl`, show the number of cards with `cardval` in hand (suit is irrelevant)
- with slack, display the ace of spades emoji and stacked list of hand

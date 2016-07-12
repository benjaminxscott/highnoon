## Data Model
- I implemented a basic Player object, with an optional name that is set by default to None. I wanted to allow people to set a 'display name', but not block on them setting that name if htey didn't want to. SInce the default value is None, I can easily check in frontend logic for display. I wanted to implement a profanity filter and XSS filter for the player's name, but ran into issues importing external libraries like `bleach`
- The bulk of app logic is implemented in `/play`, which stores the game state and variables related to game mechanics in the Game object. I wanted to encapsulate the ProtoRPC message as part of the Game, along with temporary values for the "environment"
- I overloaded the `won` variable to denote that the game is still in progress, as well as whether the player or the AI has won. This is a little bit 'clever' which normally is to be avoided, but I thought it was reasonable since it allows the 'if game.won is None' idiom

## App Logic
- I implemented restful endpoints following the $noun/$action scheme, and used GET for 'lookups' and POST for 'modification' endpoints
- I implemented a helper function to generate "assumed-unique" url-safe ID values, which would preferably use the `object.key` idiom instead, but I ran into strange issues trying to do lookups into the database using those keys
- The object itself is returned as JSON from most functions, with any un-used fields set to None by default. I like that the endpoints library omits the JSON attribute if the value is None, as this seems pythonic
- The game logic is relatively straightforward, a mod of rock/paper/scissors with a built-in doomsday timer and heavy Overwatch theming.
- I wanted to implement a sense of tension by including hints as to the state of the opponent, and deliberately surfacing only the information relevant to the player.
- The game is interesting to me in that it's "fun" in the way that a slot machine is fun, with a false sense of control over the outcome
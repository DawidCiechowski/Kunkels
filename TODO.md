- [x] Add queueing system
- [x] Speed up the download speed
- [x] Add support for playlist playing
- [x] Refactor codebase
- [x] Docstrings
- [ ] Decouple
- [ ] Add Spotify support
- [ ] Add support for multiple rito servers
- [ ] Expand Rito apis into multiple games
- [x] Finish Vego tracker - extension, use discord's task api for asynchronous monitoring of Vego's games, without impacting the rest of functionality
- [x] Apply to RITO for perma app key, cause ATM API key has to be refreshed.
- [ ] Improve discord.Embed formatting

# Onoining/Longterm

- Generally speaking, refactor the codebase, make it more generic, cause it's getting harder to actually make it work properly. Additionally, the amount of data is going to steadily increase over time, for the benefit if reasonable work pace, make all the utils and the code work asynchronously. Ensure you keep up with 1RP and keep the codebase clean in genral, as the bot grows. 

- Rito's spectator api is just sh*t. Find some other source for live data and keep the placeholder from Spectator api for now. 

- Seperate Riot's API bot functionality and vego_tracker funcs. Rito's API functionality must be generic, and vego tracker is supposed to use it. They are seperate entities. Vego's tracker is just parameterized to get info about vego. 

- Gotta add that error handling, RIP


# General ideas I want to think about, but will forget, if they're not written down

- Food for thought: Consider splitting the codebase into Commands/Task/Utils directories, within the src, for clarity purposes

- My guy, check how to write tests for discord bots, cause this thing needs some testing -> GitHub actions would be good direction, to see if I'm not breaking all the shit there is. 

- Probably split this into some branches -> Pass all the tests before merging. (TBH, didn't expect I'd be doing anything with that for longer period of time, hence lackluster efforts)

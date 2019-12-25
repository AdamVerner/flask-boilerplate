# Flask boilerplate

None of the available starters really suited me, so i started yet another boilerplate file.
I do not like much pre-configuration or some advance deployment, so i try to keep it to minimum.
Based mostly from what i learned thanks to [Miguel Grindberg](https://github.com/miguelgrinberg) 
and through my own work.
 

 - [x] Navigation 
 - [x] Email sending
 - [x] User registration
 - [x] User login
 - [x] Password recovery
 - [ ] Api
 - [ ] Error handling
 - [ ] Documentation
 - [ ] tests
 - [ ] robots.txt
 - [ ] .well-known
  
 

## Security
### Registration
Registration is confirmed by reCaptcha, to stop mass-spamming abuse.
JWT with email and expiration time is generated and sent to the user.


## UX stories

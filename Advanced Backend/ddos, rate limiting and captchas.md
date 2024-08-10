![[Pasted image 20240810212602.png]]
simply add the rate limiting middleware to rate limit all the endpoints

for DDOS protection simply use cloudflare 

### captchas
how captchas work
frontend makes user solve a challenge and then cloudflare will give the frontend a token that needs to be sent to the backend for each request that needs to be protected

the backend endpoint will communicate with a cloudflare api that will tell the backend server that the token is valid or not and based on that we can serve the request

![[Pasted image 20240810235259.png]]
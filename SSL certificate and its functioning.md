1. server has public and private key,
2. the public key is given to client
3. client encrypts their symmetric key (used to encrypt the data) and send the encrypted symmetric key to server
4. server decrypts the symmetric key with the private key
5. the decrypted symmetric key can be used to decrypt the data being sent by the clie
[[Drawing 2024-03-31 01.44.04.excalidraw]]
![[Pasted image 20240331015414.png]]
a hacker can still intercept the initial transfer of the public key and instead provide his own public key, that decrypts to his own private key
this issue is solved via ssl certificates

https://youtu.be/0yw-z6f7Mb4?t=834
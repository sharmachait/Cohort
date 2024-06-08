# fast setup for http
```shell
sudo apt update
sudo apt install nginx
sudo rm sudo vi /etc/nginx/nginx.conf
sudo vi /etc/nginx/nginx.conf
```
nginx configuration
```conf
events {
    # Event directives...
}

http {
	server {
	    listen 80;
	    server_name yourDomain.com;
		
	    location / {
	        proxy_pass http://localhost:8080;
	        proxy_http_version 1.1;
	        proxy_set_header Upgrade $http_upgrade;
	        proxy_set_header Connection 'upgrade';
	        proxy_set_header Host $host;
	        proxy_cache_bypass $http_upgrade;
	    }
	}
}
```
```shell
sudo nginx -s reload
node index.js
```
remember to add a DNS entry for your domain to your VM
to keep the node process running in the background
use pm2
![[Pasted image 20240608131416.png]]
[[certificate management]]
to configure NGINX with ssl certificate 
```shell
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx
```
the last command will ask us which domains we want to activate https for 
![[Pasted image 20240608130930.png]]
it will update the nginx to include the certificate
# nginx notes

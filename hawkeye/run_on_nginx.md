# How to deploy Gunicorn on Nginx:

1. Open a config file:
`$ vi /etc/nginx/sites-available/run`

2. Then type the following into that file:
`
	#Configuration for Nginx
    server {
	    # Configuration for Nginx
	    listen 80;
	    #Specify domain name or IP Address
	    server_name 0.0.0.0;
	    location / { 
	        include proxy_params; 
	        proxy_pass http://$server_name:8000;
	    } 
	}
`

3. [Optional] In case you want your site to open on typing just server IP 
   (i.e. you want your site on port 80, then do this. Doing this will allow you to open your site by
   typing `http://127.0.0.1` instead of `http://127.0.0.1:8000`):

	- Make a copy of `/etc/nginx/sites-available/default` file in some place with a different name.
	- Delete `/etc/nginx/sites-available/default` .

4. Enable project conf:
`$ sudo ln -s /etc/nginx/sites-available/run /etc/nginx/sites-enabled`

5. Verify the config:
`$ sudo nginx -t`
`$ sudo systemctl restart nginx`

6. Start gunicorn on another terminal:
	[Production] 	`gunicorn --bind 0.0.0.0:8000 run:app --workers=4`
	[Development] 	`gunicorn --bind 0.0.0.0:8000 run:app --workers=4 --reload --`

7. [Optional] Disable Ubuntu Firewall in case you want to view via mobile:
`$ sudo ufw disable`

8. In case you don't want to disable UFW fully, you can add a rule just to exclude your IP:
`$ sudo ufw allow from <IP>`

9. Enable firewall by doing:
`$ sudo ufw enable`

10. In case you want to restore default activity of port 80 then add back `/etc/nginx/sites-available/default` 
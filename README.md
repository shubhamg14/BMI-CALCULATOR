# BMI-CALCULATOR

A BMI calculator which takes your Height(cms) and Weight(kgs) as input and outputs whether you are Underweight, Overweight or Healthy, implemented using Flask, HTML, CSS on wsgi hosted behind Apache2 on an EC2 instance.

The Height and Weight input can only be integer and not string. 

This website is hosted on both Port 80 (http) and Port 443 (https)
	
	HTTP(Port 80): wsgi server hosted behind Apache2
	HTTPS(Port 443): Self signed SSL certificate added to the present configuration of wsgi server hosted behind Apache2

# Getting Started

These instructions will get you a copy of the project up and running on your AWS instance. 

# Prerequisites

	AWS account
	Wsgi
	Apache2
	Flask==1.0.2 
	Python==3.6.8

# Installing

A step by step series of examples that tell you how to get a development environment running

1.	Starting up an EC2 instance

	Create a free tier account on AWS (AMI-Ubuntu 18.04 with 10GB space)
	Launch and connect to EC2 instance

2.	Setting up the instance on EC2
	
	Install apache webserver and mod_wsgi

		$ sudo apt-get update
		$ sudo apt-get install apache2
		$ sudo apt-get install libapache2-mod-wsgi

	Install flask using pip

		$ sudo apt-get install python-pip
		$ sudo pip install flask

	Create a directory for our flask app
	
		$ mkdir ~/flaskapp
		$ sudo ln -sT ~/flaskapp /var/www/html/flaskapp

3.	Running flask app
	
		Create a flask application flaskapp.py
		Create a flaskapp.wsgi file to load the application
		Put the following content in a file named flaskapp.wsgi:
	
			import sys
			sys.path.insert(0, '/var/www/html/flaskapp')
			from flaskapp import app as application

	Enable mod_wsgi

	In the apache configuration file located at /etc/apache2/sites-enabled/000-default.conf, add the following block just after the         DocumentRoot /var/www/html line:

		WSGIDaemonProcess flaskapp threads=5
		WSGIScriptAlias / /var/www/html/flaskapp/flaskapp.wsgi

		<Directory flaskapp>
			WSGIProcessGroup flaskapp
			WSGIApplicationGroup %{GLOBAL}
			Order deny,allow
			Allow from all
		</Directory>

	Restart the Apache webserver

		$ sudo apachectl restart

4.	Test the configuration

	Navigate your browser to your EC2 instance's public DNS again and we should the output from our application 

5.	Any errors our stored in 

		/var/log/apache2/error.log
		
6.	HTTPS implementation
	Create the SSL certificate
		
		sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out 				/etc/ssl/certs/apache-selfsigned.crt
	
	Create Diffie-Hellman group
		
		sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
	
	Configure Apache to use SSL
	
	Create an Apache configuration snippet with strong encryption settings
	In the ssl-params.conf, set the SSLOpenSSLConfCmd DHParameters directive to point to the Diffie-Hellman file we generated 		earlier.
		
		sudo nano /etc/apache2/conf-available/ssl-params.conf
		
		SSLOpenSSLConfCmd DHParameters "/etc/ssl/certs/dhparam.pem"
	
	Modify default Apache SSL virtual host file and add the following
		
		sudo nano /etc/apache2/sites-available/default-ssl.conf
		
		ServerAdmin webmaster@localhost
                DocumentRoot /var/www/html
                WSGIScriptAlias / /var/www/html/flaskapp/flaskapp.wsgi
                <Directory flaskapp>
                 WSGIProcessGroup flaskapp
                 WSGIApplicationGroup %{GLOBAL}
                Order deny,allow
                Allow from all
                </Directory>

		SSLCertificateFile      /etc/ssl/certs/apache-selfsigned.crt
                SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
	
		BrowserMatch "MSIE [2-6]" \
                               nokeepalive ssl-unclean-shutdown \
                               downgrade-1.0 force-response-1.0
			       
	Enable the changes in Apache and restart the Apache server
		
		sudo a2enmod ssl	//enable apache SSL module
		sudo a2enmod headers
		sudo a2ensite default-ssl //enable SSL virtual host
		sudo a2enconf ssl-params	//enable conf file
		sudo apache2ctl configtest	//check for any syntax errors
		sudo systemctl restart apache2	//restart apache server
		
	Test, by opening websie with https appended to pubic dns name in the web browser.
	
# Deployment

Copy your code into linux instance on AWS from your local machine using Winscp and keep all code under folder
	
		/home/ubuntu/flaskapp/flaskapp.py (FLASK CODE)
		/home/ubuntu/flaskapp/templates/bmi_calc.html (HTML CODE)
	
Your python file containg Main method should be named flaskapp.py which is similar to the wsgi file names flaskapp.wsgi
	
# Versioning

	We use git to maintain our different code versions
	https://github.uc.edu/gupta2su/BMI-CALCULATOR/ 

# Acknowledgments
  	* HTML - https://www.w3schools.com/

	* WSGI with Apache - https://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/
	
	* SSL - https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-16-04




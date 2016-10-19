#The Following details Explain Each Request used on Tspammer.py Script
_________________________________________________________________________________________________________
###This  Request is used to get token and cookies for login 

 - URL 		       :twitter.com/

 - Method		   : GET

 - Authentication  : not required

 - Reason   	   : Getting guest cookies

 - Message         :

 ~~~~~~~~
	GET / HTTP/1.1
	Host: twitter.comUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	Accept: text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8
	Accept-Language: en-US,en;q=0.5
	Upgrade-Insecure-Requests: 1
 ~~~~~~~~
_________________________________________________________________________________________________________
### This request is used to report a user

 - URL            : twitter.com/i/safety/report_story 

 - Method         : POST

 - Authentication : Required (valid session)

 - Reason         : Submitting report to twitter

 - Message	    : 

 ~~~~~~~~
 	POST twitter.com/i/safety/report_story HTTP/1.1
 	Host: twitter.com
	User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
	Accept-Language: en-US,en;q=0.5
	Referer: https://twitter.com/i/safety/report_story?next_view=multi_tweet_select&victim=Someone_else
	Cookie: ___Cookies_Contains__Report__Details
	Content-Type: application/x-www-form-urlencoded
	
	authenticity_token=___Auth__Token___&next_view=harassment_confirmation_v2

 ~~~~~~~~
_________________________________________________________________________________________________________

### This request is used to Log in

 - URL            :https://twitter.com/sessions

 - Method         : POST

 - Authentication : Required (Valid credentials [id and passowrd ]) + (guest cookie)

 - Reason	     : Init a new session

 - Message        :
 ~~~~~~~~
	Host: twitter.com
	User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	Accept: text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8
	Accept-Language: en-US,en;q=0.5

	Referer: https://twitter.com/,Upgrade-Insecure-Requests: 1
	Cookie: ___Guest__coookies__
	Content-Type: Application/x-www-form-urlencoded
 ~~~~~~~~
_________________________________________________________________________________________________________
### This request is used to get an id of installed mobile phone (not used)
 
 - Url 	: twitter.com/settings/devices

 - Method : Get
 
 - Authentication: Required (valid session)

 -Message
 ~~~~~~~~
     GET /settings/devices HTTP/1.1
	 Host: twitter.com
	 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	 Accept: Application/json, text/javascript, */*; q=0.01
	 Accept-Language: en-US,en;q=0.5
	 Referer: https://twitter.com/settings/account
	 X-Push-State-Request: true
	 X-Asset-Version: 6c60a3
	 X-Requested-With: XMLHttpRequest
	 Cookie: ___Cookies___
	 Connection: close
 ~~~~~~~~
_________________________________________________________________________________________________________
### This request is used to delete mobile phone from account using (device ID)
 
 - Url: twitter.com/settings/devices/destroy

 - Method: POST

 - Reasong: Delete mobile phone

 - Authentication : Required (valid Login)

 - Message :

 ~~~~~~~~
     POST /settings/devices/destroy HTTP/1.1
	 Host: twitter.com
	 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	 Accept: Application/json, text/javascript, */*; q=0.01
	 Accept-Language: en-US,en;q=0.5
	 Referer: https://twitter.com/settings/account
	 Upgrade-Insecure-Requests: 1
	 Cookie: ____Cookies___
	 Connection: close
	 Content-Type: Application/x-www-form-urlencoded
	 Content-Length: 103

	 authenticity_token=__Auth_Token___&_method=delete&device_id=784045180760363008
 ~~~~~~~~


URL
Method
Authentication
Reason
Message
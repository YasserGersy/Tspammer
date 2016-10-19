#The Following details Explain Each Request used on Tspammer.py Script


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


### This request is used to report a user

 POST twitter.com/i/safety/report_story 

 Authentication: Required

 For 		   : Submitting report to twitter

 Example	   : 

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

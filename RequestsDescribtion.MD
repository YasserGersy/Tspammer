## The Following details Explain Each Request used on Tspammer.py Script

_________________________________________________________________________________________________________


```
+ this will be highlighted in green
- this will be highlighted in red
```


### This  Request is used to get token and cookies for login 

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



### **This request is used to report a user**

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


### This request is used to get an id of installed device "mobile phone" (not used)
 
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


### This request is used to delete mobile phone from account using device ID (not used)
 
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
_________________________________________________________________________________________________________


### This request is used to retweet or like a tweet

 - URL : twitter.com/i/tweet/like or twitter.com/i/tweet/retweet

 - Method: POST

 - Authentication : Required (valid session)

 - Reason : Like or retweet 

 - Message :

  ~~~~~~~~
	POST /i/tweet/like HTTP/1.1  	or   POST /i/tweet/retweet HTTP/1.1
	 Host: twitter.com
	 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	 Accept: application/json, text/javascript, */*; q=0.01
	 Accept-Language: en-US,en;q=0.5
	 Content-Length: 147
	 Content-Type: application/x-www-form-urlencoded; charset=UTF-8
	 Referer: https://twitter.com/
	 X-Requested-With: XMLHttpRequest
	 Cookie: ___Cookies___
	 Connection: close

	
	authenticity_token=___AUTH___TOK__&id=___Tweet__ID___&tweet_stat_count=0
	

  ~~~~~~~~
_________________________________________________________________________________________________________


### This request is used to post a tweet

 - url : twitter.com/i/tweet/create
 - Method : POST
 - Authentication: Required (Valid session)
 - Reason : Mass tweet
 - Message :
 ~~~~~~~~
     POST /i/tweet/create HTTP/1.1
	 Host: twitter.com
	 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	 Accept: Application/json, text/javascript, */*; q=0.01
	 Accept-Language: en-US,en;q=0.5
	 Content-Length: 129
	 Content-Type: Application/x-www-form-urlencoded; charset=UTF-8
	 Referer: https://twitter.com/
	 X-Requested-With: XMLHttpRequest
	 Cookie: ____Cookies____

	 authenticity_token=__AUTH__Token__&is_permalink_page=false&place_id=&status=___TWEET__Text__&tagged_users=
	
 ~~~~~~~~
_________________________________________________________________________________________________________


### This request is used to follow a user

 - URL : twitter.com/i/user/follow 

 - Method : POST

 - Authentication : Required (valid session)

 - Reason: Mass Follow or spam 

 - Message: 
 ~~~~~~~~
     POST /i/user/follow HTTP/1.1
	 Host: twitter.com
	 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	 Accept: Application/json, text/javascript, */*; q=0.01
	 Accept-Language: en-US,en;q=0.5
	 Content-Length: 137
	 Content-Type: Application/x-www-form-urlencoded; charset=UTF-8
	 Referer: https://twitter.com/ptionacc
	 X-Requested-With: XMLHttpRequest
	 Cookie: ____COOOKIES___
	Connection: close

	# authenticity_token=3faceb6a373f90a19aa98a423e11c7bed8e9a51d&challenges_passed=false&handles_challenges=1&impression_id=&user_id=__User__ID__
  ~~~~~~~~
_________________________________________________________________________________________________________


### This Request is used to GET id of a user

 - URL : twitter.com/_user_name_

 - Method: POST

 - Authentication:  not required

 - Reason : GEt user id for furher usage

 - Message :
  ~~~~~~~~
     GET /johncena HTTP/1.1
	 Host: twitter.com
	 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	 Accept: text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8
	 Accept-Language: en-US,en;q=0.5
	 Connection: close	
  ~~~~~~~~
_________________________________________________________________________________________________________


### This request is used to update bot profile information (NOT USED)

 - URL : twitter.com/i/profiles/update 

 - Method: POST

 - Authentication : Required (valid session)

 - Reason : Mass update bots bio

 - Message : 
  ~~~~~~~~
     POST /i/profiles/update HTTP/1.1
	 Host: twitter.com
	 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	 Accept: Application/json, text/javascript, */*; q=0.01
	 Accept-Language: en-US,en;q=0.5
	 Content-Length: 242
	 Content-Type: Application/x-www-form-urlencoded; charset=UTF-8
	 Referer: https://twitter.com/ptionacc
	 X-Requested-With: XMLHttpRequest
	 Cookie: ___COOOKIES___
	 Connection: close

	# authenticity_token=3faceb6a373f90a19aa98a423e11c7bed8e9a51d&page_context=me&section_context=profile&user%5Bdescription%5D=___BIO___Describtion___&user%5Burl%5D=___SITE___URL__
	
  ~~~~~~~~
_________________________________________________________________________________________________________


### This request is used to check if session still valid or expired

 - URL : twitter.com/
 - Method :  GET
 - Authentication : Required for valid session
 - Reason : determine if session is expired or still valid
 - Message :
  ~~~~~~~~
  	 GET / HTTP/1.1
	 Host: twitter.com
	 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	 Accept: text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8
	 Accept-Language: en-US,en;q=0.5
	 Referer: https://twitter.com/login
	 Cookie: ___COOKIES____
	 Connection: close
	 Upgrade-Insecure-Requests: 1
  ~~~~~~~~
_________________________________________________________________________________________________________


### This request is used to update bot name (not used)

 - URL :
 - Method: 
 - Authentication : 
 - Reason :
 - Message :
   ~~~~~~~~
     POST /i/profiles/update HTTP/1.1
	 Host: twitter.com
	 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	 Accept: Application/json, text/javascript, */*; q=0.01
	 Accept-Language: en-US,en;q=0.5
	 Content-Length: 242
	 Content-Type: Application/x-www-form-urlencoded; charset=UTF-8
	 Referer: https://twitter.com/ptionacc
	 X-Requested-With: XMLHttpRequest
	 Cookie: _____COOOKIES_____
	 Connection: close

	authenticity_token=__AUTH__TOKEN___&page_context=me&section_context=profile&user%5Bdescription%5D=___PRofile__Describtion___&user%5Burl%5D=___bot__URL___
	
   ~~~~~~~~
_________________________________________________________________________________________________________


### This request is used to get some tweet ids from certain user profile

 - URL : twitter.com/i/profiles/show/__USER__NAME_/timeline/tweets?include_available_features=1&include_entities=1&max_position=___LAST__Loaded_tweet__id__&reset_error_state=false 

 - Method: POST 

 - Authentication: Required (valid session )

 - Reason : For spam ( random likes or retweets)

 - Message :
   ~~~~~~~~
    GET /i/profiles/show/yassergersy/timeline/tweets?include_available_features=1&include_entities=1&max_position=723202757822304256&reset_error_state=false HTTP/1.1
	 Host: twitter.com
	 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	 Accept: application/json, text/javascript, */*; q=0.01
	 Accept-Language: en-US,en;q=0.5
	 X-Requested-With: XMLHttpRequest
	 Referer: https://twitter.com/yassergersy
	 Cookie: ____COOKIES____
	 Connection: close
   ~~~~~~~~
_________________________________________________________________________________________________________


### This request is used to get the last tweets by a user

 - URL : https://twitter.com/__USERNAME__
 - MEthod: GET
 - Authentication : not required
 - Reason: GET last tweets by a user
 - Message: 
   ~~~~~~~~
    Host: twitter.com
	User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
    Accept: text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5	
   ~~~~~~~~

_________________________________________________________________________________________________________




_________________________________________________________________________________________________________




_________________________________________________________________________________________________________



URL
Method
Authentication
Reason
Message
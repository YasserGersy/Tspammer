#!/bin/python

import requests,sys,os,time,urllib,datetime,random,string

requests.packages.urllib3.disable_warnings()
prox={'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080','ftp':'ftp://127.0.0.1:8080'}
debug=False

class STX:
	session_separator='-----------------'
	session_value_separator=' -==- '
	HEADER = '\033[95m'
	OKBlue = '\033[94m'
	OKGreen = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERlinE = '\033[4m'    	
	RED='\033[1;31m'
	brown='\033[0;33m'
	Blue='\033[0;34m'
	Green='\033[1;32m'
	magenta='\033[1;35m'
	yel = '\033[93m'
	White='\033[1;37m'
	lin="\n-----------------------------------------------------------------------"
	havlin='----------------------------'
	me='Twitter.py'
	ver='v1.2'
class App:
	action=''
	ids_file='ids.txt'
	session_file='sessions.txt'
	users_ids_file='users.txt'


class par:
	#ids_lines=[]
	Loaded_Session_list=[]
	Ids_and_passwords={}
	users_IDS={}
	Loaded_users_ids_count=0
	deserialized_sessions=[]
	valid_sessions=[]
	valid_sessions_string=''
	#valid_sessions_emails=[]
	Validators=[]

	PINGOLDSES=False
	ISSUENEWSES=False
	StoreValidSess=False
def randomstr(l):
	s=string.digits+string.lowercase+string.uppercase
	return ''.join(random.sample(s,l))
def islocked(body):
	return '{"errors":[{"code":326,"message":"To protect our users from spam and other malicious activity, this account is temporarily locked. Please log in to https://twitter.com to unlock your account.","sub_error_code":0,"bounce_location":"https://twitter.com/account/access"}]}' in body
def StoreValidator(s):

	gb=GET(s,'_twitter_sess')
	if gb=='False':
		return
	for x in par.Validators:
		t=GET(x,'_twitter_sess')
		if t=='False':
			continue
		if t==gb:
			continue
		par.Validators.append(gb)

def extract__from_Cookie(cok,name):
	try:
		v=cok.split(name)
		x=v[1].split(';')
		nb=x[0][1:]
		return nb		
	except Exception,o:
			return ""
def extract__from_body(bod,inputDeli):
	try:
		x=bod.split(inputDeli)
		v=x[1].split('"')
		return v[0]
	except Exception:
		return ""
def SerializeSession(r):
	strex=''
	eq=STX.session_value_separator
	for k in r:
	 	strex=strex+k+eq+str(r[k])+'\n'
	# strex=strex+'email'+eq+GET(r,'email')+'\n'
	# strex=strex+'password'+eq+GET(r,'password')+'\n'
	# strex=strex+'cookie'+eq+GET(r,'cookie')+'\n'
	# strex=strex+'authenticity_token'+eq+GET(r,'authenticity_token')+'\n'
	strex=strex+STX.session_separator
	return strex
def	deserializeSession(session_string):
	#raw_input(session_string)
	sess_lines=session_string.split('\n')
	sessionObject={}
	for keyvaluepair in sess_lines:
		if STX.session_value_separator not in keyvaluepair:
			continue
		if len(keyvaluepair.strip() )<2:
			continue
		if keyvaluepair.startswith('#'):
			continue
		elements=keyvaluepair.split(STX.session_value_separator)
		ele_name=elements[0].strip().lower()
		ele_val=elements[1]
		if ele_name=='password':#prevent passwords disclousre
			continue
		if ele_name=='respbody':#preven response body
			continue
		sessionObject[ele_name]=ele_val
	sessionObject['deserialized']='True'
	if GET(sessionObject,'cookie')=='False':
		sessionObject['deserialized']='False'
	if GET(sessionObject,'authenticity_token')=='False':
		sessionObject['deserialized']='False'
	return sessionObject

def prints(s):
	s=str(s)
	sys.stdout.write(s)
	sys.stdout.flush()
def ClearSuspendedSession(s):
	try:
		if GET(s,'locked')=='True':
			ind=GET(s,'sesindex')
			if ind.isdigit():
				ibc=int(ind)
				if len(par.valid_sessions)>ibc:
					del par.valid_sessions[ibc]
		return 1
	except Exception:
		return 0
def GET(lis,k):
	try:
		return lis[k]
	except Exception,i:
		#raw_input(str(i))
		return 'False'
def init():
	#cok[ _twitter_sess],cok[ guest_id],cok[_ga],cok[_gat],cok[pid],body[authenticity_token]
	res={}
	res['initrequest']=False
	url='https://twitter.com'
	hdrs={'Host': 'twitter.com','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0','Accept': 'text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5','Upgrade-Insecure-Requests': '1'}
	if debug:
		r=requests.get(url=url,headers=hdrs,allow_redirects=False,proxies=prox)
	else:
		r=requests.get(url=url,headers=hdrs,allow_redirects=False)

	if r.status_code!=200:
		return res
	try:
		cookieHeaders=r.headers['Set-Cookie']
		res['initrequest']=True

		_twitter_sess=extract__from_Cookie(cookieHeaders,'_twitter_sess')
		guest_id=extract__from_Cookie(cookieHeaders,'guest_id')
		_ga=extract__from_Cookie(cookieHeaders,'_ga')
		_gat=extract__from_Cookie(cookieHeaders,'_gat')
		pid=extract__from_Cookie(cookieHeaders,'pid')
		authenticity_token=extract__from_body(r.text,'<input type="hidden" name="authenticity_token" value="')
		#raw_input(authenticity_token)
		#_ga=GA1.2.1807619857.1475681872; _gat=1; pid="v3:1475681873798613838963613"
		
		_ga='GA1.2.1807619857.1475681872' if len(_ga)==0 else _ga
		_gat='1' if len(_gat)==0 else _gat
		pid='v3:1475681873798613838963613"' if len(pid)==0 else pid
		
		cookie='_twitter_sess='+_twitter_sess+'; guest_id='+guest_id+'; _ga='+_ga+'; _gat='+_gat+';pid='+pid
		
		if authenticity_token=='':
			authdel='" name="authenticity_token">'
			v=r.text.encode('utf-8').split(authdel)[0]
			authenticity_token=v.split('"')[-1]
			res={
		'initrequest':'True',
		'cookie':cookie.replace(' ',''),
		#'_twitter_sess':_twitter_sess,
		#'guest_id':guest_id,'_ga':_ga,'_gat':_gat,'pid':pid,
		'authenticity_token':authenticity_token.encode('utf-8'),
		'lastmsg':'got guest session',
		'initrequest':'True'
		}

	except Exception,er:
		res['lasterror']=res['sessionerror']=str(er)
		
	return res
def report(vars,uid):
	
	# POST /i/safety/report_story HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
	# Accept-Language: en-US,en;q=0.5
	# Referer: https://twitter.com/i/safety/report_story?next_view=multi_tweet_select&victim=Someone_else
	# Upgrade-Insecure-Requests: 1
	# Cookie: profile_id=4766587719; client_location="profile:profile:profile_follow_card"; source=reportprofile; reported_user_id=4766587719; report_type=abuse; abuse_type=violence; victim=Someone_else; guest_id=v1%3A147656774018470601; pid="v3:1476567750510185312822237"; _ga=GA1.2.1909173556.1476567795; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCK6MPtJXAToMY3NyZl9p%250AZCIlYTY4ZmMzZTJmMTQxOTZlYWRjYjIyNTRlMzQwNzhhOWU6B2lkIiUxYzkz%250AYjIwYTM0OTk0YzJmOTQyYzhhMWEzNjZiZjhjZToJdXNlcmwrCQDwVoTCGN8K--c8cd93c11026ce99abd5bd278bbca62dffe13280; kdt=HapxxExofvJF2RVl7WrtFdlzmlARaLZJhrevy2ni; remember_checked_on=1; twid="u=783372083908767744"; auth_token=4A4EBD6661EA475D925400B380AD017A209AA5A5; lang=en
	# Connection: close
	# Content-Type: application/x-www-form-urlencoded
	# Content-Length: 96
	ur='https://twitter.com/i/safety/report_story'
	cok=GET(vars,'cookie')+';profile_id='+uid+'; client_location="profile:profile:profile_follow_card"; source=reportprofile; reported_user_id='+uid+'; report_type=abuse; abuse_type=violence; victim=Someone_else; guest_id=v1%3A147656774018470601; pid="v3:1476567750510185312822237"; _ga=GA1.2.1909173556.1476567795;'

	h={
	'Host': 'twitter.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Referer': 'https://twitter.com/i/safety/report_story?next_view=multi_tweet_select&victim=Someone_else',
	'Cookie': cok.replace(' ',''),'Content-Type': 'application/x-www-form-urlencoded',
	}
	b='authenticity_token='+GET(vars,'authenticity_token')+'&next_view=harassment_confirmation_v2'
	if debug:
		r=requests.post(url=ur,headers=h,data=b,allow_redirects=False,proxies=prox)
	else:
		r=requests.post(url=ur,headers=h,data=b,allow_redirects=False)

	if r.status_code==302 and r.text=='':
		vars['lastmsg']='Reprted '+uid+' by '+GET(vars,'username')
		vars['reported']='True'
	else:
		vars['lastmsg']='Error reporting'

	return vars	

	
def initSession(id,ps):
	i=init()

	i['email']=id
	i['password']=ps
	i2= session(i)
	return ping(i2)

def session(vars):
	_pas_=GET(vars,'password').strip().replace('\r','').replace('\n','')
	_loginId_=GET(vars,'email').strip()
	url='https://twitter.com/sessions'
	cookie= GET(vars,'cookie')#'_twitter_sess='+GET(vars,'_twitter_sess')+'; guest_id='+GET(vars,'guest_id')
	hdrs={'Host': 'twitter.com','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0','Accept': 'text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5','Referer': 'https://twitter.com/','Upgrade-Insecure-Requests': '1','Cookie': cookie.replace(' ',''),'Content-Type': 'Application/x-www-form-urlencoded'}
	body={'session[username_or_email]':_loginId_,	'session[password]':_pas_,	'remember_me':'1','return_to_ssl':'true',	'redirect_after_login':'%2F','scribe_log':'.','authenticity_token':GET(vars,'authenticity_token')}
	if debug:
		r=requests.post(url=url,headers=hdrs,data=urllib.urlencode(body),allow_redirects=False,proxies=prox)
	else:
		r=requests.post(url=url,headers=hdrs,data=urllib.urlencode(body),allow_redirects=False)
	
		#return newsession , guestid ,kdt ,twid,auth_token
	if r.status_code==302 and '<html><body>You are being <a href="https://twitter.com/' in r.text and 'twitter.com/login/error?' not in r.text and ('error?username_or_email='  in r.text==False):
		respcok=r.headers['Set-Cookie']
		kdt=extract__from_Cookie(respcok,'kdt')
		newsess=extract__from_Cookie(respcok,'_twitter_sess')
		twid=extract__from_Cookie(respcok,'twid')
		new_auth_token=extract__from_Cookie(respcok,'auth_token')
		vars['sessionrequest']=True
		vars['_twitter_sess']=newsess
		vars['kdt']=kdt
		vars['twid']=twid
		vars['auth_token']=new_auth_token
		vars['sessionrequest']=True
		vars['lastmsg']='session initiated'
		vars['loginer']=_loginId_
	#elif '/twitter.com/login/error?username_or_email'
	else:
		vars['sessionrequest']=False
		vars['lastmsg']='Login failed for '+_loginId_
	newcok=''
	for g in r.cookies:#headers['Set-Cookie'].split(','):#+'\n--\n'
		newcok=newcok+' '+g.name+'='+g.value+';'
	vars['valid']='True'
	vars['cookie']=vars['cookie']=newcok
	vars['email']=GET(vars,'email').strip()
	vars['respbody']=r.text

	if 'href="https://twitter.com/account/login_challenge' in  r .text:
		vars['valid']='False'
		vars['lastmsg']=spaces('Login Failed for '+_loginId_,5)+' Account require activation'
		vars['error']='Acount requires activation'

	# z=''
	# for k in r.headers:
	# 	z=k+': '+r.headers[k]
	# z=z+r.text
	# sx=open('errors/'+_loginId_,'w')
	# sx.write(z)

	#vars['password']=GET(vars,'password').strip()
	
	return vars
def getdevices(vars):
	#Set authenticity_token , device_id
	#"formAuthenticityToken":"   
	#name=\"device_id\" value=\"
	#
	#optional mobile number
	#<span class="device_number_with_country_code">&lrm;+20 1111014041</span> (Egypt)

	# GET /settings/devices HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: Application/json, text/javascript, */*; q=0.01
	# Accept-Language: en-US,en;q=0.5
	# Referer: https://twitter.com/settings/account
	# X-Push-State-Request: true
	# X-Asset-Version: 6c60a3
	# X-Requested-With: XMLHttpRequest
	# Cookie: _twitter_sess=%%%--; guest_id=v1%3A147576820411476375; pid="v3:1475768207619797818698609"; 
	#		lang=en; _ga=GA1.2.215503156.1475768215; _gat=1; kdt=lcjeITrditwiKzHj2vJeUgUnP0JI5npcWG1vLYCG; remember_checked_on=1; twid="u=783372101986185216"; auth_token=288F4F139BA0A6F754A08C68ECDF3C830E0D0DEF
	# Connection: close
	u='https://twitter.com/settings/devices'
	_hcok=cookie= GET(vars,'cookie')#'_twitter_sess='+GET(vars,'_twitter_sess')+';guest_id='+GET(vars,'guest_id')+';pid='+GET(vars,'pid')+'lang=end;_ga='+GET(vars,'_ga')+';_gat=1;kdt='+GET(vars,'kdt')+';remember_checked_on=1;twid="'+GET(vars,'twid')+'";'+'auth_token='+GET(vars,'auth_token')
	_hdrs={
	'Host': 'twitter.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Accept': 'Application/json, text/javascript, */*; q=0.01',
	'Accept-Language': 'en-US,en;q=0.5',
	'Referer': 'https://twitter.com/settings/account',
	'X-Push-State-Request': 'true',
	'X-Asset-Version': '6c60a3',
	'X-Requested-With': 'XMLHttpRequest',
	'Cookie': _hcok.replace(' ','')
	}
	done=False
	prints('\n [-]Getting devices ')
	if debug:
		r=requests.get(url=u,headers=_hdrs,allow_redirects=False,proxies=prox)
	else:
		r=requests.get(url=u,headers=_hdrs,allow_redirects=False)
	decodedbody=r.text.encode('utf-8')
	#formAuthenticityToken=extract__from_body(r.text,'"formAuthenticityToken":" ')
	if islocked(decodedbody):
		vars['lastmsg']='Account locked by twitter '+GET(vars,'username')#('' if GET(vars,'username')=='False' else GET(vars,'username'))
		vars['valid']='False'
		vars['decvices']='False'
		vars['locked']='True'
		return vars
	vars['devicerequest']='True'
	if ' <a href="https://twitter.com/settings/add_phone"' in decodedbody:
		vars['lastmsg']='no devices installed'
		vars['devices']='False'
		vars['device_id']='False'
		done=True
		return vars

	else:
		deli='name=\\"device_id\\" value=\\"'
		device_id=extract__from_body(decodedbody,deli).split('\\')[0]
		device_num=extract__from_body(decodedbody,'class=\\"device_number_with_country_code\\"\\u003e&lrm;')
	

		if '\\' in device_id:
			g=device_id.split('\\')
			device_id=g[0]
		if '\\' in device_num:
			dd=device_num.split('\\')
			device_num=dd[0]
	
		if len(device_id) <1:
			error='No devices found'
			vars['devices']='False'
			vars['last msg']=' no devices found unknown error'
		else:
			vars['lastmsg']='Device id = '+device_id+('' if len(device_num)<1 else '	and num='+device_num)
			vars['device_id']=device_id
			vars['device_num']=device_num
			vars['devices']='True'	
			prints('\n GetDevice = Device found')
	done=True
	#vars['authenticity_token']=formAuthenticityToken

	return vars
def deleteDevice(vars):
	#if device deleted 
	#<html><body>You are being <a href="/settings/add_phone?from_delete=true">redirected</a>.</body></html>
	#
	#if no deletion 
	#l><body>You are being <a href="/settings/devices">redirected</a>.</body></html>

	# POST /settings/devices/destroy HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: Application/json, text/javascript, */*; q=0.01
	# Accept-Language: en-US,en;q=0.5
	# Referer: https://twitter.com/settings/account
	# Upgrade-Insecure-Requests: 1
	# Cookie: _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCQBm6RXAToMY3NyZl9p%250AZCIlYTBlNjcxZWMzZjg0OTFmM2UyN2I2ZmE5NmFhYTQzOTM6B2lkIiU4NDll%250AMTg0NjgyYmQzNzRiMWEyZTEzZDYyNDdlZDAyYjoJdXNlcmwrCQDw1sbdEt8K--b226b1f1add7aa5e694d6679758e248266f4c847;guest_id=v1%3A147593540432063877;pid=v3:1475681873798613838963613"lang=end;_ga=GA1.2.1807619857.1475681872;_gat=1;kdt=teXa1PFHcgYx9MDZhIpXssqSBDF5T9H6vTwIMkRH;remember_checked_on=1;twid=""u=783365603918802944"";auth_token=FD826C21C50F8C156FDC62E2E46ABD17F2EBC9BA
	# Connection: close
	# Content-Type: Application/x-www-form-urlencoded
	# Content-Length: 103

	# authenticity_token=44a741c28912cedf6e615b38a3cef30fe185b09f&_method=delete&device_id=784045180760363008
	u='https://twitter.com/settings/devices/destroy'
	_hcok=cookie= GET(vars,'cookie')#'_twitter_sess='+GET(vars,'_twitter_sess')+';guest_id='+GET(vars,'guest_id')+';pid='+GET(vars,'pid')+'lang=end;_ga='+GET(vars,'_ga')+';_gat=1;kdt='+GET(vars,'kdt')+';remember_checked_on=1;twid="'+GET(vars,'twid')+'";'+'auth_token='+GET(vars,'auth_token')
	_hdrs={
	'Host': 'twitter.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Accept': 'Application/json, text/javascript, */*; q=0.01',
	'Accept-Language': 'en-US,en;q=0.5',
	'Referer': 'https://twitter.com/settings/account',
	'Upgrade-Insecure-Requests': '1',
	'Cookie': _hcok.replace(' ',''), 
	'Content-Type': 'Application/x-www-form-urlencoded',
	}
	done=False
	devid=GET(vars,'device_id')
	if devid == 'False':
		vars=getdevices(vars)
		devid=GET(vars,'device_id')
		if GET(vars,'devicerequest')=='True' and GET(vars,'devices')=='False':
			return vars

	_dat='authenticity_token='+GET(vars,'authenticity_token')+'&_method=delete&device_id='+devid

	if debug:
		r=requests.post(url=u,data=_dat,headers=_hdrs,allow_redirects=False,proxies=prox)
	else:
		r=requests.post(url=u,data=_dat,headers=_hdrs,allow_redirects=False)
	
	if islocked(r.text):
		vars['lastmsg']='Account locked by twitter'
		vars['valid']='False'
		return vars
	if 'l><body>You are being <a href="/settings/devices">redirected</a>.</body></html>' in r.text:
		vars['lastmsg']='no devices deleted'
	elif 'You are being <a href="/settings/add_phone?from_delete=true">redirected</a>.</body><' in r.text:
		vars['lastmsg']='Device ['+GET(vars,'device_id')+']  deleted'
def LikeATweet(vars,twid):
	return HangeATweet(vars,twid,'like')
def PostReTweet(vars,twid):
	return HangeATweet(vars,twid,'retweet')
def HangeATweet(vars,twid,ac):
	#success {"profile_stats":[{"stat":"favorite","user_id":
	#duplicate {"message":"Your account may not be allowed to perform this action. Please
	#not exits {"errors":[{"message":"Sorry, that page does not exist","code":34}]}
	#POST /i/tweet/like HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: application/json, text/javascript, */*; q=0.01
	# Accept-Language: en-US,en;q=0.5
	# Content-Length: 147
	# Content-Type: application/x-www-form-urlencoded; charset=UTF-8
	# Referer: https://twitter.com/
	# X-Requested-With: XMLHttpRequest
	# Cookie: _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCEF9A6pXAToMY3NyZl9p%250AZCIlZWZmMmVhNjEwZDNkZWRjNzMzYTJjZTk3Y2U0MWJjMDQ6B2lkIiU3NmRj%250AYTNhYzhjZmMwZTMxZTRlYjUxZDg2M2QxYjFlZjoJdXNlcmwrCQAQ1w%252FKGN8K--3cfac244f895c88afa6ce723ccb790c3211f427c; guest_id=v1%3A147602625711550778; pid="v3:1476026155109049923941593"; _ga=GA1.2.443570169.1476026155; _gat=1; kdt=pUj3K5tgb4P7IQoEWXaUN6PbGv4w9A9A6K1DvexG; remember_checked_on=1; twid="u=783372116313968640"; auth_token=F2903FB344799D8EF0B7262A0AD052C92FBB53A1; lang=en; moments_profile_moments_nav_tooltip_self=true
	# Connection: close

	#authenticity_token=6f0d0dd6eacfadadece47e9420ae94cb48283ae8&id=784786198992683008&tweet_stat_count=0
	# authenticity_token=6f0d0dd6eacfadadece47e9420ae94cb48283ae8&earned=false&id=770374356434161665&impression_id=5529f3cfca7af84c&tweet_stat_count=7284
	ac=ac.strip()
	twid=twid.strip()
	u='https://twitter.com/i/tweet/'+ac
	cok=GET(vars,'cookie')
	at=GET(vars,'authenticity_token')
	h={
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Language': 'en-US,en;q=0.5',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Referer': 'https://twitter.com/',
	'X-Requested-With': 'XMLHttpRequest',
	'Cookie':cok.replace(' ','')
	}
	d='authenticity_token='+at+'&id='+twid+'&tweet_stat_count=0'
	doer=GET(vars,'username')
	reqdone=False
	while reqdone==False:
		try:
			if debug:
				r=requests.post(url=u,headers=h,data=d,allow_redirects=False,proxies=prox)
			else:
				r=requests.post(url=u,headers=h,data=d,allow_redirects=False)
			reqdone=True
		except Exception,e:
			reqdone=False
			#time.sleep(1)
	if '{"profile_stats":[{"stat":"favorite","user_id":' in r.text or '","retweet_id":"' in r.text:
		vars['lastmsg']=spaces((ac+'ed '+twid),15).replace('likeed','Liked').replace('retwee','ReTwee')+'        by '+doer
		vars['hanged']='True'
	elif '{"message":"Your account may not be allowed to perform this action. Please' in r.text:
		vars['lastmsg']=(ac+'ed ').replace('likeed','Liked')+twid+' before '+'by '+doer
		vars['hanged']='True'
		vars['dup']='True'
	elif '{"errors":[{"message":"Sorry, that page does not exist","code":34}]}':
		vars['lastmsg']=STX.RED+'Tweet not exist or private ['+twid+']'+STX.Green
		vars['error']='Tweet not exist'
	elif isExpired(r):
		vars['expired']='True'
		vars['valid']='False'

	return vars
def isExpired(req):
	if req.status_code==403:
		return True
	elif 'Could not authenticate you' in r.text:
		return True
	return False
def tweet(vars,tweet_str):
	#if duplicated 
	#{"message":"You have already sent this Tweet."}
	#if success
	#{"tweet_id":"784358327354527744",
	# POST /i/tweet/create HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: Application/json, text/javascript, */*; q=0.01
	# Accept-Language: en-US,en;q=0.5
	# Content-Length: 129
	# Content-Type: Application/x-www-form-urlencoded; charset=UTF-8
	# Referer: https://twitter.com/
	# X-Requested-With: XMLHttpRequest
	# Cookie: _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCHFJfpVXAToMY3NyZl9p%250AZCIlMjVlZWZjM2I4NTJjNjM4ZGVmMDZhNjI5MTE0MjJkMjk6B2lkIiU2Nzgx%250ANGQ3NjhiZDJhOGU3ZDBmZjFkMzhkN2QyYWZkMzoJdXNlcmwrCQCAVqPFGN8K--47aa526190a73114d6cae80511a7be72c00b2fc4; guest_id=v1%3A147568186404733977; _ga=GA1.2.1807619857.1475681872; _gat=1; pid="v3:1475681873798613838963613"; kdt=OaNEYOg0NGTyeZHktrtTPrDJTTgI56duV24IcvBu; remember_checked_on=1; twid="u=783372097313734656"; auth_token=AE1764C09ACC94A6844180AB434DD7AFFDE8A607; lang=en
	# Connection: close

	# authenticity_token=b812e12b291977e63d80cda13eba5096a00322f1&is_permalink_page=false&place_id=&status=hello+yankez+x&tagged_users=
	u='https://twitter.com/i/tweet/create'
	cok=GET(vars,'cookie')
	h={'Host:':'twitter.com',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
		'Accept': 'Application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'en-US,en;q=0.5',
		'Content-Type': 'Application/x-www-form-urlencoded; charset=UTF-8',
		'Referer': 'https://twitter.com/',
		'X-Requested-With': 'XMLHttpRequest',
		'Cookie':cok.replace(' ','')
	}
	body='authenticity_token='+GET(vars,'authenticity_token')+'&is_permalink_page=false&place_id=&status='+tweet_str+'&tagged_users='
	#raw_input(cok)

	reqdone=False
	while  reqdone==False:
		try:
			if debug:
				r=requests.post(url=u,headers=h,data=body,allow_redirects=False,proxies=prox)
			else:
				r=requests.post(url=u,headers=h,data=body,allow_redirects=False)
			reqdone=True
		except Exception :
			time.sleep(1)


	if islocked(r.text):
		vars['lastmsg']='Account locked by twitter'
		vars['valid']='False'
		return vars
	if r.text.startswith('{"tweet_id":"'):
		vars['tweeted']='True'
		vars['lastmsg']='Tweeted by '+spaces((GET(vars,'name') if GET(vars,'username')=='False' else GET(vars,'username')).replace('False',''),30)
	elif '{"message":"You have already sent this Tweet."}' in r.text:
		vars['lastmsg']='you already tweeted it before'
	elif '{"message":"Could not authenticate you."}' in r.text:
		vars['lastmsg']='expired'
	else:
		vars['lastmsg']='tweet error /'+GET(vars,'username')
	return vars
def follow(vars,target,action):
	orig=vars
	#if following":false,"follow_request_sent 
	# follwoing now
	#if
	#following":true,"follow_request_sent
	#followed before
	#
	# POST /i/user/follow HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: Application/json, text/javascript, */*; q=0.01
	# Accept-Language: en-US,en;q=0.5
	# Content-Length: 137
	# Content-Type: Application/x-www-form-urlencoded; charset=UTF-8
	# Referer: https://twitter.com/ptionacc
	# X-Requested-With: XMLHttpRequest
	# Cookie: _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCxY755XAToMY3NyZl9p%250AZCIlN2Q1NDk4ZTM5YzFhNGM0MzM0YWMzMzQ2MjAyOTk1MWI6B2lkIiU5OGYz%250ANTNlODFjZGM2MzYwNTYzZGJkYjc3NTA5NTc5ODoJdXNlcmwrCQCAVqPFGN8K--62e3e2d5086b5b9ad11bc75d65423f789052dc15; guest_id=v1%3A147584026833258918; pid="v3:1475840279797512215082069"; lang=en; _ga=GA1.2.1527069807.1475840308; kdt=fN0vxoVouSPGFsGDQeY1cWaAZTcfIuRXnHllDkSZ; remember_checked_on=1; twid="u=783372097313734656"; auth_token=AE1764C09ACC94A6844180AB434DD7AFFDE8A607; moments_profile_moments_nav_tooltip_self=true
	# Connection: close

	# authenticity_token=3faceb6a373f90a19aa98a423e11c7bed8e9a51d&challenges_passed=false&handles_challenges=1&impression_id=&user_id=104557267
	ModeUnfollow=False
	if len(action)>1:
		ModeUnfollow=True
	if action=='':
		action='follow'
	target=target.strip()

	vars['lastmsg']='trying to '+action +'  '+target+'  by '+GET(vars,'username')#('un' if ModeUnfollow else '')+'follow '+target
	ur='https://twitter.com/i/user/'+ action
	cok=GET(vars,'cookie').replace(' ','')
	hd={
	'Host': 'twitter.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Accept': 'Application/json, text/javascript, */*; q=0.01',
	'Accept-Language': 'en-US,en;q=0.5',
	'Content-Type': 'Application/x-www-form-urlencoded; charset=UTF-8',
	'Referer': 'https://twitter.com/johncena',
	'X-Requested-With': 'XMLHttpRequest',
	'Cookie':cok.replace(' ','')
	}
	at=GET(vars,'authenticity_token')
	bod='authenticity_token='+at+'&challenges_passed=false&handles_challenges=1&impression_id=&user_id='+target
	reqdone=False
	while reqdone==False:
		try:
			if debug:
				r=requests.post(url=ur,headers=hd,data=bod,allow_redirects=False,proxies=prox)
			else:
				r=requests.post(url=ur,headers=hd,data=bod,allow_redirects=False)
			reqdone=True
		except Exception:
			prints('\n Error ..')
	if islocked(r.text):
		ClearSuspendedSession(orig)
		vars['lastmsg']='Account locked by twitter '+GET(vars,'username')
		vars['valid']='False'
		return vars

	doer=GET(vars,'username')
	by=('' if doer == 'False' or len(doer)<1 else '  by '+doer)

	if ModeUnfollow is False:
		if r.text.startswith('{"new_state":"following'):#success
			vars['followsent']='True'
			vars['follow']='True'
			if ',"following":false,"follow_request_sent":' in r.text: #new follow
				vars['lastmsg']=spaces(action+'ed       '+target,20).replace('fol','Fol')+by
			elif ',"following":true,"follow_request_sent"' in r.text:
				vars['lastmsg']=     'Followed before '+target+by
		elif '"errors":[{"message":"Sorry, that page does not exist","code' in r.text:
			vars['lastmsg']='user not existed'
	else:
		if r.text.startswith('{"new_state":"not-following",'):
			vars['unfollowsent']='True'
			vars['lastmsg']='Unfollowed '+target+by
	vars['respbody']=bod
	return vars
def JustFollow(vars,target):
	return follow(vars,target,'')
def JustunFollow(vars,target):
	return follow(vars,target,'unfollow')
def getuserid(target):
	# <div class="ProfileNav" role="navigation" data-user-id="783372116313968640">
	#
	#GET /helloworldthis7 HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8
	# Accept-Language: en-US,en;q=0.5
	# Connection: close	
	u='https://twitter.com/'+target
	h={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0','Accept': 'text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5'}
	if debug:
		r=requests.get(url=u,headers=h,allow_redirects=False,proxies=prox)
	else:
		r=requests.get(url=u,headers=h,allow_redirects=False)
	
	if '<div class="ProfileNav" role="navigation" data-user-id=' in r.text:
		x=r.text.split('<div class="ProfileNav" role="navigation" data-user-id="')
		x=x[1]
		if '"' in x:
			return x.split('"')[0]
		if target not in par.users_IDS:
			par.users_IDS[target]=x

		par.users_IDS[target]=x
		storeValidUserIds()

		return x
	else:
		return 'not found'	



def updateBirthdate(vars,day,month,year):
	# 	POST /i/profiles/update HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: Application/json, text/javascript, */*; q=0.01	
	# Accept-Language: en-US,en;q=0.5
	# Content-Length: 215
	# Content-Type: Application/x-www-form-urlencoded; charset=UTF-8
	# Referer: https://twitter.com:2.vo/a7a
	# X-Requestedc-With: XMLHttpRequest
	# Cookie: _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCx%252BGaVXAToMY3NyZl9p%250AZCIlNTcxMWJhYTNiNzljYjE5YzFjN2E5YTE1ZmJlMjA5N2M6B2lkIiUzOTUw%250AODIyZTUwNzJkOGEzNjQwZjE5YzQyNmI1OGVhMzoJdXNlcmwrCQBg1heXGd8K--5f81caf6b1ab50b99988b302bbb16440e9c53500; guest_id=v1%3A147594369386702081; _ga=GA1.2.68612384.1475943703; _gat=1; pid="v3:1475943703798264582729593"; kdt=U3cOSxKOIIaeHNbtQrIBeI7S03B2BojugjicyjKx; remember_checked_on=1; twid="u=783372996916436992"; auth_token=CE6E82CB9C06EBD15292070884211D8E8070FA9C; lang=en
	# Connection: close
	u='https://twitter.com/i/profiles/update'
	cok=GET(vars,'cookie').replace(' ','')
	h={
	'Host': 'twitter.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Accept': 'Application/json, text/javascript, */*; q=0.01',
	'Accept-Language': 'en-US,en;q=0.5',
	'Content-Type': 'Application/x-www-form-urlencoded; charset=UTF-8',
	'Referer': 'https://twitter.com/ptionacc',
	'X-Requested-With': 'XMLHttpRequest',
	'Cookie': cok.replace(' ','')
	}
	at=GET(vars,'authenticity_token')
	data='authenticity_token='+at+'&user%5Bbirthdate%5D%5Bbirthday_visibility%5D=1&user%5Bbirthdate%5D%5Bbirthyear_visibility%5D=0&user%5Bbirthdate%5D%5Bday%5D='+str(day)+'&user%5Bbirthdate%5D%5Bmonth%5D='+str(month)+'&user%5Bbirthdate%5D%5Byear%5D='+str(year)#&page_context=me&section_context=profile&user%5Bdescription%5D='+udesc+'&user%5Burl%5D='+uurl
	if debug:
		r=requests.post(url=u,headers=h,data=data,allow_redirects=False,proxies=prox)
	else:
		r=requests.post(url=u,headers=h,data=data,allow_redirects=False)
	if islocked(r.text):
		vars['lastmsg']='Account locked by twitter'
		vars['valid']='False'
		return vars
	if '{"message":"Your account may not be allowed to perform this action.' in r.text:#url invalid
		vars['lastmsg']='invalid request'
		vars['error']='invalid request '
	elif r.text.startswith('{"emojified_name":"'):
		vars['lastmsg']='birthdate updated'
		vars['bioupdated']='True'
	elif '{"message":"Account update failed: Invalid birthdate range."}' in r.text:
		vars['lastmsg']='failed to update birthdate'
		vars['error']='invalid birthdate'

	return vars

# authenticity_token=x&user%5Bbirthdate%5D%5Bbirthday_visibility%5D=1&user%5Bbirthdate%5D%5Bbirthyear_visibility%5D=0&user%5Bbirthdate%5D%5Bday%5D=18&user%5Bbirthdate%5D%5Bmonth%5D=2&user%5Bbirthdate%5D%5Byear%5D=1985
def updateBio(vars,udesc,uurl):
	# 	POST /i/profiles/update HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: Application/json, text/javascript, */*; q=0.01
	# Accept-Language: en-US,en;q=0.5
	# Content-Length: 242
	# Content-Type: Application/x-www-form-urlencoded; charset=UTF-8
	# Referer: https://twitter.com/ptionacc
	# X-Requested-With: XMLHttpRequest
	# Cookie: _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCxY755XAToMY3NyZl9p%250AZCIlN2Q1NDk4ZTM5YzFhNGM0MzM0YWMzMzQ2MjAyOTk1MWI6B2lkIiU5OGYz%250ANTNlODFjZGM2MzYwNTYzZGJkYjc3NTA5NTc5ODoJdXNlcmwrCQCAVqPFGN8K--62e3e2d5086b5b9ad11bc75d65423f789052dc15; guest_id=v1%3A147584026833258918; pid="v3:1475840279797512215082069"; lang=en; _ga=GA1.2.1527069807.1475840308; kdt=fN0vxoVouSPGFsGDQeY1cWaAZTcfIuRXnHllDkSZ; remember_checked_on=1; twid="u=783372097313734656"; auth_token=AE1764C09ACC94A6844180AB434DD7AFFDE8A607; moments_profile_moments_nav_tooltip_self=true; moments_user_moment_profile_create_moment_tooltip=true; _gat=1
	# Connection: close

	# authenticity_token=3faceb6a373f90a19aa98a423e11c7bed8e9a51d&page_context=me&section_context=profile&user%5Bdescription%5D=Fan+of+%40yassergersy%0A+%7C+We+control+your+digital+world+%7C+We+are+legion&user%5Burl%5D=https%3A%2F%2F404notfound.com
	#authenticity_token=3faceb6a373f90a19aa98a423e11c7bed8e9a51d&page_context=me&section_context=profile&user%5Bname%5D=Dr_exception
	u='https://twitter.com/i/profiles/update'
	cok=GET(vars,'cookie').replace(' ','')
	h={
	'Host': 'twitter.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Accept': 'Application/json, text/javascript, */*; q=0.01',
	'Accept-Language': 'en-US,en;q=0.5',
	'Content-Type': 'Application/x-www-form-urlencoded; charset=UTF-8',
	'Referer': 'https://twitter.com/ptionacc',
	'X-Requested-With': 'XMLHttpRequest',
	'Cookie': cok.replace(' ','')
	}
	at=GET(vars,'authenticity_token')
	data='authenticity_token='+at+'&page_context=me&section_context=profile&user%5Bdescription%5D='+udesc+'&user%5Burl%5D='+uurl
	if debug:
		r=requests.post(url=u,headers=h,data=data,allow_redirects=False,proxies=prox)
	else:
		r=requests.post(url=u,headers=h,data=data,allow_redirects=False)
	if islocked(r.text):
		vars['lastmsg']='Account locked by twitter'
		vars['valid']='False'
		return vars
	if '{"message":"Url is not valid"}' in r.text:#url invalid
		vars['lastmsg']='updated url is invalid'
		vars['error']='invalid bio url '
	elif r.text.startswith('{"emojified_name":"'):
		vars['lastmsg']='Profile updated'
		vars['bioupdated']='True'

	return vars
def ping(vars):
	#data-user-id="783365603918802944" data-screen-name="helloworldthis3"><b class="fullname">_Dr Exception_</b><span class="screen-name hidden"
	# GET / HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8
	# Accept-Language: en-US,en;q=0.5
	# Referer: https://twitter.com/login
	# Cookie: _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCxY755XAToMY3NyZl9p%250AZCIlN2Q1NDk4ZTM5YzFhNGM0MzM0YWMzMzQ2MjAyOTk1MWI6B2lkIiU5OGYz%250ANTNlODFjZGM2MzYwNTYzZGJkYjc3NTA5NTc5ODoJdXNlcmwrCQCAVqPFGN8K--62e3e2d5086b5b9ad11bc75d65423f789052dc15; guest_id=v1%3A147584026833258918; pid="v3:1475840279797512215082069"; lang=en; _ga=GA1.2.1527069807.1475840308; _gat=1; kdt=fN0vxoVouSPGFsGDQeY1cWaAZTcfIuRXnHllDkSZ; remember_checked_on=1; twid="u=783372097313734656"; auth_token=AE1764C09ACC94A6844180AB434DD7AFFDE8A607
	# Connection: close
	# Upgrade-Insecure-Requests: 1
	
	#prints('\n 		Getting info')
	u ='https://twitter.com/'
	cok=GET(vars,'cookie').replace(' ','')
	h={
	'Host': 'twitter.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Accept': 'text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Referer': 'https://twitter.com/login',
	'Cookie': cok.replace(' ',''),
	 'Upgrade-Insecure-Requests': '1'
	
	}
	reqdone=False

	reqdone=False
	while reqdone==False:
		try:
			if debug:
				r=requests.get(url=u,headers=h,allow_redirects=False,proxies=prox)
			else:
				r=requests.get(url=u,headers=h,allow_redirects=False)
			reqdone=True
		except Exception,er:
			reqdone=False
			if '[Errno 8] _ssl.c:499: EOF occurred in violation of protocol' not in str(er):
				print('Error\n'+str(er))

	if islocked(r.text):
		vars['lastmsg']='Account locked by twitter'
		vars['valid']='False'
		return vars
	vars['valid']='False'
	if 'class="account-group js-mini-current-user"' in r.text :
		vars['valid']='True'
		ix= r.text.split('class="account-group js-mini-current-user"')
		col=ix[1].split('</b><span')[0]
		#data-user-id="783365603918802944" data-screen-name="helloworldthis3"><b class="fullname">_Dr Exception_
		arr=col.split('"')
		____id____=arr[1]
		__username_=arr[3]
		__name_____=col.split('>')[2]
		vars['id']=____id____
		vars['username']=__username_
		vars['name']=__name_____
	else:
		vars['valid']='False'
	return vars
def updateName(vars,name):
	# 	POST /i/profiles/update HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: Application/json, text/javascript, */*; q=0.01
	# Accept-Language: en-US,en;q=0.5
	# Content-Length: 242
	# Content-Type: Application/x-www-form-urlencoded; charset=UTF-8
	# Referer: https://twitter.com/ptionacc
	# X-Requested-With: XMLHttpRequest
	# Cookie: _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCxY755XAToMY3NyZl9p%250AZCIlN2Q1NDk4ZTM5YzFhNGM0MzM0YWMzMzQ2MjAyOTk1MWI6B2lkIiU5OGYz%250ANTNlODFjZGM2MzYwNTYzZGJkYjc3NTA5NTc5ODoJdXNlcmwrCQCAVqPFGN8K--62e3e2d5086b5b9ad11bc75d65423f789052dc15; guest_id=v1%3A147584026833258918; pid="v3:1475840279797512215082069"; lang=en; _ga=GA1.2.1527069807.1475840308; kdt=fN0vxoVouSPGFsGDQeY1cWaAZTcfIuRXnHllDkSZ; remember_checked_on=1; twid="u=783372097313734656"; auth_token=AE1764C09ACC94A6844180AB434DD7AFFDE8A607; moments_profile_moments_nav_tooltip_self=true; moments_user_moment_profile_create_moment_tooltip=true; _gat=1
	# Connection: close

	# authenticity_token=3faceb6a373f90a19aa98a423e11c7bed8e9a51d&page_context=me&section_context=profile&user%5Bdescription%5D=Fan+of+%40yassergersy%0A+%7C+We+control+your+digital+world+%7C+We+are+legion&user%5Burl%5D=https%3A%2F%2F404notfound.com
	#authenticity_token=3faceb6a373f90a19aa98a423e11c7bed8e9a51d&page_context=me&section_context=profile&user%5Bname%5D=Dr_exception
	u='https://twitter.com/i/profiles/update'
	cok=GET(vars,'cookie').replace(' ','')
	h={
	'Host': 'twitter.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Accept': 'Application/json, text/javascript, */*; q=0.01',
	'Accept-Language': 'en-US,en;q=0.5',
	'Content-Type': 'Application/x-www-form-urlencoded; charset=UTF-8',
	'Referer': 'https://twitter.com/ptionacc',
	'X-Requested-With': 'XMLHttpRequest',
	'Cookie': cok.replace(' ','')
	}
	at=GET(vars,'authenticity_token')
	data='authenticity_token='+at+'&page_context=me&section_context=profile&profile&user%5Bname%5D='+name #user%5Bdescription%5D='+udesc+'&user%5Burl%5D='+uurl
	if debug:
		r=requests.post(url=u,headers=h,data=data,allow_redirects=False,proxies=prox)
	else:
		r=requests.post(url=u,headers=h,data=data,allow_redirects=False)
	if islocked(r.text):
		vars['lastmsg']='Account locked by twitter'
		vars['valid']='False'
		return vars
	if r.text.startswith('{"emojified_name":"'):
		vars['lastmsg']='Name updated'
		vars['bioupdated']='True'
		vars['nameupdated']='True'

	return vars

def Do_update_Name(uemail,upas,name):
	resp=Do_login(uemail,upas)
	if GET(resp,'valid')=='True':
		resp=updateName (resp,name)
	return resp
def Do_update_bio(uemail,upas,desc,uurl):
	resp=Do_login(uemail,upas)
	if GET(resp,'valid')=='True':
		resp=updateBio(resp,desc,uurl)
	return resp
def Do_Follow(uemail,upas,target):
	response2=Do_login(uemail,upas)
	if GET(response2,'valid')=='True':
		response3=follow(response2,target,'')
		print GET(response3,'lastmsg')
	return response3
def Do_unFollow(uemail,upas,target):
	response2=Do_login(uemail,upas)
	if GET(response2,'valid')=='True':
		response3=follow(response2,target,'un')
		print GET(response3,'lastmsg')
	return response3
def Do_login(uemail,upas):

	response1={}
	response1['initrequest']='False'
	count0=0
	while  GET(response1,'initrequest')=='False':
		count0=count0+1
		response1=init()
		if count0>3:
			break 
		elif GET(response1,'initrequest')=='False':
			time.sleep(3)
			print GET(response1,'lastmsg')
			print(response1['initrequest'] if  response1['initrequest'] != 'False' else response1['lasterror'])
		else:
			print 'initated'

	response1['email']=uemail
	response1['password']=upas
	response2={}
	response2['sessionrequest']='False'
	count1=0
	while  GET(response2,'sessionrequest')=='False':
		count1=count1+1
		response2=session(response1)
		if GET(response2,'sessionrequest')=='False':
			#time.sleep(3)
			print ('waiting 2')
			print GET(response2,'lastmsg')
		if count1==4:
			break

	if GET(response2,'sessionrequest') :
		print 'valid'
		response2['valid']='True'
	else :
		print GET(response2,'lastmsg')
	return response2
def Do_Get_Device(uemail,upas):
	response2=Do_login(uemail,upas)
	if GET(response2,'valid')=='True':
		response3=getdevices(response2)
		print response3['lastmsg']
	else:
		print GET(response3,'lastmsg')
def Do_Delete_Device(uemail,upas):
	resp=Do_Get_Device(uemail,upas)
	resp2=deleteDevice(resp)
	print GET(resp,'device_id')
	print GET(resp2,'lastmsg')
def Do_tweet(uemail,upas,twstr):
	resp=Do_login(uemail,upas)
	if GET(resp,'valid')=='True':
		resp2=tweet(resp,twstr)
		print ('Result of tweeting = '+GET(resp2,'lastmsg'))

def Load_Users_Ids():
	if os.path.isfile(App.users_ids_file):
		with open(App.users_ids_file) as uiread:
			lines=uiread.readlines()
			for l in lines:
				if ':' in l:
					x=l.split(':')
					username=x[0]
					user_id=x[1]
					if len(username)<1 or len(user_id) <1:
						continue
					par.users_IDS[username]=user_id
			if len(par.users_IDS) >0:
				prints(STX.Blue+'\n\n     Reading users ids ..\n'+STX.Green+'     Loaded = '+str(len(par.users_IDS)))
				par.Loaded_users_ids_count=len(par.users_IDS)
def followunfolow():	
	lines=''
	coun=0
	loop=-1
	with open('valid_ids.txt') as stm:
		lines=stm.readlines()
	for l in lines:
		loop=loop+1
		if l.startswith('#'):
			continue
		x=l.split(':')
		i=x[0].strip()
		p=''
		try:
			p=x[1].strip()
		except Exception:
			p=''
		if p=='' :
			continue
		print '\n-----['+str(loop+1)+']--------\n"'+i+' 	: "'+p+'"\n--------------'
		#Do_Get_Device(i,p)
		#Do_tweet(i,p,'#we_control_your_digital_world')
		#Do_Delete_Device(i,p)
		z=Do_unFollow(i,p,'330508216')
		if GET(z,'followsent')=='True':
			coun=coun+1
	print ('\n------------['+str(coun)+'] follow Sent \n') 
def init_Me():
	Load_ids_passwords()
	Load_Users_Ids()
	#Getting old sessions
	prints(STX.Blue+'\n\n [+] Getting old sessions ....')
	if os.path.isfile('sessions.txt'):
		prints(STX.Green+'\n     Session File  exists \n')
		readsess= open('sessions.txt')
		tmp=readsess.read()
		if STX.session_separator in tmp:
			par.Loaded_Session_list=tmp.split(STX.session_separator)
		else:
			par.Loaded_Session_list.append(tmp)
		prints('     Found sesssions = '+str(len(par.Loaded_Session_list)-1))
		readsess.close()
	else:
		prints('\n Sessions file not found ('+App.session_file+')')
	#deserialize old sessions
	if len(par.Loaded_Session_list) >0:
		prints(STX.Blue+'\n\n [+] Deserializing old sessions ')
		for session_string in par.Loaded_Session_list:
			if '\n' not in session_string:
				continue
			if len(session_string.strip())<2:
				continue
			sessionObject=deserializeSession(session_string)
			if GET(sessionObject,'deserialized')!='False':
				par.deserialized_sessions.append(sessionObject)	
		prints(STX.Green+'\n     Deserialized sessions = '+str(len(par.deserialized_sessions)))
	else:
		prints('\n No sessions found , try to generate ')
	par.valid_sessions=par.deserialized_sessions
def isValidNum(x1,min,max):
	x=x1.strip()
	if x.isdigit()==False:
		return False
	sx=int(x)
	if sx<min:
		return False
	if sx>max:
		return False
	return True
def returnAction(int_):
	actions=['exit','getid','tweet','like','retweet','follow','reply','dm','spam','report',
	'check','generate','filter','fix','add','login','show','selffollow']
	return actions[int_]
def FixBrockenSessions():
	#Fixing brocken sessions
	valid_sessions=[]
	par.valid_sessions_string=''
	if True:#par.ISSUENEWSES:
		prints('\n\n [+]Getting new sessions \n')
		#raw_input(par.valid_sessions_emails)
		somecount=-1
		for _idLine_ in par.ids_lines:
			somecount=somecount+1
			if ':' not in _idLine_ or _idLine_.startswith('#'):
				continue
			arx=_idLine_.split(':')
			uid=arx[0].strip()
			upas=arx[1].strip()
			if  len(uid) <2 or len(upas) <2 :
				continue
			elif uid in par.valid_sessions_emails:
				continue
			prints('\n['+str(somecount+1)+']  	Login with "'+uid+'"" @ "'+upas+'" 	\n')
			newsess=Do_login(uid,upas)
			strex=''
			if GET(newsess,'valid')!='False':
				addValidSession(newsess)
				# par.valid_sessions_string=par.valid_sessions_string+SerializeSession(newsess)
				# if uid not in par.valid_sessions_emails:
				# 	par.valid_sessions_emails.append(uid)
def constructValidSessionString():
	par.valid_sessions_string=''
	for s in par.valid_sessions:
		par.valid_sessions_string=par.valid_sessions_string+SerializeSession(s)

def issessionExitsOnList(s,lis):
	for ns in lis:
		g=GET(ns,'email')
		z=GET(s,'email')
		if z=='False':
			z='somethingsasf'
		if g==z:
			return True
	return False
def Generate_sessions_fromAccounts():
	if len(par.users_IDS) < 1:
		prints('\n no accounts found')
	else:
		prints('\n Generating sessions ...')
		poc=1
		for l in par.Ids_and_passwords:
			poc=poc+1
			i=l
			p=par.Ids_and_passwords[l]
			if len(i)<1:
				continue
			if len(p) < 6:
				continue
			s=initSession(i,p)
			if GET(s,'valid')=='True':
				prints('\n '+spaces(str(poc),3)+'  Session initated for [ '+l+' ]' )
				if issessionExitsOnList(s,par.valid_sessions):
					continue
				else:
					addValidSession(s)

			else:
				prints(spaces('\n'+str(poc)+' Login failed for ['+l+']		',10)+GET(s,'error'))
			
				
	prints(STX.yel+'\n Valid sessions = '+str(   len(par.valid_sessions)  )  )

def CheckCurrentSessions():
	#checking session availability
	if True:#par.PINGOLDSES:#force ping
		vsex=par.valid_sessions
		par.valid_sessions=[]
		prints('\n\n[+]Checking old sessions ')
		pingcount=-1
		for deserialized_ in vsex:
			em=GET(deserialized_,'email')
			pingcount=pingcount+1
			prints(STX.yel+'\n   ['+str(pingcount+1)+']  [ping]	 ['+em+' ] 	')
			r=ping(deserialized_)
			if GET(r,'locked')=='True':
				prints('\n '+GET(r,'lastmsg'))
				continue
			if GET(r,'valid')!='False':		
				em=GET(r,'email').strip()
				if GET(r,'expired')!='True':
				# if em not in par.valid_sessions_emails or len(em) < 2:
				# 	par.valid_sessions_emails.append(em)
				# 	par.valid_sessions_string=par.valid_sessions_string+SerializeSession(r)
				 	addValidSession(r)
					prints(STX.Green+'\n        [+] valid  			id= '+GET(r,'id')+'\n        username= '+spaces(GET(r,'username'),10)+'     	name= '+GET(r,'name')+'')
				else:
					prints('\n 	Expired')
			else:
				prints(STX.RED+'\n        [-] invalid ')
				
		prints(STX.Blue+'\n--------------\n Valid sessions='+str(len(par.valid_sessions)))
	else:
		par.valid_sessions=par.deserialized_sessions
def StoreValidSessions():
	#storing valid sessions
	# constructValidSessionString()
	# if len(par.valid_sessions_string)>10 and '\n' in par.valid_sessions_string:
	# 	store=open('sessions.txt','w')
	# 	print('Storing Valid sessions ')
	# 	store.write(par.valid_sessions_string)
	# 	prints('\n Saved sessions\n\n')

	if len(par.valid_sessions) >0:
		xv='#cound='+str(len(par.valid_sessions))+'\n\n'
		for s in par.valid_sessions:
			ds = SerializeSession(s)
			xv=xv+ds+'\n'
		x=open(App.session_file,'w')
		x.write(xv)
		x.close()
		prints('\n Stored valid session '+str(len(par.valid_sessions)))
	else:
		prints('empty list')
def spaces(s,l):
	return s+(' '*(l-len(s)))
def Load_ids_passwords():
	prints(STX.Blue+' [+] Loading Accounts  ')
	if os.path.isfile(App.ids_file) is False:
		prints(' 	[-]File not found ')
		return 
	with open(App.ids_file) as red:
		lines=red.readlines()
		for l in lines:
			if l.startswith('#'):
				continue
			elif ':' not in l:
				continue
			else:
				arr=l.split(':')
				aid=arr[0].strip()
				aps=arr[1].strip()
				if len(aid)<1 or len(aps) <6:
					continue
				else:
					par.Ids_and_passwords[aid]=aps
		prints(STX.Green+'\n     Loaded ids '+str(len(par.Ids_and_passwords)))

	return
def prompt_not_empty(s,min=1,l=1000):
	emp=True
	vc=''#raw_input(s+STX.magenta).strip()
	while  len(vc) < min :
		vc=raw_input(s+STX.magenta)
	if len(vc) > l:
		vc=vc[0:l]
	return vc
def SplitIDsUserInputToArray(s,l):
	x=[]
	res=[]
	if ',' in s:
		x=s.split(',')
	else:
		x=[s]
	for o in x:
		i=o.strip()
		if len(i)<l or ' ' in o:
			continue
		
		if '/' in i:
			i=(i.split('/')[-1])
		if '?' in i :
			i=i.split('?')[0]

		res.append(i)
	return res
def storeValidUserIds():
	res=''
	if len(par.users_IDS) > 0 :#and len(par.users_IDS)>par.Loaded_users_ids_count:
		for l in par.users_IDS:
			res=res+'\n'+l+':'+par.users_IDS[l]
		if len(res)>1 :
			x=open(App.users_ids_file,'w')
			x.write(res.replace('\n\n','\n')+'\n')
			x.close()
			prints('\n Saved grabbed users iDS to '+App.users_ids_file+'   +')
			prints(len(par.users_IDS))
def Leav():
	prints(STX.yel+'\n Leaving ...... ')
	StoreValidSessions()
	storeValidUserIds()
	prints(STX.Green+STX.lin+STX.White+'\n')
	exit(0)

def AutoMate_Mass_Follow(ids):
	nids=[]
	prints('\n [+]Getting users ids')
	for p in ids:
		if p.isdigit():
			nids.append(p)
		else:
			v=Getcash_user_id(p)
			if v !=' not found':
				nids.append(v)
			prints('\n 	'+p+'   '+v)
	ids=nids
	all=0
	exp=[]
	counc=0
	prints('\n    Following ..'+str(ids).encode('utf-8').replace('u',''))
	for l in ids:
		li=0
		sescount=-1
		for s in par.valid_sessions:
			sescount=sescount+1
			counc=counc+1
			if s in exp:
				
				prints('\n Expired skipped')
				continue
			s['sesindex']=sescount
			r=JustFollow(s,l)
			StoreValidator(r)
			if GET(r,'follow')!='False':
				if GET(r,'dup')!='True' and 'trying to follow' not in GET(r,'lastmsg'):
					li=li+1
					all=all+1
			elif GET(r,'expired')=='True':
				exp.append(s)
			prints('\n   '+spaces(str(counc),2)+'   '+GET(r,'lastmsg').replace('trying to','Can not '))
	prints('\n All Follows sent = '+str(all))
def AutoMate_Post_Retweets(ids,likespertweet):
	exp=[]
	all=0
	for l in ids:
		li=0
		for s in par.valid_sessions:
			if s in exp:
				continue
			if li==likespertweet:
				break
			r=PostReTweet(s,l)
			if GET(r,'hanged')!='False':
				if GET(r,'dup')!='True':
					li=li+1
					all=all+1
				prints('\n'+GET(r,'lastmsg'))
			elif GET(r,'expired')=='True':
				exp.append(s)
		#prints('\n Likes Sent to '+l+' ='+str(li))
	prints('\n All Retweets sent = '+str(all))
def AutoMate_Set_Likes(ids,likespertweet):
	exp=[]
	invalidIds=[]
	all=0
	for il in range(0,len(ids)):
	#for l in ids:
		l=ids[il]
		li=0
		if l in invalidIds:
			continue
		for i_s in range(0,len(par.valid_sessions)):
#		for s in par.valid_sessions:
			s=par.valid_sessions[i_s]
			if s in exp:
				continue
			if li==likespertweet:
				il=il+1
				if il >= len(ids):
					break
			r=LikeATweet(s,l)
			if GET(r,'hanged')!='False':
				if GET(r,'dup')!='True':
					li=li+1
					all=all+1
				prints('\n'+GET(r,'lastmsg'))
			elif GET(r,'expired')=='True':
				exp.append(s)
			if   'Tweet not exist' in GET(r,'lastmsg'):
				invalidIds.append(l)
				break

		#prints('\n Likes Sent to '+l+' ='+str(li))
	prints('\n All likes sent = '+str(all))

	# for s in par.valid_sessions:
	# 	for l in ids:
	# 		r=LikeATweet(s,l)
	# 		if GET(r,'liked')=='False':
	# 			raw_input(r)
	# 			break
	# 		else:
	# 			prints(GET(r,'lastmsg')+'\n')
def AutoMate_Get_UserIds(lis):
	for l in lis:
		if l in par.users_IDS:
			res=par.users_IDS[l]
		else:
			res=getuserid(l)
			par.users_IDS[l]=res
		prints(STX.Green+'\n User [ '+STX.yel+spaces(''+l,15)+STX.Green+' ]  '+(STX.RED+'not exists on twitter' if res=='not found' else 'id is [ '+STX.yel+res+STX.Green+' ]'))
	storeValidUserIds()
def GetTweetIds(u,lastid):

	# GET /i/profiles/show/yassergersy/timeline/tweets?include_available_features=1&include_entities=1&max_position=723202757822304256&reset_error_state=false HTTP/1.1
	# Host: twitter.com
	# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0
	# Accept: application/json, text/javascript, */*; q=0.01
	# Accept-Language: en-US,en;q=0.5
	# X-Requested-With: XMLHttpRequest
	# Referer: https://twitter.com/yassergersy
	# Cookie: _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCBmvS8pXAToMY3NyZl9p%250AZCIlZjRhZTU1ZDZkNDlhNzM5YWFhYzQwMjMxOGVkOGU3MzA6B2lkIiU5NDZi%250ANzE3YzYwNWE2NmVlODIwY2JlZjJlYWU5YWM2NA%253D%253D--c79c2efaa310f3d79cf1a2f1979cdba2626f0510; guest_id=v1%3A147656774018470601; _gat=1; pid="v3:1476567750510185312822237"; _ga=GA1.2.1909173556.1476567795; lang=en
	# Connection: close

	url='https://twitter.com/i/profiles/show/'+u.strip()+'/timeline/tweets?include_available_features=1&include_entities=1&max_position='+lastid.strip()+'&reset_error_state=false'
	h={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0','Accept': 'text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5'}
	reqdone=False
	r=''
	while  reqdone==False:
		try:
			if debug:
				r=requests.get(url=url,headers=h,allow_redirects=False,proxies=prox)
			else:
				r=requests.get(url=url,headers=h,allow_redirects=False)
			reqdone=True
		except Exception:
			prints('\ error on gettweetids ... retrying ')
			reqdone=False
	
	arr=r.text.split('stream-item-tweet-')
	res=[]
	for ax in arr:
		# if ax[0].isdigit()==False:
		# 	continue
		if '\\' in ax:
			ax=ax.split('\\')[0]
		ax=ax.strip()
		if ax.isdigit() and ax not in res and len(str(ax)) >= 12:
			res.append(ax)
	#prints('\n Loaded = '+str(len(res)))

	return res
def GetFirst19TweetsIDS(u):
	res=[]
	if '/' in u :
		u=u.split('/')[-1]

	url='https://twitter.com/'+u
	h={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0','Accept': 'text/html,Application/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5'}
	reqdone=False
	while  reqdone==False:
		try:
			if debug:
				r=requests.get(url=url,headers=h,allow_redirects=False,proxies=prox)
			else:
				r=requests.get(url=url,headers=h,allow_redirects=False)
			reqdone=True
		except Exception:
			prints('\ error on gettweetids ... retrying ')
			reqdone=False
	#<a href="/traffup/status/781800739400065024" class="tweet-timestamp js-permalink js-nav js-tooltip" data-original-title="3:19 AM - 30 Sep 2016">
	#<span class="_timestamp js-short-timestamp " data-aria-label-part="last" data-time="1475230796" data-time-ms="1475230796000" data-long-form="true">Sep 30</span></a>
	deli='data-permalink-path="/'+u+'/status/'
	deli2='data-item-id="'
	del3='" id="stream-item-tweet-'
	arr=r.text.encode('utf-8').split(deli)
	prints(STX.yel+'\n Getting tweets ids for '+u+'\n')
	for a in arr:
		if '"' in a:
			a=a.split('"')[0]
			if a.isdigit()==False:

				continue
			if a not in res  and len(str(a)) >= 15:
				res.append(a)
			
	if len(res)<1:
		del2='" class="tweet-timestamp js-permalink'
		arx=r.text.encode('utf-8').split(del2)
		for arzn in arx:
			arz=arzn.strip()
			if '/' not in arzn:
				continue
			v=arz.split('/')
			for v2 in v :
				if v2.isdigit():
					if v2 not in res and len(str(v2))>= 15:
						res.append(v2) 

	#prints('\n Ids = '+str(len(res)))

	#Getting tweets count
	vc=0
	try:
		vc=r.text.encode('utf-8').split('<span class="ProfileNav-value" data-is-compact="false">')
		vc=vc[1]
		vc=vc.split('<')[0].replace(',','')
		prints('\n Max Tweets = ['+str(vc)+']')
		vc=int(vc)
	except Exception:
		vc=0

	return res,vc

def GetMassTweetsIds(user ,count):
	twetsids,maxt=GetFirst19TweetsIDS(u)
	
	if len(twetsids) <1:
		return []
	if count==19  or (count>maxt and maxt<=19) or (count<19 and count>=maxt):
		return twetsids
	
	c=count
	lastELeIndex=len(twetsids)-1
	for i in range(0,c):
		while  lastELeIndex >= len(twetsids):
			lastELeIndex=lastELeIndex-1
		while  lastELeIndex< 0:
			lastELeIndex=lastELeIndex+1

		lastt=twetsids[lastELeIndex]
		if len(twetsids) >= maxt or len(twetsids) >= count:
			if len(twetsids) <= count:
				return twetsids
			else:
				return twetsids[0:count]
		dd=GetTweetIds(u,lastt)
		same=len(twetsids)
		for o in dd:
			if o not in twetsids:
				twetsids.append(o)
		if same==len(twetsids):
			lastELeIndex=lastELeIndex-1

	if len(twetsids) > count:
		twetsids=twetsids[0:count]


	return twetsids
def AutoMate_Mass_Spam(uids,count,startIndex,likespertweet):
	prints('\n Launching Mass Spams on '+str(len(uids))+' Users\n'+STX.havlin+'\n')
	for u in uids:
		twetsids=GetMassTweetsIds(u,count)
		prints('\n Loaded '+str(len(twetsids))+' Tweets for '+str(u))
		if len(twetsids) <= startIndex:
			startIndex=0
		else:
			prints('\n Starting from '+twetsids[startIndex]+'\n')
		AutoMate_Set_Likes(twetsids[startIndex:],likespertweet)
		AutoMate_Post_Retweets(twetsids[startIndex:],likespertweet)

def AutoMate_Mass_Tweet(twstr,twcount):
	done=0
	prints('\n Launching Mass Tweets '+str(twcount)+' \n'+STX.havlin+'\n')
	
	w=0
	while  done != twcount:

		randomstring=randomstr(5)
		for s in par.valid_sessions:
			r=tweet(s,twstr+'-'+randomstring) #chr(vb)+chr(vb2))
			if done==twcount:
				break
			if GET(r,'tweeted')!='False':
				done=done+1
			elif 'ou already tweeted it before' in GET(r,'lastmsg'):
				r=tweet(s,twstr+'-'+randomstring) #vb2=vb2+1

			w=w+1
			print spaces(str(w),5)+GET(r,'lastmsg')
		time.sleep(1)
		print('')
	prints('\n All tweets sent = '+str(done))

def Getcash_user_id(u):
	x=''
	if u in par.users_IDS:
		x= par.users_IDS[u]
	else:
		x= getuserid(u)
	par.users_IDS[u]=x
	return x
def prompt_int(s,min,max):
	ok=False
	minmsg=''
	r=''
	while ok==False:
		r=raw_input(s)
		if r.isdigit():
			ok=True
			r=int(r)
		if r>max or r<min:
			ok=False

	return r
def addValidSession(s):
	if GET(s,'valid')!='True':
		return
	vs=GET(s,'email')

	for x in par.valid_sessions:
		vx=GET(x,'email')
		if vx==vs and vs != 'False':
			return
	par.valid_sessions.append(s)
def sessionWizard(s):
	print"""
1- Log out
2- Like some tweets
3- Follow some targets
4- Retweet
5- Change your name
6- edit bio

	"""
	v=prompt_int('',1,6)


def loginWizard():
	puid=prompt_not_empty(STX.Blue+'Your Login       ID :',1)
	pups=prompt_not_empty(STX.Blue+'Your Login Password :',6)
	se_=initSession(puid,pups)
	if GET(se_,'valid') and GET(se_,'username')!='False':
		prints(STX.Green+'\n Logged in successfully')
		prints('\n Your username is '+GET(se_,'username'))
		p=prompt_not_empty('\n Save this sesion (yes/no) : ')
		if p=='yes':
			addValidSession(se_)
			StoreValidSessions()
			prints(STX.Green+'\n Valid sessions = '+str(len(par.valid_sessions))+'\n')
		sessionWizard(p)
	else:
		prints(GET(se_,'lastmsg'))
	#if GET(se_,'valid')=='True':
def AutoMate_Mass_Report(usernames,count):
	ids=[]
	for x in usernames:
		i=Getcash_user_id(x)
		if i!= 'not found' and i not in ids:
			ids.append(i)
	r=0
	v=count/len(par.valid_sessions)
	if v <1:
		v=1
	for i2 in ids:
		prints(STX.yel+'Reporting '+i2)
		px=0
		for z in range(0,v+1):
			for s in par.valid_sessions:
				if r>= count:
					break
				px=px+1
				j=report(s,i2)
				if GET(j,'reported')=='True':
					r=r+1
				prints(STX.Green+'\n'+spaces(str(px),4)+' '+GET(j,'lastmsg') )
	prints('\n All reports Sent = '+str(r))
if __name__=='__main__':
	print STX.yel+"""
_________ _______  _______  _______  _______  _______  _______  _______ 
\__   __/(  ____ \(  ____ )(  ___  )(       )(       )(  ____ \(  ____ )
   ) (   | (    \/| (    )|| (   ) || () () || () () || (    \/| (    )|
   | |   | (_____ | (____)|| (___) || || || || || || || (__    | (____)|
   | |   (_____  )|  _____)|  ___  || |(_)| || |(_)| ||  __)   |     __)
   | |         ) || (      | (   ) || |   | || |   | || (      | (\ (   
   | |   /\____) || )      | )   ( || )   ( || )   ( || (____/\| ) \ \__
   )_(   \_______)|/       |/     \||/     \||/     \|(_______/|/   \__/
                                                                                                                                       
	===== Twitter Spamming tool  By Yasser Gersy =====
	==================================================
	"""+STX.White+STX.lin
	
	init_Me()
	_ac_=0
	executedonce=False

	while _ac_!='10':
		if executedonce:
			cont=raw_input('\n'+STX.havlin+STX.Blue+'\n Do you want to Continue ? (yes/no) : '+STX.magenta)
			if cont.lower().strip()=='no' or cont.lower().strip()=='n':
				break
		executedonce=True
		prints(STX.White+STX.lin+STX.Blue+"""
     Actions :"""+STX.White+"""
--------------
		"""+STX.brown+"""
[1 ] -  Get user id 				"""+STX.yel+"""	
[2 ] -  Mass Tweet          	    """+STX.brown+"""
[3 ] -  Like some tweets    		"""+STX.yel+"""
[4 ] -  Make retweets 				"""+STX.brown+"""
[5 ] -  Follow some targets 		"""+STX.yel+"""
[6 ] -  Reply on some tweets 		"""+STX.brown+"""
[7 ] -  Send DM 					"""+STX.yel+"""
[8 ] -  Spam some users				"""+STX.yel+"""
[9 ] -  Report some users			"""+STX.yel+"""
[10] -  Check current sessions.     """+STX.brown+"""
[11] -  Generate new sessions. 		"""+STX.yel+"""
[12] -  Filter expired sessions.    """+STX.brown+"""
[13] -  Fix Brocken sessions  		"""+STX.yel+"""
[14] -  Add New Session  			"""+STX.brown+"""
[15] -  Login 						"""+STX.yel+"""
[16] -  Show loginers 				"""+STX.yel+"""
[17] -  Follow yourselves 			"""+STX.yel+"""
[0 ] -  Exit  						"""+STX.brown+"""
		\n"""+STX.magenta)
		_ac_=raw_input(STX.Blue+'What is your choice? :'+STX.magenta)
		validnum=isValidNum(_ac_,0,17)
		prints(STX.White)
		while validnum==False:
			_ac_=raw_input(STX.Green+'invalid input insert number from (0:17) : '+STX.magenta)
			validnum=isValidNum(_ac_,0,17)
		App.action=returnAction(int(_ac_))
		can_interact=len(par.valid_sessions)>0
		prints('['+App.action+']'+STX.lin+'\n')
		if int(_ac_) < 9 and int(_ac_)>0 and len(par.valid_sessions) < 1:
		
		#	prints('\n no sessions found to perform this action :( , you need to generate or paste to sessions file ')
		#else:
			print('_ac_='+str(_ac_))
			print(len(par.valid_sessions))

		if App.action=='selffollow':
			idx=[]
			for s in par.valid_sessions:
				f=GET(s,'username')
				if f != 'False' and f not in idx:
					idx.append(f)
			AutoMate_Mass_Follow(idx)


		if App.action=='show':
			ct=0
			for x in par.valid_sessions:
				ct=ct+1
				prints('\n  '+spaces(str(ct),4)+'- '+spaces(GET(x,'username'),19)+'		'+GET(x,'email'))
		
		if App.action=='exit':
			Leav()
		elif App.action=='login':
			loginWizard()

		elif App.action=='add':
			prints('\n not implemented')#########################

		elif App.action=='fix':
			FixBrockenSessions()

		elif App.action=='filter':
		 	par.PINGOLDSES=True
			CheckCurrentSessions()

		elif App.action=='generate':
			Generate_sessions_fromAccounts()
			StoreValidSessions()
			
		
		elif App.action=='check':
			par.PINGOLDSES=True
			CheckCurrentSessions()
			some=''
			while  some!='yes' and some!='no':
				some=prompt_not_empty('\nDo you want to save changes? (yes/no)')
				if some.lower().strip()=='yes':			
					StoreValidSessions()
					break
				elif some=='no':
					break
		elif App.action=='report' and can_interact:
			u=prompt_not_empty(STX.Blue+'Enter Targets usernames , or links separated by comma if many : ')
		 	uids=SplitIDsUserInputToArray(u,1)
		 	con=prompt_int('How many Reports for each user ? : ',1,10000)
		 	AutoMate_Mass_Report(uids,con)
		elif App.action=='spam' and can_interact:
			u=prompt_not_empty(STX.Blue+'Enter Targets usernames , or links separated by comma if many : ')
		 	uids=SplitIDsUserInputToArray(u,1)
		 	twetsCount=prompt_int(STX.Blue+'How Many Tweets to interact with  ? :',1,102222)
		 	startindex=0
		 	vx=raw_input('If you want to start from certain tweet enter the index :')
		 	if vx.isdigit():
		 		startindex=int(vx)

		 	likespertweet=prompt_int(STX.Blue+'How Many likes for each tweet ? ',1,len(par.valid_sessions))

		 	AutoMate_Mass_Spam(uids,twetsCount,startindex,likespertweet)
		elif App.action=='dm' and can_interact:
			prints('\n not implements')#########################
		
		elif App.action=='reply' and can_interact:
			prints('\n not implemented')#########################
		
		elif App.action=='follow' and can_interact:
		 	u=prompt_not_empty(STX.Blue+'Enter Targets ids , or links separated by comma if many : ')
		 	uids=SplitIDsUserInputToArray(u,1)
		 	AutoMate_Mass_Follow(uids)

		elif App.action=='retweet' and can_interact:
			tw=prompt_not_empty(STX.Blue+'Enter tweet ids , or links separated by comma if many : ')
			tweets=SplitIDsUserInputToArray(tw,1)
			likespertweet=prompt_int(STX.Blue+'How Many retweets for each tweet ? ',1,len(par.valid_sessions))
			prints('\n ------Preparing to Retweet '+str(len(tweets))+' tweets\n')
			AutoMate_Post_Retweets(tweets,likespertweet)
		
		elif App.action=='like' and can_interact:
			tw=prompt_not_empty(STX.Blue+'Enter tweet ids , or links separated by comma if many : ',4)
			tweets=SplitIDsUserInputToArray(tw,1)
			likespertweet=prompt_int(STX.Blue+'How Many likes for each tweet ? ',1,len(par.valid_sessions))
			prints('\n -------Preparing to like '+str(len(tweets))+' tweets\n')
			AutoMate_Set_Likes(tweets,likespertweet)
		
		elif App.action=='tweet' and can_interact:
			tw=prompt_not_empty(STX.Blue+'Enter Tweet Text (max =138) : ',1,138)
			iv=prompt_int(STX.Blue+STX.Blue+'How Many Tweets ?',1,10000000)
			prints('\n --------Preparing to Tweet '+str(iv)+' \n')
			AutoMate_Mass_Tweet(tw,iv)
		
		elif App.action=='getid':
			tw=prompt_not_empty('Enter User ids , or links separated by comma if many : ')
			ids=SplitIDsUserInputToArray(tw,1)
			AutoMate_Get_UserIds(ids)



	Leav()

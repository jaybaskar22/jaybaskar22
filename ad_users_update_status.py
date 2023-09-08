import ldap
import sys
ldapconnectstring="ldap://<ADHostname>:389/"
binddn = "<DN of the service account>"
f=open('lastmodify.txt', 'w')
pw = "<pwd of service account>"
n=0
i=0
modyfydn=[]
basedn = "<basedn for search>"
statusattribute="useraccountcontrol"
searchAttribute = [statusattribute]
#filter to get all users that either start with 1bank or corp
searchFilter = "(&(|(cn=1bank*)(cn=corp*))(objectclass=user))"
#connect to LDAP
l=ldap.initialize(ldapconnectstring)
try:
    l.protocol_version = ldap.VERSION3
    l.simple_bind_s(binddn, pw) 
except ldap.INVALID_CREDENTIALS:
  print ("Your username or password is incorrect.")
  sys.exit(0)
except ldap.LDAPError as e:
  if type(e.message) == dict and e.message.has_key('desc'):
      print (e).message['desc']
  else: 
      print (e)
  sys.exit(0)

try:
   #Search AD for all users that start with '1bank' or 'corp'
   print('searching AD...')
   searchresult=l.search_s(basedn,ldap.SCOPE_SUBTREE, searchFilter,searchAttribute)
   print(searchresult)
   n=len(searchresult)
   print('Number of entries that are corp and 1bank:')
   print (n)
   listdns=[]
   listdns=searchresult[i]
   print (type(listdns[0]))
   print (listdns[0])
   #for every entry in result, do the following
   for modifydn, _ in searchresult:
     print('modifying the entry', modifydn)
     f.writelines(modifydn)
     f.write('\n')
     lmod=ldap.initialize(ldapconnectstring)
    #try:
     lmod.protocol_version = ldap.VERSION3
     lmod.simple_bind_s(binddn, pw) 

     try: 
            #actual modification - overwrite useraccount control to 66048 
            lmod.modify_s(modifydn,[(ldap.MOD_REPLACE,statusattribute,"66048".encode())])
            #lmod.unbind()
     except Exception as e:
             print (e)
         
except ldap.LDAPError as e:
  if type(e.message) == dict and e.message.has_key('desc'):
      print (e).message['desc']
  else: 
      print (e)
#  sys.exit(0)

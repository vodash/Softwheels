test=$(curl -i -s -X POST -H 'Content-Type: application/json' -d '{"username": "user1", "password": "abcxyz"}' aitai.nl:14164/auth | grep -Po '"access_token": *\K"[^"]*"') #match after access_token
test=${test#'"'} #remove prefix
test=${test%'"'} #remove suffix
echo $test
# curl aitai.nl:14164/users
curl -H "Authorization: JWT $test" aitai.nl:14164/users
curl -H "Authorization: JWT $test" aitai.nl:14164/protected

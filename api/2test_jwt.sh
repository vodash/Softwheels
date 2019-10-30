test=$(curl -i -s -X POST -H 'Content-Type: application/json' -d '{"username": "user1", "password": "aabcxyz"}' localhost:8000/auth | grep -Po '"access_token": *\K"[^"]*"') #match after access_token
test=${test#'"'} #remove prefix
test=${test%'"'} #remove suffix
echo $test
#curl -H "Authorization: JWT $test" localhost:8000/protected

test=$(curl -i -s -X POST -H 'Content-Type: application/json' -d '{"username": "user1", "password": "abcxyz"}' localhost:5000/auth | grep -Po '"access_token": *\K"[^"]*"') #match after access_token
test=${test#'"'} #remove prefix
test=${test%'"'} #remove suffix
curl -H "Authorization: JWT $test" localhost:5000/protected

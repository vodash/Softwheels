test=$(curl -i -s -X POST -H 'Content-Type: application/json' -d '{"username": "pietje@puk.pok", "password": "a"}' localhost:8000/auth | grep -Po '"access_token": *\K"[^"]*"') #match after access_token
test=${test#'"'} #remove prefix
test=${test%'"'} #remove suffix
# echo $test
# curl localhost:8000/users
curl -H "Authorization: JWT $test" localhost:8000/sleepData?start=2020-01-05&end=2020-01-08&id=5
# curl -H "Authorization: JWT $test" localhost:8000/protected

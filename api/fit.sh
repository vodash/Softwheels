test=$(curl -i -s -X POST -H 'Content-Type: application/x-www-form-urlencoded Authorization: Basic MjJCNVhYOmVjYzdiOWNmODk0ZjJhOTZiYzg4OWJkZjQxOTQwYTQ4' -d 'grant_type=refresh_token&refresh_token=2d6b36c0f6d42d483f032acd6181c0d43a0f0be4262f5ece1efcb52927d67c7a' https://api.fitbit.com/oauth2/token)
echo $test

# test=${test#'"'} #remove prefix
# test=${test%'"'} #remove suffix

# echo $test
# curl localhost:8000/users

# curl -H "Authorization: JWT $test" localhost:8000/fake

# curl -H "Authorization: JWT $test" localhost:8000/protected

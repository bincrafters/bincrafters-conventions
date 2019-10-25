body='{
"request": {
"branch":"cron"
}}'

curl -s -X POST \
   -H "Content-Type: application/json" \
   -H "Accept: application/json" \
   -H "Travis-API-Version: 3" \
   -H "Authorization: token ${TRAVIS_TOKEN}" \
   -d "$body" \
   https://api.travis-ci.com/repo/bincrafters%2Fbincrafters-conventions/requests

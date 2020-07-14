localStorage["url"] = 'http://localhost:4444/data2.json';
localStorage["api"] = 'http://localhost:4444/token.json';
localStorage["auth"] = '{"auth": "key1"}';

$.post(localStorage["api"], localStorage["auth"], function (jsonresponse) {
    localStorage["token"] = JSON.stringify(jsonresponse);
}, "json");


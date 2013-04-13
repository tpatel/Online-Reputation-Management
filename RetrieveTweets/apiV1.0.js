var http = require('http');

var fieldsToRemove = [
	'from_user_id',
	'geo',
	'profile_image_url',
	'profile_image_url_https',
	'source',
	'iso_language_code',
	'from_user_name',
	'id',
	'place',
	'to_user_id',
	'to_user_name',
	'in_reply_to_status_id'
];

var allTweets = [];

function handleResult(data, depth) {
	for(var i in data.results) {
		var c = data.results[i];
		for(var j in fieldsToRemove) {
			if(typeof c[fieldsToRemove[j]] != 'undefined')
				delete c[fieldsToRemove[j]];
		}
		allTweets.push(c);
	}
	//console.log(data.results);
	//console.log(data.next_page);
	searchTweets(data.next_page, handleResult, depth+1);
}

function searchTweets(paramsString, callback, depth) {
	if(!depth) depth = 0;
	if(depth < 3) { //Max pages
		(function(depth) {
			http.get("http://search.twitter.com/search.json" + paramsString, function(res) {
				res.setEncoding('utf8');
				var body = '';
				res.on('data', function(chunk) {
					body += chunk;
				});
				res.on('end', function() {
					body = JSON.parse(body);
					// Do stuff here
					handleResult(body, depth);
				});
			}).on('error', function(e) {
			  console.log("Got error: " + e.message);
			});
		})(depth);
	} else { //The end
		//console.log(allTweets);
		for(var i in allTweets) {
			console.log(allTweets[i]);
		}
	}
}

searchTweets("?q=microsoft&lang=en&rpp=1&result_type=recent", handleResult);

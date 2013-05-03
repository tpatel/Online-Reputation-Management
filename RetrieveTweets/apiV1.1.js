var twitter = require('ntwitter');

var twit = new twitter({
  consumer_key: 'LTRvazKgRtvH6Sq2atAkzw',
  consumer_secret: 'FxiuOQNmj9WjNgWF438t8XuriBFlMfbV8bnayeyttU',
  access_token_key: '569891699-JEbpQruL9XGMc3a6hJauLAqCZeKD3gWi0kt1sWX6',
  access_token_secret: 'Md4K7FnmYuTjY5WUnoryjSfzCq23MDhpYuPOL48Kw'
});

twit.verifyCredentials(function (err, data) {
});

var fieldsToRemove = [
	'id'
	,'in_reply_to_status_id'
	,'geo'
	,'coordinates'
	,'place'
	,'favorited'
	,'retweeted'
	,'in_reply_to_status_id'
	,'in_reply_to_user_id'
	,'user'
	,'entities'
	,'lang'
	,'source'
	,'metadata'
	,'truncated'
	,'possibly_sensitive'
	,'in_reply_to_screen_name'
	,'contributors'
	,'retweeted_status'
];

var allTweets = [];

function handleResult(data, depth) {
	for(var i in data.statuses) {
		var c = data.statuses[i];
		c.user_id_str = c.user.id_str;
		c.user_screen_name = c.user.screen_name;
		c.user_followers_count = c.user.followers_count;
		if(c.retweeted_status)
			 c.retweeted_status_id_str = c.retweeted_status.id_str;
		for(var j in fieldsToRemove) {
			if(typeof c[fieldsToRemove[j]] != 'undefined')
				delete c[fieldsToRemove[j]];
		}
		allTweets.push(c);
	}
	console.log(data.search_metadata.next_results, depth+1);
	searchTweets(data.search_metadata.next_results, depth+1);
}

function searchTweets(paramsString, depth) {
	if(!depth) depth = 0;
	if(paramsString && paramsString != 'undefined') { //Max pages
		(function(depth) {
			twit.search(paramsString, function(err, data) {
				if(err) {
					console.log(err);
					var fs = require('fs');
					fs.writeFile("./tweets.json", JSON.stringify(allTweets), function(err) {
						if(err) {
							console.log(err);
						} else {
							console.log("The file was saved!");
						}
					});
				}
				else {
					handleResult(data, depth);
				}
			});
		})(depth);
	} else { //The end
		//console.log(allTweets);
		/*for(var i in allTweets) {
			console.log(allTweets[i]);
		}*/
		var fs = require('fs');
		fs.writeFile("./tweets.json", JSON.stringify(allTweets), function(err) {
			if(err) {
				console.log(err);
			} else {
				console.log("The file was saved!");
			}
		});
	}
}

searchTweets('?q=coca cola&lang=en&count=100&result_type=recent');

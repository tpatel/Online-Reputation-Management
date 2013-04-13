var twitter = require('ntwitter');

var twit = new twitter({
  consumer_key: 'LTRvazKgRtvH6Sq2atAkzw',
  consumer_secret: 'FxiuOQNmj9WjNgWF438t8XuriBFlMfbV8bnayeyttU',
  access_token_key: '569891699-JEbpQruL9XGMc3a6hJauLAqCZeKD3gWi0kt1sWX6',
  access_token_secret: 'Md4K7FnmYuTjY5WUnoryjSfzCq23MDhpYuPOL48Kw'
});



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

function searchTweets(paramsString, depth) {
	if(!depth) depth = 0;
	if(depth < 1) { //Max pages
		(function(depth) {
			twit.search(paramsString, function(err, data) {
				if(err)
					console.log(err);
				else
					handleResult(data, depth);
			});
		})(depth);
	} else { //The end
		//console.log(allTweets);
		for(var i in allTweets) {
			console.log(allTweets[i]);
		}
	}
}

searchTweets('?q=microsoft&lang=en&count=1&result_type=popular');

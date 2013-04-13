var fs = require('fs');

//Extracts the tweets from all the json files
//Remplaces the \n by a space in the tweets
//Append the result in alltweets.txt

var sumTweets = 0;

fs.readdir('.', function(err, files) {
	if(err) throw err;
	for(var i in files) {
		if(files[i].search(/\.json/) != -1) {
			console.log(files[i]);
			
			var data = fs.readFileSync(files[i], 'utf8');
			var tweets = JSON.parse(data);
			console.log(tweets.length);
			sumTweets += tweets.length;
			for(var j in tweets) {
				fs.appendFileSync('alltweets.txt', tweets[j].id_str + ' ' + tweets[j].text.replace(/\n/g, ' ') + '\n');
			}
		}
	}
	
	var exec = require('child_process').exec, child;
	child = exec('wc -l alltweets.txt',
	  function (error, stdout, stderr) {
	  	var nbLines = parseInt(stdout.substr(0, stdout.search(' ')));
	  	if(nbLines == sumTweets) {
	  		console.log('Done.');
	  	} else {
	  		console.log('Please rm alltweets.txt before...');
	  	}
	});
});

we rarely create our own async function, an ugly way to write wrappers is this
```js
const fs=require("fs");

function myUglyAsync(callback){
	fs.readFile("file name", "utf-8", function(err,data){callback(data);} );
}

function callback(data){
	console.log(data);
}
```
better way is to use promises
```js
const fs=require("fs");

function myPrettyAsync(){
	return new Promise(function(WhenComplete){
			fs.readFile("file name", "utf-8", function(err,data){
												WhenComplete(data);
												}
			);
	});
}

function callback(data){console.log(data)};

myPrettyAsync().then(callback);
```
.then() doesnt block the thread
syntax
```js
new Promise(function(resolve){do somethign and then resolve()});
```
calling .then() on a new promise just adds the call back to the pipeline, which will execute when ever the control reaches to the resolve() in the promise

the following piece of code will print "hi"

```js
const fs = require("fs");

function myPrettyAsync() {
	return new Promise(function (WhenComplete) {
			console.log('hi')
			fs.readFile("harkirat.docx", "utf-8", function (err, data) {
				WhenComplete(data);
			}
		);
	});
}

function callback(data) { console.log(data) };

myPrettyAsync()//.then(callback);
```

just a pretty way to call async functions
under the hood it still uses the call stack the call back queue and the event stack
most of the time we only create a wrapper on a async function like on fetch
we pass the promise constructor an anonymous function taking a callback
and the callback takes a json object

that is the promise -> anonymous function -> callback -> json 

in the call back we define we can only pass one thing from the promise so if we want to pass multiple things we need to pass an object or list

```js
function myPrettyAsync() {
    return new Promise(function (resolve) {
        console.log('hi')
        let a = "you called .then()";
        let idx = 5;
        for (let i = 0; i < 10; i++) {
            if (i == 5) {
                resolve({ data: a, index: idx });
            } else {
                console.log(i);
            }
        }
    });
}

function callback(result) {
    console.log(result.data);
    console.log(result.index);
}

myPrettyAsync().then(callback);
```

the above code prints 0 1 2 3 4 NOT 5 6 7 8 9 then prints "you called .then()" and then prints 5 

"you called .then()" and then 5 are not printed if we dont do .then

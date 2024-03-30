[[1. Javascript high level, dates and json]] 
[[2. Async]] 
[[3. Promises]]
[[4. Conversions in JS]]
1. how to make JS use multiple children processes?  
	1. cluster module
2. what are two other alert("") like browser APIs, what do they return? 
	1. alert("")
	2. confirm("")
	3. prompt("")
3. what is the syntax for the coalesce operator, what is it used for ?
	1. name ?? "no name"
4. what is optional chaining in JS? write some syntaxes?
	1. let a=[]; 
	2. a[4]?.property
	3. a.?[0]
5. what are the two kinds of foreach loops, what do they iterate over?
	1. in, indexes
	3. of, elements
6. write the syntax for classes constructor and static variables.
	```js
	class animal{
		static variable="static variable this is";
		constructor(name, legCount){
			this.name=name;
			this.legcount=legCount;
		}
	}
	```
7. how many data types in JS?
	1. 3 strings, numbers, booleans
8. how to perform string interpolation
	1. `${variable} is interpoled`
9. what are static methods and how are the accessed?
	```js
	class Animal{
		static staticMethod(){
			return true;
		}
	}
	
	Animal.staticMethod();
	```
10. how to create dates? what are some useful getters and setters for the date properties. what do they return?
	```js
	let now=new Date();
	now.getMonth();
	now.getDate();
	now.getYear();
	now.getFullYear();
	now.getHours();
	now.getMinutes();
	now.getSeconds();
	now.getTime();
	```
11. how to convert object to string using JSON class and parse the string to JSON objects
	```js
	const user="{"name":"harkirat","age":18}";
	const User=JSON.parse(user);
	console.log(User.name);//User["name"]
	console.log(JSON.stringify(User));
	```
12. how to use positive and negative infinities in JS
	```js
	Number.NEGATIVE_INFINITY;
	Number.POSITIVE_INFINITY;
	```
13. how to convert number to string, to decimal string and how to use number max and min values
	```js
	let val=5;
	val.toString();
	let val=new Number(100);
	val.toFixed();//100.00
	Number.MIN_VALUE;
	Number.MAX_VALUE;
	```
14. what are some important  functions of the Math library in JS
	```js
	Math.max(1,2,3,4,5,6,6);
	Math.min();
	Math.abs();
	Math.floor();
	Math.ceil();
	Math.random();
	```
15. how to get random values between two values
	```js
	let max=20;
	let min=10;
	Math.floor(Math.random() * (max-min+1))+min;
	```
16. when we await a promise what do we get in return?
	1. we get what ever the promise resolves to 
17. explain the promise syntax 
	1. promise takes a function as an parameter
	2. that functions takes resolve as a parameter
	3. resolve is a function which can take anything as a parameter
	4. .then() takes a callback function as an argument
	5. that callback function takes some parameter
	6. the parameter of the callback is what ever the promise function called the resolve function with int step 3
		```js
		function myPrettyAsync(){
			return new Promise(function(resolve){
					fs.readFile("file name", "utf-8", function(err,data){
														resolve(data);
														}
					);
			});
		}
		
		function callback(data){console.log(data)};
		
		myPrettyAsync().then(callback);
		```
	7. the function inside the promise takes reject as an optional parameter
	8. what ever call back is passed into the .catch() is called on with the reject() parameter
	9. what ever callback is passed into the .then() is called on with the resolve() parameter
	```js
	new Promise(function(resolve,reject){do somethign and then resolve()});
	```
18. does calling .then on a promise block thread?, what are three promise states?
	1. the three promise states are
		1. pending
		2. fulfilled
		3. rejected
	2. it doesnt block the main thread 
	3. it only registers callbacks to be called when the promise resolves or rejects
	4. calling .then only adds the call back to the pipeline which will execute when ever the control reaches to the resolve in the promise.
	5. it will actually go into the callback queue and be picked up by the main thread when ever the thread is idle
	6. even if we dont provide a callback to the promise the code before the resolve is still executed 
19. how to run multiple promises together? call .then on multiple promises together
	1. Promise.all
	```js
	Promise.all([promise1,promise2,promise3]).then((List_of_resolves)=>{});
	```
	2. in the .then() the callback in this case would get all the resolutions of promises in a list
20. what is promise chaining?
	1. when the callback in the .then returns another promise in that case we can keep on .thening 
21. at what level is the await keyword blocking?
	1. the await keyword is thread blocking at the function level
	2. if we have an async function and i awaited some promise inside of it, the async function goes into the micro task queue.
	3. the async function is picked up when the thread is idle.
	4. the thread continues from where the async function was called
	5. in the following code hi is printed before the object is printed because the await keyword is thread blocking only at the function level.
	```js
	function returns_promise_object() {
	    return new Promise(function (resolve) {
	        setTimeout(function () {
	            resolve({ "prop1": "val1", "prop2": "val2" });
	        }, 10000);
	    })
	}
	async function main() {
	    let obj = await returns_promise_object();
	    console.log(obj);
	}
	
	main();
	
	setTimeout(function () {
	    console.log("hi");
	}, 5000);
	```
22. how can we check type of some object
	```js
	console.log(typeof a);
	```
23. what does Number() convert the following to? 
	1. "33abc",  Number('33abc')
		1. Nan
	2. null
		1. 0
	3. undefined
		1. Nan
	4. true
		1. 1
24. what does Boolean() convert the following to?
	1. Boolean(1)
		1. true
	2. Boolean("")
		1. false
	3. Boolean("somthing")
		1. true
25. what about String?
	1. String(33)
		1. "33"
26. what kind of variables can be exported using "export const" ?
	1. serializable
27. why cant mongoose models be exported with the export const syntax?
	1. they are not serializable
	2. they are not immutable
	3. if we export as const we will get different copies of the model in different places leading to inaccurate database queries


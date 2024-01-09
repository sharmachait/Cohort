just a pretty way to call async functions
under the hood it still uses the call stack the call back queue and the event stack
most of the time we only create a wrapper on a async function like on fetch
we pass the promise constructor an anonymous function taking a callback
and the callback takes a json object

that is the promise -> anonymous function -> callback -> json 

in the call back we define we can only pass one thing from the promise so if we want to pass multiple things we need to pass an object or list

```
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

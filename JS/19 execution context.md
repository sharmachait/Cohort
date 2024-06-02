basically like the closure but of the entire code that is executing
execution contexts are what is pushed on to the call stack
its the entire environment the code is being executed in
![[Pasted image 20240601195714.png]]
when ever we run a script a global execution context is created
	memory is allocated for functions and variables
	and the context is pushed on to the stack

the global execution context compirses of 
1. realm - the isolated environment our code is executing in, consisting of all the APIs we use, all the variables we create using the var keyword the functions 
	1. const and let are hoisted and memory is allocated but value is not initialized until the execution stage
	2. functions are initialized even before the execution stage
2. lexical environment - 
3. variable environment - 
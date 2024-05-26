### process.argv

The `process.argv` property returns an array containing the command-line arguments passed when the Node.js process was launched. The first element will be [`process.execPath`]  The second element will be the path to the JavaScript file being executed. The remaining elements will be any additional command-line arguments.

### .git folder internals
[What is in that .git directory? (meain.io)](https://blog.meain.io/2023/what-is-in-dot-git/)

### git objects
- Blobs 
    - These are used to store file data.
    - Blobs only store the contents of a file, not its name or permissions.
    - Each Git Blob is stored as a separate file in the `.git/objects` directory. The file contains a header and the contents of the blob object, compressed using Zlib.
    - The format of a blob object file looks like this (after Zlib decompression):
```
  blob <size>\0<content>
```
- `<size>` is the size of the content (in bytes)
- `\0` is a null byte
- `<content>` is the actual content of the file
    For example, if the contents of a file are `hello world`, the blob object file would look like this (after Zlib decompression):
```
  blob 11\0hello world
```
- Trees 
    - These are used to store directory structures.
    - The information stored can include things like what files/directories are in a tree, their names and permissions.
- Commits 
    - These are used to store commit data.
    - The information stored can include things like the commit message, author, committer, parent commit(s) and more.

### git plumbing commands
1. git cat-file 
```bash
git cat-file -t 4c5b58f323d7b459664b5d3fb9587048bb0296deblob$
git cat-file -s 4c5b58f323d7b459664b5d3fb9587048bb0296de9$ 
git cat-file -p 4c5b58f323d7b459664b5d3fb9587048bb0296demeain.io
```
	-t for type
	-s for size
	-p for content

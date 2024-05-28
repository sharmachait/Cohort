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
### git cat-file
```bash
git cat-file -t 4c5b58f323d7b459664b5d3fb9587048bb0296deblob$
git cat-file -s 4c5b58f323d7b459664b5d3fb9587048bb0296de9$ 
git cat-file -p 4c5b58f323d7b459664b5d3fb9587048bb0296demeain.io
```
	-t for type
	-s for size
	-p for content
### hashing and zlib compression
calculating the SHA1
```ts
import crypto from 'crypto';  
  
export function calculateSha1(buffer: Buffer): string {  
  const hash = crypto.createHash('sha1');  
  hash.update(buffer);  
  return hash.digest('hex');  
}
```
zlib Compression and Rarefaction
```ts
import zlib from 'zlib';
const bufferToWrite = fs.readFileSync(compressedFilePath);
const compressedBuffer = zlib.deflateSync(bufferToWrite);
const buffer = zlib.unzipSync(compressedBuffer);
```
### git ls-tree command
used to inspect tree object
a tree object is made up of entries
each entry includes
- a sha hash that point to a blob or tree object
	- if the entry is a file it points to a blob
	- if the entry is a dir it points to another tree object
- name of the file/directory
- mode of the file/directory
	- mode is basically different kinds of permissions 
	- for files we have three options
		- `100644` (regular file)
		- `100755` (executable file)
		- `120000` (symbolic link)
```ts
export function getFileMode(stats: fs.Stats): string {  
  if (stats.isSymbolicLink()) {  
    return '120000'; // symbolic link  
  } else if (stats.mode & 0o111) {  
    return '100755'; // executable file  
  } else {  
    return '100644'; // regular file  
  }  
}
getFileMode(fs.statSync(filePath));
```
	- for dirs the value is `40000`

- For example, if you had a directory structure like this:
```
  your_repo/
    - file1
    - dir1/
      - file_in_dir_1
      - file_in_dir_2
    - dir2/
      - file_in_dir_3
```
The entries in the tree object would look like this:, this is also the output of the git ls-tree command
```
  40000 dir1 <tree_sha_1>
  40000 dir2 <tree_sha_2>
  100644 file1 <blob_sha_1>
```
dir1 and dir 2 are tree objects as well and if we inspect them we will find the files in them
the output is alphabetically sorted
> gist ls-tree --name-only <tree_sha>

this outputs only the name of the files

git cat-file -p tree_sha
the format of the tree object file is like so
```
tree <size>\0
<mode> <name>\0<sha>
<mode> <name>\0<sha>
```
the actual out put doesnt have a new line character

### git write-tree
creates a tree object from the current state of the staging area
outputs the sha of the tree object
iterate over the folder structure in the staging area
- if the entry is a file create a blob object and record its sha
- if directory create a tree object and record its sha
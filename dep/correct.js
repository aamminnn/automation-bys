constfs=require('fs'); constunzip=require('unzip');
fs.createReadStream('archive.zip') .pipe(unzip.Parse()) .on('entry',entry=>{
constfileName=entry.path;
// BAD: This could write any file on the filesystem. entry.pipe(fs.createWriteStream(fileName));
});
chr = process.argv[2]
start = process.argv[3]
stop = process.argv[4]

console.log(chr + "\t"+ start +"\t" + stop)

fs = require('fs')
const { TabixIndexedFile } = require("@gmod/tabix");
const VCF = require("@gmod/vcf");
const {RemoteFile} = require('generic-filehandle')
const remoteTbiIndexed = new TabixIndexedFile({
  filehandle: new RemoteFile('https://appdev.kbase.us/dynserv/b8fedfd6d8a1fc10372bcbad4f152b4b6d85507b.VariationFileServ/shock/a293a557-47b3-4fcc-8bef-d2049ad6368a'),
  tbiFilehandle: new RemoteFile('https://appdev.kbase.us/dynserv/b8fedfd6d8a1fc10372bcbad4f152b4b6d85507b.VariationFileServ/shock/f19936ff-6f66-4a44-831f-1bfcdc6e88c4') // can also be csiFilehandle
})
const lines = []
async function getvar(){
await remoteTbiIndexed.getLines(chr, start, stop, (line, fileOffset) => lines.push(line))


fs.writeFile('data.txt', lines, function (err,data) {
  if (err) {
    return console.log(err);
  }
});

const headerText = await remoteTbiIndexed.getHeader()
const tbiVCFParser = new VCF({ header: headerText })

fs.writeFile('sample_names.txt', tbiVCFParser.samples, function (err,data) {
  if (err) {
    return console.log(err);
  }
  //console.log(tbiVCFParser.samples);
});
}

getvar()



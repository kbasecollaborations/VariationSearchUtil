chr = process.argv[2]
start = process.argv[3]
stop = process.argv[4]
url_template = process.argv[5]
tbi_url_template = process.argv[6]
token=process.argv[7]

const fetch = require("node-fetch")
const { TabixIndexedFile } = require("@gmod/tabix");
const VCF = require("@gmod/vcf");
const {RemoteFile} = require('generic-filehandle')

kbase_session_token = 'kbase_session=' + token
var headers ={'Cookie': kbase_session_token}

const remoteTbiIndexed = new TabixIndexedFile({
  filehandle: new RemoteFile(url_template, {
    fetch,
    headers: headers
  }),
  tbiFilehandle: new RemoteFile(tbi_url_template, {
    fetch,
    headers: headers
  })
});

start=Number(start)
stop = Number(stop)

const lines = []
async function getvar(){
await remoteTbiIndexed.getLines(chr, start, stop,  (line, fileOffset) => lines.push(line))

return console.log(lines.join("\n"));

}

getvar()



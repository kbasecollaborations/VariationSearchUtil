#node get_variants.js Chr01 51 52 https://appdev.kbase.us/dynserv/b8fedfd6d8a1fc10372bcbad4f152b4b6d85507b.VariationFileServ/shock/a293a557-47b3-4fcc-8bef-d2049ad6368a https://appdev.kbase.us/dynserv/b8fedfd6d8a1fc10372bcbad4f152b4b6d85507b.VariationFileServ/shock/f19936ff-6f66-4a44-831f-1bfcdc6e88c4


#node get_variants.js Chr01 51 52 \
#https://appdev.kbase.us:443/dynserv/682063b283a644bbcb27ca7a49919b8093608d05.VariationFileServ/shock/b501e1e4-6c68-4d1f-aefc-b85583c97f40 \
#https://appdev.kbase.us:443/dynserv/682063b283a644bbcb27ca7a49919b8093608d05.VariationFileServ/shock/b497f1bd-1518-4b30-b97c-4b9645724c02

#node get_variants.js Chr01 51 52 \
#http://127.0.0.1:5000/shock/b501e1e4-6c68-4d1f-aefc-b85583c97f40 \
#http://127.0.0.1:5000/shock/b497f1bd-1518-4b30-b97c-4b9645724c02


token="5UOWDLRRQCVHLDTO6O65K3FHBYZ3I4GJ"

url="http://127.0.0.1:5000/jbrowse_query/appdev.kbase.us/services/shock-api/node/"

url="https://appdev.kbase.us/dynserv/bc4028183a9f3b118815b5bfd89bec13e4fe1463.VariationFileServ/jbrowse_query/appdev.kbase.us/services/shock-api/node/"
vcf=${url}ecc48e31-4d63-41b2-9ca2-3945e22165a9
tbi=${url}2f8e5be2-3460-4c53-8449-a9cd61c0f989

vcf=${url}b501e1e4-6c68-4d1f-aefc-b85583c97f40
tbi=${url}b497f1bd-1518-4b30-b97c-4b9645724c02

#node --trace-warnings  get_variants.js Chr01 51 52 \
#  $vcf $tbi $token

echo "node --trace-warnings  get_variants.js Chr01 51 52"
echo $vcf
echo $tbi
echo $token


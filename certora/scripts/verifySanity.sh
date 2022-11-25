contractPath=${1}
project=${2}
contract=`echo ${1} | perl -0777 -pe 's/.*\///g' | awk -F'.' '{print $1}'`
echo $contractPath
echo $contract
set -x
certoraRun ${contractPath} \
  --verify ${contract}:certora/specs/sanity.spec \
  --solc solc8.10 \
  --settings -t=300 \
  --staging --msg "${project} ${contract} Sanity" --rule sanity

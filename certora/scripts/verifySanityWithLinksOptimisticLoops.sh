certoraRun certora/munged/protocol/tokenization/AToken.sol certora/munged/protocol/pool/Pool.sol \
  --verify AToken:specs/sanity.spec \
  --link AToken:_pool=Pool \
  --settings -t=300 \
  --optimistic_loop \
  --staging --msg "Aave AToken Sanity optimistic loops and link" 

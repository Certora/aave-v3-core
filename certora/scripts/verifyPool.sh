certoraRun certora/munged/protocol/pool/Pool.sol \
              certora/harness/ATokenHarness.sol \
              certora/harness/StableDebtTokenHarness.sol \
              certora/harness/SimpleERC20.sol \
              certora/munged/protocol/tokenization/VariableDebtToken.sol \
              certora/harness/SymbolicPriceOracle.sol \
  --verify Pool:certora/specs/pool.spec \
  --solc solc8.10 --optimistic_loop \
  --staging \
  --settings -t=600 --settings -superOptimisticReturnsize=true \
#   --link ATokenHarness:POOL=Pool \
  --rule_sanity \
  --msg "Pool"

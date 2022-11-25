certoraRun certora/harness/SimpleERC20.sol certora/harness/ATokenHarness.sol \
    --verify ATokenHarness:certora/specs/AToken.spec \
    --solc solc8.10 \
    --msg "aToken spec - all " \
    --link ATokenHarness:_underlyingAsset=SimpleERC20 \
    --optimistic_loop \
    --staging \
    --settings -enableGhostGrounding=true
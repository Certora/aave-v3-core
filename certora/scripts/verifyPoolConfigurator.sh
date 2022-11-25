certoraRun certora/harness/PoolConfiguratorHarness.sol certora/harness/PoolHarnessForConfigurator.sol \
    --verify PoolConfiguratorHarness:certora/specs/PoolConfigurator.spec \
    --solc solc8.10 \
    --msg "PoolConfigurator spec on harness" \
    --link PoolConfiguratorHarness:_pool=PoolHarnessForConfigurator \
    --optimistic_loop \
    --staging \
    --settings -useBitVectorTheory
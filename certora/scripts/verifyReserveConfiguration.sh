certoraRun certora/harness/ReserveConfigurationHarness.sol \
    --verify ReserveConfigurationHarness:certora/specs/ReserveConfiguration.spec \
    --solc solc8.10 \
    --settings -useBitVectorTheory \
    --staging \
    --msg "ReserveConfiguration" \
    --rule_sanity \
    --optimistic_loop 
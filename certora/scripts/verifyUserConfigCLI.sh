certoraRun certora/harness/UserConfigurationHarness.sol \
    --verify UserConfigurationHarness:certora/specs/UserConfiguration.spec \
    --solc solc8.10 \
    --settings -useBitVectorTheory \
    --staging \
    --msg "UserConfiguration spec rule = isolated" \
    --optimistic_loop \
    --rule isolated 
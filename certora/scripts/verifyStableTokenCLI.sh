certoraRun certora/harness/StableDebtTokenHarness.sol:StableDebtTokenHarness \
    --verify StableDebtTokenHarness:certora/specs/StableDebtToken.spec \
    --solc solc8.10 \
    --settings -assumeUnwindCond,-b=4 \
    --rule_sanity \
    --cache StableToken --staging
    --msg "stableTokenCLI"
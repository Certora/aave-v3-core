certoraRun contracts/protocol/tokenization/VariableDebtToken.sol \
    --verify VariableDebtToken:certora/specs/VariableDebtToken.spec \
    --solc solc8.10 \
    --optimistic_loop \
    --staging \
    --msg "variable debt token" 
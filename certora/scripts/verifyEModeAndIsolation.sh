certoraRun contracts/protocol/pool/Pool.sol \
    --verify Pool:certora/specs/eModeAndIsolation.spec \
    --solc solc8.10 \
    --staging \
    --msg "eMode and isolation spec"
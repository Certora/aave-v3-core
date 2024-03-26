CMN=""



echo "******** Running:  1 ***************"
certoraRun $CMN certora/conf/AToken.conf \
           --msg "1: AToken.conf"

echo "******** Running:  2 ***************"
certoraRun $CMN certora/conf/Pool.conf \
           --msg "2: Pool.conf"

echo "******** Running:  3 ***************"
certoraRun $CMN certora/conf/ReserveConfiguration.conf \
           --msg "3: ReserveConfiguration.conf"

echo "******** Running:  4 ***************"
certoraRun $CMN certora/conf/StableTokenCLI.conf \
           --msg "4: StableTokenCLI.conf"

echo "******** Running:  5 ***************"
certoraRun $CMN certora/conf/UserConfigCLI.conf \
           --msg "5: UserConfigCLI.conf"

echo "******** Running:  6 ***************"
certoraRun $CMN certora/conf/VariableTokenCLI.conf \
           --msg "6: VariableTokenCLI.conf"


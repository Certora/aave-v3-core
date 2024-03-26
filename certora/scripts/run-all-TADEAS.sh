CMN=""



echo "******** Running:  1 ***************"
certoraRun $CMN certora/conf/NEW-pool-simple-properties.conf \
           --rule cannotDepositInInactiveReserve \
           --msg "1: NEW :: cannotDepositInInactiveReserve"

echo "******** Running:  2 ***************"
certoraRun $CMN certora/conf/NEW-pool-simple-properties.conf \
           --rule cannotDepositInFrozenReserve \
           --msg "2: NEW :: cannotDepositInFrozenReserve"

echo "******** Running:  3 ***************"
certoraRun $CMN certora/conf/NEW-pool-simple-properties.conf \
           --rule cannotDepositZeroAmount \
           --msg "3: NEW :: cannotDepositZeroAmount"

echo "******** Running:  4 ***************"
certoraRun $CMN certora/conf/NEW-pool-simple-properties.conf \
           --rule cannotWithdrawZeroAmount \
           --msg "4: NEW :: cannotWithdrawZeroAmount"

echo "******** Running:  5 ***************"
certoraRun $CMN certora/conf/NEW-pool-simple-properties.conf \
           --rule cannotWithdrawFromInactiveReserve \
           --msg "5: NEW :: cannotWithdrawFromInactiveReserve"

echo "******** Running:  6 ***************"
certoraRun $CMN certora/conf/NEW-pool-simple-properties.conf \
           --rule cannotBorrowZeroAmount \
           --msg "6: NEW :: cannotBorrowZeroAmount"

echo "******** Running:  7 ***************"
certoraRun $CMN certora/conf/NEW-pool-simple-properties.conf \
           --rule cannotBorrowOnInactiveReserve \
           --msg "7: NEW :: cannotBorrowOnInactiveReserve"

echo "******** Running:  8 ***************"
certoraRun $CMN certora/conf/NEW-pool-simple-properties.conf \
           --rule cannotBorrowOnReserveDisabledForBorrowing \
           --msg "8: NEW :: cannotBorrowOnReserveDisabledForBorrowing"

echo "******** Running:  9 ***************"
certoraRun $CMN certora/conf/NEW-pool-simple-properties.conf \
           --rule cannotBorrowOnFrozenReserve \
           --msg "9: NEW :: cannotBorrowOnFrozenReserve"


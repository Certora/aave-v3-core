import "pool_no-summarizations.spec";



// @title When a user deposits X amount of an asset, the protocol balance on that asset is increased by X.
rule depositIncreasesProtocolBalance(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;
    mathint total_supply_before = _aToken.totalSupply(e);

    deposit(e, asset, amount, onBehalfOf, referralCode);
    mathint total_supply_after = _aToken.totalSupply(e);
    assert amount > 0 => total_supply_after > total_supply_before;
    assert total_supply_after - total_supply_before == to_mathint(amount);
}

// @title User cannot withdraw more than their balance.
// TODO: Fix false violation:
// https://prover.certora.com/output/40577/8f288e4728444645ae8ff55903d6e94d/?anonymousKey=82088b4c3515661c9184cbe74081551e24216245
rule withdrawMoreThanBalanceImpossible(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;
    mathint balance_before = aTokenBalanceOf(e, e.msg.sender);
    mathint underlying_balance_before = _underlyingAsset.balanceOf(e, to);
    mathint underlying_total_before = _underlyingAsset.balanceOf(e, _aToken); //PoolHarness

    require asset != to;
    require to != _aToken;

    withdraw(e, asset, amount, to);

    mathint balance_after = aTokenBalanceOf(e, e.msg.sender);
    mathint underlying_balance_after = _underlyingAsset.balanceOf(e, to);
    mathint underlying_total_after = _underlyingAsset.balanceOf(e, _aToken); //PoolHarness

    assert balance_after < balance_before;
    assert underlying_balance_before >= to_mathint(amount);
    assert underlying_total_before >= to_mathint(amount);
}

// @title After withdraw, the withdrawn amount is subtracted from the user aToken balance
// TODO: use different balances. See:
// https://prover.certora.com/output/40577/836d9b39c113460a8dab6530a52ceb6c/?anonymousKey=6da278a0a4287899be2df3d7d03faacdd6b2dbd0
// https://prover.certora.com/output/40577/c5c10712244240ef8a2f6902bbd1f120/?anonymousKey=6ecbbcd553c303d83fded29b9a57a50f2e24f8f7
rule withdrawUpdatesBalances(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;
    mathint balance_before = aTokenBalanceOf(e, e.msg.sender);

    require asset != to;
    require to != _aToken;

    withdraw(e, asset, amount, to);

    mathint balance_after = aTokenBalanceOf(e, e.msg.sender);

    assert balance_before - balance_after == to_mathint(amount);
}

// @title Rule for studing how does the normalized_income changes
rule normalized_income_changes_with(env e, method f) filtered {
    f -> !f.isView &&
    f.selector != sig:initReserve(address,address, address, address, address).selector &&
    f.selector != sig:dropReserve(address).selector &&
    f.selector != sig:mintToTreasury(address[]).selector &&
    // f.selector != sig:supplyWithPermit(address,uint256,address,uint16,uint256,uint8,bytes32,bytes32).selector &&
    f.selector != sig:supply(address,uint256,address,uint16).selector &&
    f.selector != sig:rebalanceStableBorrowRate(address,address).selector &&
    f.selector != sig:swapBorrowRateMode(address,uint256).selector &&
    f.selector != sig:backUnbacked(address,uint256,uint256).selector &&
    f.selector != sig:flashLoan(address,address[],uint256[],uint256[],address,bytes,uint16).selector &&
    f.selector != sig:repay(address,uint256,uint256,address).selector &&
    f.selector != sig:withdraw(address,uint256,address).selector &&
    f.selector != sig:rescueTokens(address,address,uint256).selector &&
    f.selector != sig:mintUnbacked(address,uint256,address,uint16).selector &&
    f.selector != sig:flashLoanSimple(address,address,uint256,bytes,uint16).selector &&
    f.selector != sig:deposit(address,uint256,address,uint16).selector // &&
    // f.selector != sig:.selector &&
    // f.selector != sig:.selector &&
} {
    address asset;
    mathint normalized_income_before = getReserveNormalizedIncome(e, asset);
    calldataarg args;

    f(e, args);

    mathint normalized_income_after = getReserveNormalizedIncome(e, asset);
    assert normalized_income_before == normalized_income_after;
}

// @title Impossible to borrow making HF smaller than 1
rule cannotBorrowWithHealthFactorLessThanOne(env e) {
    address asset;
    uint256 amount;
    uint256 interestRateMode;
    uint16 referralCode;
    address onBehalfOf;

	uint256 healthFactor;

	// DataTypes.ReserveData data = getReserveData(e, asset);
	// address[] reservesList = getReservesList(e);

	// _, _, _, _, healthFactor, _ = calculateUserAccountData(data, reservesList, eModeCategories, params);

	_, _, _, _, healthFactor, _ = getUserAccountData(e, onBehalfOf);

    borrow(e, asset, amount, interestRateMode, referralCode, onBehalfOf);

	assert healthFactor > RAY();
}

// @title Rule for studing how does the total AToken supply changes
// https://prover.certora.com/output/40577/a0cc6689742649a799e8c4814ce9267d/?anonymousKey=56ae6a1b357d6fe96c95a712345e68f9d028c113
rule totalChangesOnlyWithInitDropSupplyMint(env e, method f) filtered{
    f -> !f.isView &&
    f.selector != sig:initReserve(address,address, address, address, address).selector &&
    f.selector != sig:dropReserve(address).selector &&
    f.selector != sig:mintToTreasury(address[]).selector &&
    f.selector != sig:supplyWithPermit(address,uint256,address,uint16,uint256,uint8,bytes32,bytes32).selector &&
    f.selector != sig:supply(address,uint256,address,uint16).selector &&
    f.selector != sig:repayWithPermit(address,uint256,uint256,address,uint256,uint8,bytes32,bytes32).selector &&
    f.selector != sig:swapBorrowRateMode(address,uint256).selector &&
    //f.selector != sig:flashLoan(address,address[],uint256[],uint256[],address,bytes,uint16).selector &&
    f.selector != sig:repay(address,uint256,uint256,address).selector &&
    f.selector != sig:deposit(address,uint256,address,uint16).selector &&
    f.selector != sig:flashLoanSimple(address,address,uint256,bytes,uint16).selector &&
    f.selector != sig:borrow(address,uint256,uint256,uint16,address).selector &&
    f.selector != sig:mintUnbacked(address,uint256,address,uint16).selector
} {
    address user;
    calldataarg args;
    mathint totalSupplyBefore = getTotalATokenSupply(e, user);

    f(e, args);

    mathint totalSupplyAfter = getTotalATokenSupply(e, user);

    assert totalSupplyBefore == totalSupplyAfter; 
}

// @title After withdraw, the withdrawn amount is subtracted from the user aToken balance.
// WIP
// Failing here: https://prover.certora.com/output/40577/836d9b39c113460a8dab6530a52ceb6c/?anonymousKey=6da278a0a4287899be2df3d7d03faacdd6b2dbd0
rule withdrawUpdatesBalances(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;
    mathint balance_before = aTokenBalanceOf(e, e.msg.sender);

    require asset != to;
    require to != _aToken;

    withdraw(e, asset, amount, to);

    mathint balance_after = aTokenBalanceOf(e, e.msg.sender);

    assert balance_before - balance_after == to_mathint(amount);
}

// @title P20: It's not possible to borrow more than the available liquidity in the reserve.
// @dev: Aave works on similar invariant so this one is obsolete
// invariant cannotBorrowMoreThanReserve(env e)
//     to_mathint(_aToken.scaledTotalSupply(e)) >= _stable.debtTotalSupply(e) + _variable.debtTotalSupply(e);


// @title P21: It's not possible to borrow at a stable rate in a reserve where the stable rate is not enabled.
// @dev: This rule has been proved but now it fails after diffterent configurations were merged.
// Passing: https://prover.certora.com/output/31688/566a7085f86e46db86aba7b76cc8e565/?anonymousKey=10ba8cd538750242841a1b225053d4157fee11c4
// Failing in the current setup: https://prover.certora.com/output/31688/44e15483753a4ca28b620fc4180678cb/?anonymousKey=81bad1c54c7f098635d5e9cbca93cf2be07f2449
rule borrowStableRateOnlyWhenEnabled(env e) {
    address asset;
    uint256 amount;
    uint256 interestRateMode;
    uint16 referralCode;
    address onBehalfOf;

    borrow@withrevert(e, asset, amount, getStableRateConstant(e), referralCode, onBehalfOf);
    bool borrowRevert = lastReverted;

    assert !isStableRateEnabled(e, asset) => borrowRevert;
}

// @title P22: It's not possible to borrow at a stable rate more than the percentage over the available liquidity defined by the parameters returned by getMaxStableRateBorrowSizePercent()
// link: https://prover.certora.com/output/31688/23986e61346846878965d305995df7bd/?anonymousKey=2bfc3b014fec3129bc227dfe59dd494ba867bbee
rule notBorrowMoreThanMaxStableRate(env e) {
    address asset;
    uint256 amount;
    uint16 referralCode;
    address onBehalfOf;

    uint256 maxStableRate = MAX_STABLE_RATE_BORROW_SIZE_PERCENT(e);
    uint256 availableLiquidity = getAvailableLiquidity(e, asset);
    uint256 maxLoanSizeStable = require_uint256(require_uint256(require_uint256(availableLiquidity*maxStableRate)+5000)/10000);
    borrow@withrevert(e, asset, amount, getStableRateConstant(e), referralCode, onBehalfOf);

    assert (amount > maxLoanSizeStable) => lastReverted;
}

// @title P24: A borrower can only borrow up to the amount which would set the HF to 1 (alternatively written, after a borrow action the HF of the borrower is always > 1)
// link: https://prover.certora.com/output/31688/25d2c63198d34de6af5fcd404085208e/?anonymousKey=957accecb954a52bdde687f2b2c2fe182efaf902
rule lowHealthFactor(env e) {
    address asset;
    uint256 amount;
    uint16 referralCode;
    uint256 interestRateMode;
    address onBehalfOf;
    uint256 totalCollateralInBaseCurrency;
    uint256 totalDebtInBaseCurrency;
    uint256 avgLtv;
    uint256 availableBorrowsBase;
    uint256 healthFactorBefore;
    uint256 currentLiquidationThreshold;

    require(e.msg.sender != currentContract);
    totalCollateralInBaseCurrency, totalDebtInBaseCurrency, availableBorrowsBase, currentLiquidationThreshold, avgLtv, healthFactorBefore = getUserAccountData(e, onBehalfOf);
    require healthFactorBefore > 0;

    borrow@withrevert(e, asset, amount, interestRateMode, referralCode, onBehalfOf);
    bool borrowReverted = lastReverted;

    uint256 totalCollateralInBaseCurrency1;
    uint256 totalDebtInBaseCurrency1;
    uint256 avgLtv1;
    uint256 availableBorrowsBase1;
    uint256 healthFactor;
    uint256 currentLiquidationThreshold1;
    totalCollateralInBaseCurrency1, totalDebtInBaseCurrency1, availableBorrowsBase1, currentLiquidationThreshold1, avgLtv1, healthFactor = getUserAccountData(e, onBehalfOf);

    assert !borrowReverted => (healthFactor >= 1);
}

// @title P25: Whenever a user borrows an asset at a variable rate the balanceOf(user) on the VariableDebtToken increases by the amount borrowed
// Failing: https://prover.certora.com/output/31688/193b517f9ed24e17871b840cc3eb3d62/?anonymousKey=d254766ab67c09ac00ed09bed8669c8a8cd19088
rule balanceIncreaseAfterBorrowVariable(env e) {
    address asset;
    uint256 amount;
    uint16 referralCode;
    address onBehalfOf;


    uint256 balanceBefore = ballanceOfInAsset(e, asset, e.msg.sender);
    borrow(e, asset, amount, getVariableRateConstant(e), referralCode, onBehalfOf);
    uint256 balanceAfter = ballanceOfInAsset(e, asset, e.msg.sender);

    assert balanceAfter == require_uint256(balanceBefore + amount);
}

// @title P26: Whenever a user borrows an asset at a stable rate, the  balanceOf(user) on the StableDebtToken increases by the amount borrowed
// Failing: https://prover.certora.com/output/31688/00fafc3031a34fa7817787b8889b1ff4/?anonymousKey=4251aa5ce30e8f7d6429e33d4953c4bc20d8cfd5
rule balanceIncreaseAfterBorrowStable(env e) {
    address asset;
    uint256 amount;
    uint16 referralCode;
    address onBehalfOf;

    uint256 balanceBefore = ballanceOfInAsset(e, asset, e.msg.sender);
    borrow(e, asset, amount, getStableRateConstant(e), referralCode, onBehalfOf);
    uint256 balanceAfter = ballanceOfInAsset(e, asset, e.msg.sender);

    assert balanceAfter == require_uint256(balanceBefore + amount);
}

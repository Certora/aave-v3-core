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

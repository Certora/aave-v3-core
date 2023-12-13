import "pool-base.spec";

methods {
    function _._getUserDebtInBaseCurrency(address user, DataTypes.ReserveData storage reserve, uint256 assetPrice, uint256 assetUnit) internal => NONDET;
    function _.rayMul(uint256 a, uint256 b) internal => mulDivDownAbstractPlus(a, b, 10^27) expect uint256 ALL;
    function _.rayDiv(uint256 a, uint256 b) internal => mulDivDownAbstractPlus(a, 10^27, b) expect uint256 ALL;
    // function _.getFlags(DataTypes.ReserveConfigurationMap memory self) internal => NONDET;
	// function _.calculateInterestRates(DataTypes.CalculateInterestRatesParams params) external => NONDET;
}

// Passing for PoolHarness:
// https://prover.certora.com/output/40577/e75bfa369a10490ca0cc71992984dc54/?anonymousKey=c12450d39df13d66fd92b82819c9dcc7f66d2012
rule method_reachability(env e, method f) {
    calldataarg args;
    f(e, args);
    satisfy true;
}

// @title based on this result of run in the CI:
// https://prover.certora.com/output/33050/3e09e274b3644f6c9ed051b83a6e4dfb?anonymousKey=b6ade0dd3ada78730183db26a344bafb282861b4
definition methodIsEasyForRuleMethodReachability(method f) returns bool = f.isView ||
	     f.selector == sig:PoolHarness.getUserEMode(address).selector ||
	     f.selector == sig:PoolHarness.mintUnbacked(address,uint256,address,uint16).selector ||
	     f.selector == sig:PoolHarness.getUserConfiguration(address).selector ||
	     f.selector == sig:PoolHarness.finalizeTransfer(address,address,address,uint256,uint256,uint256).selector ||
	     // f.selector == sig:PoolHarness.POOL_REVISION().selector || // view function
	     f.selector == sig:PoolHarness.supply(address,uint256,address,uint16).selector ||
	     f.selector == sig:PoolHarness.getReserveAddressById(uint16).selector ||
	     f.selector == sig:PoolHarness.isStableRateEnabled(address).selector ||
	     f.selector == sig:PoolHarness.updateFlashloanPremiums(uint128,uint128).selector ||
	     f.selector == sig:PoolHarness.cumulateToLiquidityIndex(address,uint256,uint256).selector ||
	     f.selector == sig:PoolHarness.deposit(address,uint256,address,uint16).selector ||
	     // f.selector == sig:PoolHarness.FLASHLOAN_PREMIUM_TOTAL().selector || // view function
	     f.selector == sig:PoolHarness.swapBorrowRateMode(address,uint256).selector ||
	     f.selector == sig:PoolHarness.getReserveNormalizedVariableDebt(address).selector ||
	     f.selector == sig:PoolHarness.getReserveVariableBorrowIndex(address).selector ||
	     f.selector == sig:PoolHarness.withdraw(address,uint256,address).selector ||
	     // f.selector == sig:PoolHarness.FLASHLOAN_PREMIUM_TO_PROTOCOL().selector || // view function
	     f.selector == sig:PoolHarness.dropReserve(address).selector ||
	     f.selector == sig:PoolHarness.ballanceOfInAsset(address,address).selector ||
	     f.selector == sig:PoolHarness.setConfiguration(address, DataTypes.ReserveConfigurationMap).selector ||
	     f.selector == sig:PoolHarness.setUserEMode(uint8).selector ||
	     f.selector == sig:PoolHarness.getReserveLiquidityIndex(address).selector ||
	     f.selector == sig:PoolHarness.updateReserveIndexesWithCache(address,DataTypes.ReserveCache).selector ||
	     // f.selector == sig:PoolHarness.MAX_STABLE_RATE_BORROW_SIZE_PERCENT().selector || // view function
	     // f.selector == sig:PoolHarness.getReservesList().selector || // view function
	     // f.selector == sig:PoolHarness.getAvailableLiquidity(address).selector || // view function
	     // f.selector == sig:PoolHarness.getUserAccountData(address).selector || // view function
	     f.selector == sig:PoolHarness.rescueTokens(address,address,uint256).selector ||
	     // f.selector == sig:PoolHarness.getReserveStableBorrowRate(address).selector || // view function
	     // f.selector == sig:PoolHarness.MAX_NUMBER_RESERVES().selector || // view function
	     // f.selector == sig:PoolHarness.getVariableRateConstant().selector || // view function
	     f.selector == sig:PoolHarness.configureEModeCategory(uint8,DataTypes.EModeCategory).selector ||
	     f.selector == sig:PoolHarness.mintToTreasury(address[]).selector ||
	     f.selector == sig:PoolHarness.updateBridgeProtocolFee(uint256).selector ||
	     f.selector == sig:PoolHarness.setUserUseReserveAsCollateral(address,bool).selector ||
	     // f.selector == sig:PoolHarness.getConfiguration(address).selector || // view function
	     // f.selector == sig:PoolHarness.getTotalDebt(address).selector || // view function
	     // f.selector == sig:PoolHarness.getStableRateConstant().selector || // view function
	     // f.selector == sig:PoolHarness.getReserveNormalizedIncome(address).selector || // view function
	     f.selector == sig:PoolHarness.setReserveInterestRateStrategyAddress(address,address).selector ||
	     // f.selector == sig:PoolHarness.ADDRESSES_PROVIDER().selector || // view function
	     f.selector == sig:PoolHarness.initReserve(address,address,address,address,address).selector ||
	     // f.selector == sig:PoolHarness.getStableRate(address).selector || // view function
	     f.selector == sig:PoolHarness.resetIsolationModeTotalDebt(address).selector ||
	     // f.selector == sig:PoolHarness.getTotalATokenSupply(address).selector || // view function
	     // f.selector == sig:PoolHarness.getCurrScaledVariableDebt(address).selector || // view function
	     f.selector == sig:PoolHarness.initialize(address).selector ||
	     // f.selector == sig:PoolHarness.getReserveVariableBorrowRate(address).selector || // view function
	     // f.selector == sig:PoolHarness.getEModeCategoryData(uint8).selector || // view function
	     f.selector == sig:PoolHarness.BRIDGE_PROTOCOL_FEE().selector ||
	     // f.selector == sig:PoolHarness.getReserveData(address).selector || // view function
	     f.selector == sig:PoolHarness.updateReserveIndexes(address).selector;

rule method_reachability_split_for_CI_01(env e, method f, calldataarg args) filtered {
    f -> methodIsEasyForRuleMethodReachability(f)
} {
    f(e, args);
    satisfy true;
}

rule method_reachability_split_for_CI_02_backUnbacked(env e, method f, calldataarg args) filtered {
    f -> f.selector == sig:PoolHarness.backUnbacked(address,uint256,uint256).selector
} {
    f(e, args);
    satisfy true;
}

rule method_reachability_split_for_CI_03_repayWithATokens(env e, method f, calldataarg args) filtered {
    f -> f.selector == sig:PoolHarness.repayWithATokens(address,uint256,uint256).selector
} {
    f(e, args);
    satisfy true;
}

rule method_reachability_split_for_CI_04_repayWithPermit(env e, method f, calldataarg args) filtered {
    f -> f.selector == sig:PoolHarness.repayWithPermit(address,uint256,uint256,address,uint256,uint8,bytes32,bytes32).selector
} {
    f(e, args);
    satisfy true;
}

rule method_reachability_split_for_CI_05_liquidationCall(env e, method f, calldataarg args) filtered {
    f -> f.selector == sig:PoolHarness.liquidationCall(address,address,address,uint256,bool).selector
} {
    f(e, args);
    satisfy true;
}

rule method_reachability_split_for_CI_06_flashLoan(env e, method f, calldataarg args) filtered {
    f -> f.selector == sig:PoolHarness.flashLoan(address,address[],uint256[],uint256[],address,bytes,uint16).selector
} {
    f(e, args);
    satisfy true;
}

rule method_reachability_split_for_CI_07_borrow(env e, method f, calldataarg args) filtered {
    f -> f.selector == sig:PoolHarness.borrow(address,uint256,uint256,uint16,address).selector
} {
    f(e, args);
    satisfy true;
}

rule method_reachability_split_for_CI_08_supplyWithPermit(env e, method f, calldataarg args) filtered {
    f -> f.selector == sig:PoolHarness.supplyWithPermit(address,uint256,address,uint16,uint256,uint8,bytes32,bytes32).selector
} {
    f(e, args);
    satisfy true;
}

rule method_reachability_split_for_CI_09_rebalanceStableBorrowRate(env e, method f, calldataarg args) filtered {
    f -> f.selector == sig:PoolHarness.rebalanceStableBorrowRate(address,address).selector
} {
    f(e, args);
    satisfy true;
}

rule method_reachability_split_for_CI_10_repay(env e, method f, calldataarg args) filtered {
    f -> f.selector == sig:PoolHarness.repay(address,uint256,uint256,address).selector
} {
    f(e, args);
    satisfy true;
}

rule method_reachability_split_for_CI_11_flashLoanSimple(env e, method f, calldataarg args) filtered {
    f -> f.selector == sig:PoolHarness.flashLoanSimple(address,address,uint256,bytes,uint16).selector
} {
    f(e, args);
    satisfy true;
}

// @title It is impossible to deposit an inactive reserve
// Proved:
// https://prover.certora.com/output/40577/b8bd6244053e42e4bddb129f04e1dd93/?anonymousKey=5374001e512e1149d120f0efa19c18a3d531d115
// Note, that getFlags must not be NONDET.
rule cannotDepositInInactiveReserve(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;
    bool reserveIsActive = isActiveReserve(e, asset);

    deposit(e, asset, amount, onBehalfOf, referralCode);

    assert reserveIsActive;
}

// @title It is impossible to deposit a frozen reserve
// Proved:
// https://prover.certora.com/output/40577/d4f2bfae10ae4092bb7dab309e72b166/?anonymousKey=a370279a63e87a810fd79cb20d33ef00aead7c2b
// Note, that getFlags must not be NONDET.
rule cannotDepositInFrozenReserve(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;
    bool reserveIsFrozen = isFrozenReserve(e, asset);

    deposit(e, asset, amount, onBehalfOf, referralCode);

    assert !reserveIsFrozen;
}

// @title It is impossible to deposit zero amount
// Proved
// https://prover.certora.com/output/40577/400f77e9ca1948b9896ca35435b0ea03/?anonymousKey=760e8acd1473e9eb801aa4bcaf60d50927f9f026
rule cannotDepositZeroAmount(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;

    deposit(e, asset, amount, onBehalfOf, referralCode);

    assert amount != 0;
}

// @title It is impossible to withdraw zero amount
// Proved
// https://prover.certora.com/output/40577/869e48220a2d40369884dd6a0cbd1734/?anonymousKey=7cf6aced7660c59314f767f4f14de508e38a37ea
rule cannotWithdrawZeroAmount(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;

    withdraw(e, asset, amount, to);

    assert amount != 0;
}

// @title It is impossible to withdraw an inactive reserve
// Proved
// https://prover.certora.com/output/40577/a4eb1d4472ae43c2a1bfe202f070453a/?anonymousKey=05c0ddc494d371d6a28fc40ed4cc1902bba29eba
// Note, that getFlags must not be NONDET.
rule cannotWithdrawFromInactiveReserve(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;
    bool reserveIsActive = isActiveReserve(e, asset);

    withdraw(e, asset, amount, to);

    assert reserveIsActive;
}

// @title It is impossible to borrow zero amount
// Proved
// https://prover.certora.com/output/40577/13a0a08cbc6f448888bcdb28716d856b/?anonymousKey=48621623ac7255815e8a6465d72d38f39d55f0f4
rule cannotBorrowZeroAmount(env e) {
    address asset;
    uint256 amount;
    uint256 interestRateMode;
    uint16 referralCode;
    address onBehalfOf;

    borrow(e, asset, amount, interestRateMode, referralCode, onBehalfOf);

    assert amount != 0;
}

// @title It is impossible to borrow on inactive reserve.
// Proved
// https://prover.certora.com/output/40577/2e93cd5ce80f4aa491b9d648e1a73583/?anonymousKey=64bbd85099c3ae4a387bd0a24ce565c23094ee4f
// Note, that getFlags must not be NONDET.
rule cannotBorrowOnInactiveReserve(env e) {
    address asset;
    uint256 amount;
    uint256 interestRateMode;
    uint16 referralCode;
    address onBehalfOf;
    bool reserveIsActive = isActiveReserve(e, asset);

    borrow(e, asset, amount, interestRateMode, referralCode, onBehalfOf);

    assert reserveIsActive;
}

// It is impossible to borrow on a reserve, that is disabled for borrowing.
// Proved
// https://prover.certora.com/output/40577/1b50faf4cbb3459c9563e4af75658525/?anonymousKey=e04b8838d1f6eceb3fb29504969ecf0817269679
// Note, that getFlags must not be NONDET.
rule cannotBorrowOnReserveDisabledForBorrowing(env e) {
    address asset;
    uint256 amount;
    uint256 interestRateMode;
    uint16 referralCode;
    address onBehalfOf;
    bool reserveIsEnabledForBorrow = isEnabledForBorrow(e, asset);

    borrow(e, asset, amount, interestRateMode, referralCode, onBehalfOf);

    assert reserveIsEnabledForBorrow;
}

// @title It is impossible to borrow on frozen reserve.
// Proved
// https://prover.certora.com/output/40577/b25ecb5e5b804832b3aa75e3bd54079c/?anonymousKey=8029d9f6ac5edf386f4795c4de0e7928f0487722
// Note, that getFlags must not be NONDET.
rule cannotBorrowOnFrozenReserve(env e) {
    address asset;
    uint256 amount;
    uint256 interestRateMode;
    uint16 referralCode;
    address onBehalfOf;
    bool reserveIsFrozen = isFrozenReserve(e, asset);

    borrow(e, asset, amount, interestRateMode, referralCode, onBehalfOf);

    assert !reserveIsFrozen;
}

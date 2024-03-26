import "NEW-pool-base.spec";

methods {
    // function _.calculateInterestRates(DataTypes.CalculateInterestRatesParams storage params) external => NONDET;
    // function _.calculateInterestRates(DataTypes.CalculateInterestRatesParams params) external => calculateInterestRatesMock(params) expect uint256, uint256, uint256 ALL;
    function _.hasRole(bytes32 b ,address a) external => DISPATCHER(true);

    function _.getReservesList() external => DISPATCHER(true);
    function _.getReserveData(address a) external => DISPATCHER(true);

    function _.symbol() external => DISPATCHER(true);
    function _.isFlashBorrower(address a) external => DISPATCHER(true);

    function _.executeOperation(address[] a, uint256[]b, uint256[]c, address d, bytes e) external => DISPATCHER(true);

    function _.getAverageStableRate() external => DISPATCHER(true);
    function _.isPoolAdmin(address a) external => DISPATCHER(true);
    function _.getConfiguration(address a) external => DISPATCHER(true);

    function _.rayMul(uint256 a, uint256 b) internal => mulDivDownAbstractPlus(a, b, 10^27) expect uint256 ALL;
    function _.rayDiv(uint256 a, uint256 b) internal => mulDivDownAbstractPlus(a, 10^27, b) expect uint256 ALL;

    //IPriceOracleSentinel
    function _.isBorrowAllowed() external => DISPATCHER(true);
    function _.isLiquidationAllowed() external => DISPATCHER(true);
    function _.setSequencerOracle(address newSequencerOracle) external => DISPATCHER(true);
    function _.setGracePeriod(uint256 newGracePeriod) external => DISPATCHER(true);
    function _.getGracePeriod() external => DISPATCHER(true);

    // Modification of index is tracked by incrementCounter:
    function _.incrementCounter() external => ghostUpdate() expect bool ALL;
}

ghost mathint counterUpdateIndexes;

function ghostUpdate() returns bool
{
    counterUpdateIndexes = counterUpdateIndexes + 1;
	return true;
}


function calculateInterestRatesMock(DataTypes.CalculateInterestRatesParams params) returns (uint256, uint256, uint256)
{
    uint256 liquidityRate = 1;
    uint256 stableBorrowRate = 1;
    uint256 variableBorrowRate = 1;
	return (liquidityRate, stableBorrowRate, variableBorrowRate);
}


/* ==================================================================================================
   @title Rule checking, that the ghostUpdate summary is correct and that it is being applied
   This rule is part of a check, that the liquidity index cannot decrease.

   Nissan remark on 26/03/2024: This rule fails!
   See here: https://prover.certora.com/output/66114/812c9675658a4d4d935a8e0a3e1f4a99/?anonymousKey=46e0337ab421a402e525e156b4aa1fb7a9b2fce9
   ==================================================================================================*/
rule _updateIndexesWrapperReachable(env e, method f) {
    calldataarg args;

	mathint updateIndexesCallCountBefore = counterUpdateIndexes;

	f(e, args);

	mathint updateIndexesCallCountAfter = counterUpdateIndexes;

    satisfy updateIndexesCallCountBefore != updateIndexesCallCountAfter;
}

// @title cumulateToLiquidityIndex does not decrease the liquidity index.
// This rule is part of a check, that the liquidity index cannot decrease.
// Proved here:
// https://prover.certora.com/output/40577/bb018f9a52b64b27a0ac364e0c22cd79/?anonymousKey=21613bfbfc0f479ed2c99ce5fa2dd16e581baf5e
rule liquidityIndexNonDecresingFor_cumulateToLiquidityIndex()
{
    address asset;
	uint256 totalLiquidity;
	uint256 amount;
    env e;
    
    uint256 reserveLiquidityIndexBefore = getReserveLiquidityIndex(e, asset);
    require reserveLiquidityIndexBefore >= RAY();

    uint256 reserveLiquidityIndexAfter = cumulateToLiquidityIndex(e, asset, totalLiquidity, amount);

    assert reserveLiquidityIndexAfter >= reserveLiquidityIndexBefore;
}

/* ==================================================================================================
// @title When liquidity index changes, either ReserveLogic::_updateIndex or ReserveLogic::cumulateToLiquidityIndex has been called.
// This rule is part of a check, that the liquidity index cannot decrease.
// We use ghost counterUpdateIndexes to track callings to special interface function ICVL.incrementCounter(), which happens
// only in the two methods ReserveLogic::_updateIndex and ReserveLogic::cumulateToLiquidityIndex
//
// Almost Proved. In these runs (only for liquidationCall timeouts):
// repayWithATokens: https://prover.certora.com/output/40577/cde7addcfdf94737bc83afb01c8935db/?anonymousKey=160f24175b6c590e99b2c5f24501854ed8cabe90
// repayWithPermit: https://prover.certora.com/output/40577/722a0fcc745e4a6aad84aadcfafe051f/?anonymousKey=ba5250252cac965ece652255af19c514ac338613
// TIMEOUT !!! liquidationCall: https://prover.certora.com/output/40577/4b3395d424dd453f8631c417058d8a58/?anonymousKey=5c3a840f6f5c7d948752fc37de801f92cd7819fa
// repay: https://prover.certora.com/output/40577/1cfbfdeca1f742e289f7db3e5b99bb5a/?anonymousKey=25806694d7eb991c9b66f3268b8a055b291b7fc9
// everything else: https://prover.certora.com/output/40577/9499b88814524c0ea03e2286250cb79c/?anonymousKey=8391a758d5594555c69cc3230509fe0bb9a478bf


   Nissan remark on 26/03/2024: This rule fails!
   See here: https://prover.certora.com/output/66114/812c9675658a4d4d935a8e0a3e1f4a99/?anonymousKey=46e0337ab421a402e525e156b4aa1fb7a9b2fce9
   ==================================================================================================*/
rule indexChangesOnlyWith_updateIndexes(env e, method f) filtered {
    f -> !f.isView &&
	     f.selector != sig:PoolHarness.updateReserveIndexes(address).selector &&
        //  f.selector != sig:PoolHarness.updateReserveIndexesWithCache(address,_).selector &&
		 f.selector != sig:PoolHarness.dropReserve(address).selector &&
		 f.selector != sig:PoolHarness.initReserve(address,address,address,address,address).selector
} {
    address asset;
    calldataarg args;

    mathint liquidityIndexBefore = getLiquidityIndex(e, asset);
    require liquidityIndexBefore < max_uint256;
	mathint updateIndexesCallCountBefore = counterUpdateIndexes;
    require liquidityIndexBefore >= to_mathint(RAY());

	f(e, args);

    mathint liquidityIndexAfter = getLiquidityIndex(e, asset);
	mathint updateIndexesCallCountAfter = counterUpdateIndexes;

    assert liquidityIndexAfter != liquidityIndexBefore => updateIndexesCallCountBefore != updateIndexesCallCountAfter;
}

/*==================================================================================================
// @title _updateIndexes cannot decrease the indexes
// This rule is part of a check, that the liquidity index cannot decrease.
// Proved:
// https://prover.certora.com/output/6893/be1581a978124ff4907a73774b878b8a/?anonymousKey=d557886cfefc63a31e0d73e846529ecd1268c429
// Similar rule here: https://prover.certora.com/output/40577/5001fdd253a8429589906a5a82bd027e/?anonymousKey=fd1ba83af54cb583b13966783433ba0aff985f8b

Nissan remark on 26/03/2024: This rule fails!
See here: https://prover.certora.com/output/66114/812c9675658a4d4d935a8e0a3e1f4a99/?anonymousKey=46e0337ab421a402e525e156b4aa1fb7a9b2fce9
==================================================================================================*/
rule indexesNonDecresingFor_updateIndexes()
{
    address asset;
    env e;

    uint256 reserveLiquidityIndexBefore = getReserveLiquidityIndex(e, asset);
    uint256 variableBorrowIndexBefore = getReserveVariableBorrowIndex(e, asset);
    require reserveLiquidityIndexBefore >= RAY();
    DataTypes.ReserveCache cache;
    require cache.currLiquidityIndex == reserveLiquidityIndexBefore;
    require cache.currVariableBorrowIndex == variableBorrowIndexBefore;

    updateReserveIndexesWithCache(e, asset, cache);

    uint256 variableBorrowIndexAfter = getReserveVariableBorrowIndex(e, asset);
    uint256 reserveLiquidityIndexAfter = getReserveLiquidityIndex(e, asset);
    assert variableBorrowIndexAfter >= variableBorrowIndexBefore;
    assert reserveLiquidityIndexAfter >= reserveLiquidityIndexBefore;
}

// @title When a user deposits asset, his corresponding aToken balance increases (doesn't say by how much).
// We proved something similar here:
// https://prover.certora.com/output/40577/fad5aaf8dcd749448281077a94787820/?anonymousKey=0038e1e03f375e0e1a5b77a77f703ed059a86afd
// But still we keep this little stronger rule. This rule is currently timeouting:
// TIMEOUT:
// https://prover.certora.com/output/40577/91d9cf9aac8846ad9e84569b4a05fded/?anonymousKey=01b9afcf3cbfb036c9a02557cfe9ac1d575ecfbe
// rule depositIncreasesUserBalance(env e) {
//     address asset;
//     uint256 amount;
//     address onBehalfOf;
//     uint16 referralCode;
//     mathint balance_before = aTokenBalanceOf(e, onBehalfOf);
//     require balance_before == 6*RAY();
//     mathint balance_before_sender = aTokenBalanceOf(e, e.msg.sender);
//     require balance_before_sender + balance_before_sender > balance_before_sender;
//     mathint underlying_balance_before = _underlyingAsset.balanceOf(e, onBehalfOf);
//     mathint underlying_balance_before_sender = _underlyingAsset.balanceOf(e, e.msg.sender);
//     require to_mathint(amount) == 3*RAY();
//     require asset != onBehalfOf;
//     require onBehalfOf != _aToken;
//     require e.msg.sender != _aToken;
//     require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);
//     mathint normalized_income_before = getReserveNormalizedIncome(e, asset);
//     require normalized_income_before == to_mathint(RAY());

//     // e.msg.sender pays amount of asset and aToken balance of 'onBehalfOf' increases by amount
//     deposit(e, asset, amount, onBehalfOf, referralCode);

//     mathint balance_after = aTokenBalanceOf(e, onBehalfOf);
//     mathint balance_after_sender = aTokenBalanceOf(e, e.msg.sender);
//     mathint underlying_balance_after = _underlyingAsset.balanceOf(e, onBehalfOf);
//     mathint underlying_balance_after_sender = _underlyingAsset.balanceOf(e, e.msg.sender);
//     mathint normalized_income_after = getReserveNormalizedIncome(e, asset);
//     mathint amountScaled;

//     assert normalized_income_before == normalized_income_after => balance_after > balance_before;
// }

// @title When a user deposits X amount of an asset, he receives exactly X amount of the corresponding aToken.
// TIMEOUT:
// https://prover.certora.com/output/40577/c1bfa2d810f34762ba9af721b8ed45cf/?anonymousKey=dae12197a619d40fc71332968b1fce6ce2d04030
// rule depositUpdatesUserATokenBalance(env e) {
//     address asset;
//     uint256 amount;
//     address onBehalfOf;
//     uint16 referralCode;

//     require to_mathint(amount) == 30*RAY(); //under approx
//     require asset != onBehalfOf;
//     require onBehalfOf != _aToken;
//     require e.msg.sender != _aToken;
//     require e.msg.sender != asset;
//     require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);

//     mathint balanceBefore = aTokenBalanceOf(e, onBehalfOf);
//     mathint superBalanceBefore = _aToken.superBalance(e, onBehalfOf);
//     require superBalanceBefore == 20*RAY(); //under approx

//     mathint liquidityIndexBefore = getLiquidityIndex(e, asset);
//     require liquidityIndexBefore == to_mathint(RAY()); //under approx
//     mathint normalized_income_before = getReserveNormalizedIncome(e, asset);
//     require normalized_income_before == to_mathint(RAY());

//     deposit(e, asset, amount, onBehalfOf, referralCode);

//     mathint balanceAfter = aTokenBalanceOf(e, onBehalfOf);
//     mathint normalized_income_after = getReserveNormalizedIncome(e, asset);
//     require normalized_income_after == normalized_income_before;

//     mathint liquidityIndexAfter = getLiquidityIndex(e, asset);

//     require liquidityIndexAfter == liquidityIndexBefore;

//     assert balanceAfter >= balanceBefore + amount - RAY() - RAY();
//     assert balanceAfter <= balanceBefore + amount + RAY() + RAY();
// }


// @title When a user deposits X amount of an asset and the current liquidity index for this asset is 1, his scaled balance (=superBalance) increases by X.
// Using superBalance is easier for the prover as we do not need to compute the balance from the scaled balance.
// WE ALLOW OFF BY ONE RAY
// Proved here:
// https://prover.certora.com/output/40748/64071407741f4234a137572fdbbf4437/?anonymousKey=745539ab36494a799c922b6d401d0c604c03b1a0
rule depositUpdatesUserATokenSuperBalance(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;

    require to_mathint(amount) == 30*RAY(); //under approx
    require asset != onBehalfOf;
    require onBehalfOf != _aToken;
    require e.msg.sender != _aToken;
    require e.msg.sender != asset;
    require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);

    mathint superBalanceBefore = _aToken.superBalance(e, onBehalfOf);
    require superBalanceBefore == 20*RAY(); //under approx
    mathint liquidityIndexBefore = getLiquidityIndex(e, asset);
    require liquidityIndexBefore == 1*RAY(); //under approx
    mathint currentLiquidityRateBefore = getCurrentLiquidityRate(e, asset);
    require currentLiquidityRateBefore == 1; //under approx

    deposit(e, asset, amount, onBehalfOf, referralCode);

    mathint superBalanceAfter = _aToken.superBalance(e, onBehalfOf);
    mathint currentLiquidityRateAfter = getCurrentLiquidityRate(e, asset);
    require currentLiquidityRateAfter == currentLiquidityRateBefore;

    mathint liquidityIndexAfter = getLiquidityIndex(e, asset);

    require liquidityIndexAfter == liquidityIndexBefore;
    assert superBalanceAfter >= superBalanceBefore + amount - 1 * RAY();
    assert superBalanceAfter <= superBalanceBefore + amount + 1 * RAY();
}

// @title Depositing on behalf of user A does not change balance of user other than A.
// Proved here:
// https://prover.certora.com/output/40577/f1ffe85de15b4dff80901c7de73dddaa/?anonymousKey=cd4234136f07cfc1d25aa13344a8ef7893af4ab0
rule depositCannotChangeOthersATokenSuperBalance(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    address otherUser;
    uint16 referralCode;

    require to_mathint(amount) == 30*RAY(); //under approx
    require asset != onBehalfOf;
    require onBehalfOf != _aToken;
    require e.msg.sender != _aToken;
    require e.msg.sender != asset;
    require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);
    require otherUser != onBehalfOf;
    require otherUser != _aToken;

    mathint superBalanceBefore = _aToken.superBalance(e, otherUser);

    deposit(e, asset, amount, onBehalfOf, referralCode);

    mathint superBalanceAfter = _aToken.superBalance(e, otherUser);
    assert superBalanceAfter == superBalanceBefore;
}


// @title Transferring AToken does not change AToken total supply.
// TIMEOUT
// Latest timeout: https://prover.certora.com/output/40577/1edb3b6f54404c2fbde79ef1b66553e6/?anonymousKey=8043b4fb6ff3e8ef32fd6f6db09de09e4b40acab
// rule transferATokenDoesntChangeTotal(env e, method f) filtered{
//     f -> !f.isView &&
//     f.selector != sig:initReserve(address,address, address, address, address).selector &&
//     f.selector != sig:dropReserve(address).selector
// } {
//     address user;
//     calldataarg args;
//     mathint balance_before = aTokenBalanceOf(e, user);
//     mathint total_supply_before = _aToken.totalSupply(e);
//     f(e, args);
//     mathint balance_after = aTokenBalanceOf(e, user);
//     mathint total_supply_after = _aToken.totalSupply(e);

//     assert balance_before != balance_after => total_supply_before == total_supply_after;
// }

import "pool-base.spec";
//import "pool_mintBurnIndex.spec";

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

    //IPriceOracleSentinel
    function _.isBorrowAllowed() external => DISPATCHER(true);
    function _.isLiquidationAllowed() external => DISPATCHER(true);
    function _.setSequencerOracle(address newSequencerOracle) external => DISPATCHER(true);
    function _.setGracePeriod(uint256 newGracePeriod) external => DISPATCHER(true);
    function _.getGracePeriod() external => DISPATCHER(true);

}


function calculateInterestRatesMock(DataTypes.CalculateInterestRatesParams params) returns (uint256, uint256, uint256)
{
    uint256 liquidityRate = 1;
    uint256 stableBorrowRate = 1;
    uint256 variableBorrowRate = 1;
	return (liquidityRate, stableBorrowRate, variableBorrowRate);
}

rule liquidityIndexGteRay(method f) filtered 
    { f -> f.contract == currentContract 
           //&& f.selector != sig:dropReserve(address).selector
           //&& f.selector == sig:withdraw(address,uint256,address).selector
           //&& f.selector == sig:repay(address,uint256,uint256,address).selector
           //&& f.selector == sig:repayWithPermit(address,uint256,uint256,address,uint256,uint8,bytes32,bytes32).selector
           //&& f.selector == sig:backUnbacked(address,uint256,uint256).selector
           //&& f.selector == sig:supply(address,uint256,address,uint16).selector
           //&& f.selector == sig:mintUnbacked(address,uint256,address,uint16).selector
           //&& f.selector == sig:swapBorrowRateMode(address,uint256).selector
           //&& f.selector == sig:deposit(address,uint256,address,uint16).selector
           //&& f.selector == sig:flashLoanSimple(address,address,uint256,bytes,uint16).selector
           //&& f.selector == sig:liquidationCall(address,address,address,uint256,bool).selector
           //&& f.selector == sig:repayWithATokens(address,uint256,uint256).selector
           //&& f.selector == sig:supplyWithPermit(address,uint256,address,uint16,uint256,uint8,bytes32,bytes32).selector
           && f.selector == sig:rebalanceStableBorrowRate(address,address).selector
           }
{
    address asset;
    env e;
	calldataarg arg;
    uint256 indexBefore = getReserveLiquidityIndex(e, asset);
    //require indexBefore >= RAY();
	f(e, arg); 
    uint256 indexAfter = getReserveLiquidityIndex(e, asset);
    //assert indexAfter >= RAY();
    assert indexAfter >= indexBefore;
}

rule stableBorrowRateGteRay(method f) filtered 
    { f -> f.contract == currentContract && 
           f.selector != sig:dropReserve(address).selector }
{
    address asset;
    env e;
	calldataarg arg;
    uint256 indexBefore = getReserveStableBorrowRate(e, asset);
    require indexBefore >= RAY();
	f(e, arg); 
    uint256 indexAfter = getReserveStableBorrowRate(e, asset);
    assert indexAfter >= RAY();
}

rule variableBorrowIndexGteRay(method f) filtered 
    { f -> f.contract == currentContract  
           && f.selector != sig:dropReserve(address).selector 
           && f.selector == sig:supply(address,uint256,address,uint16).selector
    }
{
    address asset;
    env e;
	calldataarg arg;
    uint256 indexBefore = getReserveVariableBorrowIndex(e, asset);
    require indexBefore >= RAY();
	f(e, arg); 
    uint256 indexAfter = getReserveVariableBorrowIndex(e, asset);
    assert indexAfter >= indexBefore; //RAY();
}

rule indexesNonDecresing()
{
    address asset;
    env e;
    
    uint256 reserveLiquidityIndexBefore = getReserveLiquidityIndex(e, asset);
    uint256 variableBorrowIndexBefore = getReserveVariableBorrowIndex(e, asset);
    //uint256 stableBorrowIndexBefore = getReserveVariableBorrowIndex(e, asset);
    require reserveLiquidityIndexBefore >= RAY();   //from ReserveLogic.init
    //require getReserveVariableBorrowRate(e, asset) >= RAY();
    DataTypes.ReserveCache cache;
    require cache.currLiquidityIndex == reserveLiquidityIndexBefore;
    require cache.currVariableBorrowIndex == variableBorrowIndexBefore;

	//updateReserveIndexes(e, asset);
    updateReserveIndexesWithCache(e, asset, cache);

    uint256 variableBorrowIndexAfter = getReserveVariableBorrowIndex(e, asset);
    uint256 reserveLiquidityIndexAfter = getReserveLiquidityIndex(e, asset);
    assert variableBorrowIndexAfter >= variableBorrowIndexBefore;
    assert reserveLiquidityIndexAfter >= reserveLiquidityIndexBefore;
}

rule dummy(method f)
{
    env e;
	calldataarg arg;
	f(e, arg); 
    assert true;
}

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

//     // require _userState[onBehalfOf].additionalData == 1 * RAY();

//     mathint balanceBefore = aTokenBalanceOf(e, onBehalfOf);
//     // require balanceBefore == 20*RAY(); //under approx

//     mathint superBalanceBefore = _aToken.superBalance(e, onBehalfOf);
//     require superBalanceBefore == 20*RAY(); //under approx
//     mathint liquidityIndexBefore = getLiquidityIndex(e, asset);
//     require liquidityIndexBefore == to_mathint(RAY());
//     // TODO: Fight with getNormalizedIncome in this report:
//     // https://prover.certora.com/output/40577/166daca033a340fbad7e3f554075bdcd/?anonymousKey=2a537acce252cfb24a7ed9ccc4328325d4058339
//     // mathint normalized_income_before = getReserveNormalizedIncome(e, asset);
//     // require normalized_income_before == 1*RAY();
//     // Or instead, easier may be to require currentLiquidityRate to be Ray:
//     mathint currentLiquidityRateBefore = getCurrentLiquidityRate(e, asset);
//     require currentLiquidityRateBefore == to_mathint(RAY());


//     // e.msg.sender pays amount of asset and aToken balance of 'onBehalfOf' increases by amount
//     deposit(e, asset, amount, onBehalfOf, referralCode);

//     mathint balanceAfter = aTokenBalanceOf(e, onBehalfOf);
//     // mathint superBalanceAfter = _aToken.superBalance(e, onBehalfOf);
//     // mathint currentLiquidityRateAfter = getCurrentLiquidityRate(e, asset);
//     mathint liquidityIndexAfter = getLiquidityIndex(e, asset);

//     // assert currentLiquidityRateBefore == currentLiquidityRateAfter;

//     // assert superBalanceAfter == superBalanceBefore + amount;
//     require liquidityIndexAfter == liquidityIndexBefore;
//     assert balanceAfter >= balanceBefore + amount - RAY() - RAY();
//     assert balanceAfter <= balanceBefore + amount + RAY() + RAY();
//     // assert superBalanceAfter >= superBalanceBefore + amount - 2 * RAY();
//     // assert superBalanceAfter <= superBalanceBefore + amount + 2 * RAY();
// }

rule depositUpdatesUserATokenBalance(env e) {
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

    mathint balanceBefore = aTokenBalanceOf(e, onBehalfOf);
    // require balanceBefore == 20*RAY(); //under approx
    mathint superBalanceBefore = _aToken.superBalance(e, onBehalfOf);
    require superBalanceBefore == 20*RAY(); //under approx

    mathint liquidityIndexBefore = getLiquidityIndex(e, asset);
    require liquidityIndexBefore == to_mathint(RAY()); //under approx
    // mathint currentLiquidityRateBefore = getCurrentLiquidityRate(e, asset);
    // require currentLiquidityRateBefore == 1; //under approx
    // require currentLiquidityRateBefore == 0; //under approx
    mathint normalized_income_before = getReserveNormalizedIncome(e, asset);
    require normalized_income_before == to_mathint(RAY());

    deposit(e, asset, amount, onBehalfOf, referralCode);

    mathint balanceAfter = aTokenBalanceOf(e, onBehalfOf);
    // mathint currentLiquidityRateAfter = getCurrentLiquidityRate(e, asset);
    // require currentLiquidityRateAfter == currentLiquidityRateBefore;
    mathint normalized_income_after = getReserveNormalizedIncome(e, asset);
    require normalized_income_after == normalized_income_before;

    mathint liquidityIndexAfter = getLiquidityIndex(e, asset);

    require liquidityIndexAfter == liquidityIndexBefore;

    // uint256 liquidityRate;
    // uint256 stableBorrowRate;
    // uint256 variableBorrowRate;
    // (liquidityRate, stableBorrowRate, variableBorrowRate) = getInterestRates();

    assert balanceAfter >= balanceBefore + amount - RAY() - RAY();
    assert balanceAfter <= balanceBefore + amount + RAY() + RAY();
}

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


    // mathint balanceBefore = aTokenBalanceOf(e, onBehalfOf);

    mathint superBalanceBefore = _aToken.superBalance(e, onBehalfOf);
    require superBalanceBefore == 20*RAY(); //under approx
    mathint liquidityIndexBefore = getLiquidityIndex(e, asset);
    require liquidityIndexBefore == to_mathint(RAY()); //under approx
    mathint currentLiquidityRateBefore = getCurrentLiquidityRate(e, asset);
    require currentLiquidityRateBefore == 1; //under approx
    // require currentLiquidityRateBefore == 0; //under approx

    deposit(e, asset, amount, onBehalfOf, referralCode);

    // mathint balanceAfter = aTokenBalanceOf(e, onBehalfOf);
    mathint superBalanceAfter = _aToken.superBalance(e, onBehalfOf);
    mathint currentLiquidityRateAfter = getCurrentLiquidityRate(e, asset);
    require currentLiquidityRateAfter == currentLiquidityRateBefore;

    mathint liquidityIndexAfter = getLiquidityIndex(e, asset);

    require liquidityIndexAfter == liquidityIndexBefore;
    // assert balanceAfter >= balanceBefore + amount - RAY() - RAY();
    // assert balanceAfter <= balanceBefore + amount + RAY() + RAY();
    assert superBalanceAfter >= superBalanceBefore + amount - RAY();
    assert superBalanceAfter <= superBalanceBefore + amount + RAY();
}

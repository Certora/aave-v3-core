import "pool-base.spec";

methods {
    // //Unsat Core Based
    //function _.getFlags(DataTypes.ReserveConfigurationMap memory self) internal => NONDET;
    //function _.setUsingAsCollateral(DataTypes.UserConfigurationMap storage self,uint256 reserveIndex,bool usingAsCollateral) internal => NONDET;
    //function _.setBorrowing(DataTypes.UserConfigurationMap storage self,uint256 reserveIndex,bool borrowing) internal => NONDET;


    // function _.calculateInterestRates(DataTypes.CalculateInterestRatesParams storage params) external => NONDET;
    // function _.calculateInterestRates(DataTypes.CalculateInterestRatesParams params) external => calculateInterestRatesMock(params) expect uint256, uint256, uint256 ALL;

    //function _.rayMul(uint256 a, uint256 b) internal => rayMulPreciseSummarization(a, b) expect uint256 ALL;
    //function _.rayDiv(uint256 a, uint256 b) internal => rayDivPreciseSummarization(a, b) expect uint256 ALL;
}


function calculateInterestRatesMock(DataTypes.CalculateInterestRatesParams params) returns (uint256, uint256, uint256)
{
    uint256 liquidityRate = 1;
    uint256 stableBorrowRate = 1;
    uint256 variableBorrowRate = 1;
	return (liquidityRate, stableBorrowRate, variableBorrowRate);
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

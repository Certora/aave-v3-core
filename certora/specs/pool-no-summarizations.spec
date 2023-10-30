import "pool-base.spec";

methods {
    // //Unsat Core Based
    function _.getFlags(DataTypes.ReserveConfigurationMap memory self) internal => NONDET;
    function _.setUsingAsCollateral(DataTypes.UserConfigurationMap storage self,uint256 reserveIndex,bool usingAsCollateral) internal => NONDET;
    function _.setBorrowing(DataTypes.UserConfigurationMap storage self,uint256 reserveIndex,bool borrowing) internal => NONDET;



    // function _.calculateInterestRates(DataTypes.CalculateInterestRatesParams storage params) external => NONDET;
}

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

    // require _userState[onBehalfOf].additionalData == 1 * RAY();

    mathint balanceBefore = aTokenBalanceOf(e, onBehalfOf);
    require balanceBefore == 20*RAY(); //under approx

    // mathint superBalanceBefore = _aToken.superBalance(e, onBehalfOf);
    // require superBalanceBefore == 20*RAY(); //under approx
    // mathint currentLiquidityRateBefore = getCurrentLiquidityRate(e, asset);
    mathint liquidityIndexBefore = getLiquidityIndex(e, asset);
    // require currentLiquidityRateBefore == 1;
    require liquidityIndexBefore == 1*RAY();

    // e.msg.sender pays amount of asset and aToken balance of 'onBehalfOf' increases by amount
    deposit(e, asset, amount, onBehalfOf, referralCode);

    mathint balanceAfter = aTokenBalanceOf(e, onBehalfOf);
    // mathint superBalanceAfter = _aToken.superBalance(e, onBehalfOf);
    // mathint currentLiquidityRateAfter = getCurrentLiquidityRate(e, asset);
    mathint liquidityIndexAfter = getLiquidityIndex(e, asset);

    // assert currentLiquidityRateBefore == currentLiquidityRateAfter;
    // assert liquidityIndexBefore == liquidityIndexAfter;

    // assert superBalanceAfter == superBalanceBefore + amount;
    require liquidityIndexAfter == liquidityIndexBefore;
    assert balanceAfter >= balanceBefore + amount - 2 * RAY();
    assert balanceAfter <= balanceBefore + amount + 2 * RAY();
    // assert balanceAfter <= balanceBefore + amount + 1;
}

rule depositUpdatesUserATokenBalance2(env e) {
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
    //require balanceBefore == 20*RAY(); //under approx

    mathint superBalanceBefore = _aToken.superBalance(e, onBehalfOf);
    require superBalanceBefore == 20*RAY(); //under approx
    // mathint currentLiquidityRateBefore = getCurrentLiquidityRate(e, asset);
    mathint liquidityIndexBefore = getLiquidityIndex(e, asset);
    // require currentLiquidityRateBefore == 1;
    require liquidityIndexBefore == 1*RAY();

    // e.msg.sender pays amount of asset and aToken balance of 'onBehalfOf' increases by amount
    deposit(e, asset, amount, onBehalfOf, referralCode);

    mathint balanceAfter = aTokenBalanceOf(e, onBehalfOf);
    mathint superBalanceAfter = _aToken.superBalance(e, onBehalfOf);
    // mathint currentLiquidityRateAfter = getCurrentLiquidityRate(e, asset);
    // mathint liquidityIndexAfter = getLiquidityIndex(e, asset);

    // assert currentLiquidityRateBefore == currentLiquidityRateAfter;
    // assert liquidityIndexBefore == liquidityIndexAfter;

    // assert superBalanceAfter == superBalanceBefore + amount;
    assert balanceAfter >= superBalanceBefore + amount;
    assert balanceAfter <= superBalanceBefore + amount + RAY();
    // assert balanceAfter <= balanceBefore + amount + 1;
}

/*
    This is a Specification File for Smart Contract Verification with the Certora Prover.
    This file is run with scripts/verifyPool.sh
*/

/*
    Declaration of contracts used in the spec
*/
using ATokenHarness as _aToken;
// using StableDebtTokenHarness as _stable
// using VariableDebtToken as _variable
// using SimpleERC20 as _asset
// using SymbolicPriceOracle as priceOracle
using AaveProtocolDataProvider as _dataProvider;
using ReserveConfiguration as RC;
using SimpleERC20 as _underlyingAsset;

/*

Methods Summerizations and Enviroment-Free (e.g relative to e.msg variables) Declarations 

*/

methods {
    //Pool
    /*    function getReserveList(uint256 index) external returns (address) envfree;
    function getReserveDataIndex(address token) external returns (uint256) envfree;
    function getReservesCount() external returns (uint256) envfree;*/
    function _.handleAction(address, uint256, uint256) external => NONDET;
    //function _dataProvider.getConfigurationData(address) external returns (uint256, uint256, uint256, uint256, uint256, bool, bool, bool, bool, bool) envfree;
    /*
    function getUserEMode(address) external returns uint256 envfree;
    function getAssetEMode(address) external returns uint256 envfree;
    function getAssetId(address) external returns uint16 envfree;
    function reserveAddressById(uint256) external returns address envfree;
    
    function isFrozenReserve(address asset) external returns bool envfree;
    function isPausedReserve(address asset) external returns bool envfree;
    function isBorrowableReserve(address) external returns bool envfree;
    function isStableRateBorrowableReserve(address) external returns bool envfree;
    function getReserveATokenAddress(address) external returns address envfree;
    function getReserveStableDebtTokenAddress(address) external returns address envfree;
    function getReserveVariableDebtTokenAddress(address) external returns address envfree;
    function getReserveLiquidityIndex(address) external returns uint256 envfree;
    function getReserveCurrentLiquidityRate(address) external returns uint256 envfree;
    function getReserveVariableBorrowIndex(address) external returns uint256 envfree;
    function getReserveCurrentVariableBorrowRate(address) external returns uint256 envfree;
    function getReserveCurrentStableBorrowRate(address) external returns uint256 envfree;
    function getATokenTotalSupply(address) external returns uint256 envfree;
    function getReserveSupplyCap(address) external returns uint256 envfree;*/
    //function _.mockUserAccountData() returns (uint256, uint256, uint256, uint256, uint256, bool) => NONDET;
    //function _.mockHealthFactor() returns (uint256, bool) => NONDET;
    function _.getAssetPrice(address) external => NONDET;
    function _.getPriceOracle() external => ALWAYS(2);
    function _.getPriceOracleSentinel() external => ALWAYS(4);
    function _.isBorrowAllowed() external => NONDET;
    
    // PoolHarness
    // function getCurrScaledVariableDebt(address) external returns (uint256) envfree;

    // math
    // function _.rayMul(uint256 a, uint256 b) internal => NONDET;
    // function _.rayDiv(uint256 a, uint256 b) internal => NONDET;
    function _.percentMul(uint256 value, uint256 percentage) internal => NONDET;
    function _._getUserDebtInBaseCurrency(address user, DataTypes.ReserveData storage reserve, uint256 assetPrice, uint256 assetUnit) internal => NONDET;
    function _.rayMul(uint256 a, uint256 b) internal => rayMulSummariztion(a, b) expect uint256 ALL;
    // function _.rayDiv(uint256 a, uint256 b) internal => rayDivSummariztion(a, b) expect uint256 ALL;
    function _.rayDiv(uint256 a, uint256 b) internal => NONDET; //JB UC

    // function _.calculateLinearInterest(uint256, uint40) internal => ALWAYS(1000000000000000000000000000); // this is not good dont use this
    function _.calculateCompoundedInterest(uint256 x, uint40 t0, uint256 t1) internal => calculateCompoundedInterestSummary(x, t0, t1) expect uint256 ALL;

    // ERC20
    function _.transfer(address, uint256) external => DISPATCHER(true);
    function _.transferFrom(address, address, uint256) external => DISPATCHER(true);
    function _.approve(address, uint256) external => DISPATCHER(true);
    function _.mint(address, uint256) external => DISPATCHER(true);
    function _.burn(uint256) external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
    
    // ATOKEN
    function _.mint(address user, uint256 amount, uint256 index) external => DISPATCHER(true);
    function _.burn(address user, address receiverOfUnderlying, uint256 amount, uint256 index) external => DISPATCHER(true);
    function _.mintToTreasury(uint256 amount, uint256 index) external => DISPATCHER(true);
    function _.transferOnLiquidation(address from, address to, uint256 value) external => DISPATCHER(true);
    function _.transferUnderlyingTo(address user, uint256 amount) external => DISPATCHER(true);
    function _.handleRepayment(address user, uint256 amount) external => DISPATCHER(true);
    function _.permit(address owner, address spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external => DISPATCHER(true);
    function _.ATokenBalanceOf(address user) external => DISPATCHER(true);

    // //Unsat Core Based
    function _.getFlags(DataTypes.ReserveConfigurationMap memory self) internal => NONDET;
    function _.getParams(DataTypes.ReserveConfigurationMap memory self) internal => NONDET;
    //function _.setUsingAsCollateral(DataTypes.UserConfigurationMap storage self,uint256 reserveIndex,bool usingAsCollateral) internal => NONDET;
    //function _.setBorrowing(DataTypes.UserConfigurationMap storage self,uint256 reserveIndex,bool borrowing) internal => NONDET;

    function _.calculateUserAccountData(mapping(address => DataTypes.ReserveData) storage reservesData,mapping(uint256 => address) storage reservesList,mapping(uint8 => DataTypes.EModeCategory) storage eModeCategories,DataTypes.CalculateUserAccountDataParams memory params) internal => NONDET;
    function _._getUserBalanceInBaseCurrency(address user,DataTypes.ReserveData storage reserve,uint256 assetPrice,uint256 assetUnit) internal => NONDET;
    function _.wadDiv(uint256 a, uint256 b) internal => NONDET;
    function _.wadToRay(uint256 a) internal => NONDET;
    function _._calculateDomainSeparator() internal => NONDET;


    //Debt Tokens
    //    function _variable.scaledTotalSupply() external => DISPATCHER(true);
    function _.scaledTotalSupply() external => DISPATCHER(true);
    
    // StableDebt
    function _.mint(address user, address onBehalfOf, uint256 amount, uint256 rate) external => DISPATCHER(true);
    function _.burn(address user, uint256 amount) external => DISPATCHER(true);
    function _.getSupplyData() external => DISPATCHER(true);
    
    //variableDebt
    function _.burn(address user, uint256 amount, uint256 index) external => DISPATCHER(true);
    
    // ReserveConfiguration
    //function _.mockGetEModeCategory() returns uint256 => CONSTANT;
    //function _.mockGetActive() returns bool => CONSTANT;
    //function _.mockGetFrozen() returns bool => CONSTANT;
    //function _.mockGetBorrowingEnabled() returns bool => CONSTANT;
    //function _.mockGetStableRateBorrowingEnabled() returns bool => CONSTANT;
    //function _.mockGetPaused() returns bool => CONSTANT;
    //function _.mockGetReserveFactor() returns uint256 => CONSTANT;
    //function _.mockGetBorrowCap() returns uint256 => CONSTANT;
    //function _.mockGetBorrowableInIsolation() returns bool => CONSTANT;
    //function _.mockGetLtv() returns uint256 => CONSTANT;
    //function _.mockGetSupplyCap() returns uint256 => ALWAYS(100000000000000000000000000000000000000000000000000);
}

/* definitions and functions to be used within the spec file */

definition RAY() returns uint256 = 10^27;
definition IS_UINT256(uint256 x) returns bool = ((x >= 0) && (x <= max_uint256));

// definition ACTIVE_MASK() returns uint256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFF;
// definition FROZEN_MASK() returns uint256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDFFFFFFFFFFFFFF;

function first_term(uint256 x, uint256 y) returns uint256 { return x; }
ghost mapping(uint256 => mapping(uint256 => uint256)) calculateCompoundedInterestSummaryValues;
function calculateCompoundedInterestSummary(uint256 rate, uint40 t0, uint256 t1) returns uint256
{
    //uint256 deltaT = require_uint256(t1 - t0);
    uint256 deltaT = assert_uint256( (t1-t0) % 2^256 );
    if (deltaT == 0)
	{
            return RAY();
	}
    if (rate == RAY())
	{
            return RAY();
	}
    if (rate >= RAY())
	{
            require calculateCompoundedInterestSummaryValues[rate][deltaT] >= rate;
	}
    else{
        require calculateCompoundedInterestSummaryValues[rate][deltaT] < rate;
    }
    return calculateCompoundedInterestSummaryValues[rate][deltaT];
}

ghost mapping(uint256 => mapping(uint256 => uint256)) rayMulSummariztionValues;
ghost mapping(uint256 => mapping(uint256 => uint256)) rayDivSummariztionValues;

function rayMulSummariztion(uint256 x, uint256 y) returns uint256
{
	if (x == 0) || (y == 0)
	{
		return 0;
	}
	if (x == RAY())
	{
		return y;
	}
	if (y == RAY())
	{
		return x;
	}
	
	if (y > x)
	{
		if (y > RAY())
		{
			require rayMulSummariztionValues[y][x] >= x;
		}
		if (x > RAY())
		{
			require rayMulSummariztionValues[y][x] >= y;
		}
		return rayMulSummariztionValues[y][x];
	}
	else{
		if (x > RAY())
		{
			require rayMulSummariztionValues[x][y] >= y;
		}
		if (y > RAY())
		{
			require rayMulSummariztionValues[x][y] >= x;
		}
		return rayMulSummariztionValues[x][y];
	}
}

function rayDivSummariztion(uint256 x, uint256 y) returns uint256
{
	if (x == 0)
	{
		return 0;
	}
	if (y == RAY())
	{
		return x;
	}
	if (y == x)
	{
		return RAY();
	}
	require y > RAY() => rayDivSummariztionValues[x][y] <= x;
	require y < RAY() => x <= rayDivSummariztionValues[x][y];
	return rayDivSummariztionValues[x][y];
}

function isActiveReserve(env e, address asset) returns bool
{
    DataTypes.ReserveData data = getReserveData(e, asset);
    DataTypes.ReserveConfigurationMap configuration = data.configuration;
    bool isActive = RC.getActive(e, configuration);

    return isActive;
}

// function getReserveCacheNextLiquidityIndex(env e, address asset) returns mathint
// {
//     DataTypes.ReserveData data = getReserveData(e, asset);
//     DataTypes.ReserveCache cache = data.cache;

//     return cache.nextLiquidityIndex;
// }

function isFrozenReserve(env e, address asset) returns bool
{
    DataTypes.ReserveData data = getReserveData(e, asset);
    DataTypes.ReserveConfigurationMap configuration = data.configuration;
    bool isFrozen = RC.getFrozen(e, configuration);

    return !isFrozen;
}

function aTokenBalanceOf(env e, address user) returns uint256
{
    // DataTypes.ReserveData data = getReserveData(e, asset);
    // address aTokenAddress = data.aTokenAddress;
    // address aToken = IAToken(aTokenAddress);
    // return aToken.balanceOf(user);
    //TODO: Fix this, we need the aToken to be aToken of the asset somehow.
    return _aToken.ATokenBalanceOf(e, user);
}

// function isFrozenReserve2(env e, address asset) returns bool
// {
//     uint256 decimals;
//     uint256 ltv;
//     uint256 liquidationThreshold;
//     uint256 liquidationBonus;
//     uint256 reserveFactor;
//     bool usageAsCollateralEnabled;
//     bool borrowingEnabled;
//     bool stableBorrowRateEnabled;
//     bool isActive;
//     bool isFrozen;
//     decimals, ltv, liquidationThreshold, liquidationBonus, reserveFactor, usageAsCollateralEnabled, borrowingEnabled, stableBorrowRateEnabled, isActive, isFrozen = _dataProvider.getReserveConfigurationData(e, asset);
//     return isFrozen;
// }

// The borrowing index should monotonically increasing
// rule getReserveNormalizedVariableDebtCheck()
// {
//     env e1;
//     calldataarg args;
//     calldataarg args2;
//     address asset; uint256 amount; address onBehalfOf; uint16 referralCode;
//     require asset != _aToken;
//     uint256 oldIndex = getReserveNormalizedVariableDebt(e1, args);
//     uint256 totalDebtBefore = getCurrScaledVariableDebt(asset);
//     supply(e1, asset, amount, onBehalfOf, referralCode);
//     uint256 newIndex = getReserveNormalizedVariableDebt(e1, args);
//     assert totalDebtBefore != 0 => newIndex >= oldIndex;
// }

rule method_reachability(env e, method f) {
    calldataarg args;
    f(e, args);
    satisfy true;
}


// Violated for flashLoan, flashLoanSimple, 
// https://prover.certora.com/output/40577/6a0ff9324815417c9c5d5ac16d9e6416/?anonymousKey=0dd820519581b25388b8b635b0c8b3821990b541
// Timeout
// https://prover.certora.com/output/40577/3cda9c0d56554e28b09871bf20f2d4bb/?anonymousKey=bc4a229509291b1eec2975142e50da45119539ae
// Proved here:
// https://prover.certora.com/output/40577/33eed8a8086c4556bc3812fca1624b94/?anonymousKey=307c2714548addf7a1d16c9715155003203e3fc5
rule totalChangesOnlyWithInitDropSupplyMint(env e, method f) filtered{
    f -> !f.isView &&
    f.selector != sig:initReserve(address,address, address, address, address).selector &&
    f.selector != sig:dropReserve(address).selector &&
    f.selector != sig:mintToTreasury(address[]).selector &&
    f.selector != sig:supplyWithPermit(address,uint256,address,uint16,uint256,uint8,bytes32,bytes32).selector &&
    f.selector != sig:supply(address,uint256,address,uint16).selector
} {
    address user;
    calldataarg args;
    mathint balance_before = _aToken.ATokenBalanceOf(e, user);
    mathint total_supply_before = _aToken.totalSupply(e);
    // require total_supply_before == 10;
    // require balance_before == 5;
    f(e, args);
    mathint total_supply_after = _aToken.totalSupply(e);

    assert total_supply_before == total_supply_after; 
}


rule transferATokenDoesntChangeTotal(env e, method f) filtered{
    f -> !f.isView &&
    f.selector != sig:initReserve(address,address, address, address, address).selector &&
    f.selector != sig:dropReserve(address).selector
} {
    address user;
    calldataarg args;
    mathint balance_before = aTokenBalanceOf(e, user);
    mathint total_supply_before = _aToken.totalSupply(e);
    f(e, args);
    mathint balance_after = aTokenBalanceOf(e, user);
    mathint total_supply_after = _aToken.totalSupply(e);

    assert balance_before != balance_after => total_supply_before == total_supply_after;
}

rule cannotDepositInInactiveReserve(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;

    deposit(e, asset, amount, onBehalfOf, referralCode);


    assert isActiveReserve(e, asset);
}

rule cannotDepositInFrozenReserve(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;
    bool frozen_reserve = isFrozenReserve(e, asset);

    deposit(e, asset, amount, onBehalfOf, referralCode);

    assert !frozen_reserve;
}

rule cannotDepositZeroAmount(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;

    deposit(e, asset, amount, onBehalfOf, referralCode);

    assert amount != 0;
}

// rule depositIncreasesCollateral(env e) {
//     address asset;
//     uint256 amount;
//     address onBehalfOf;
//     uint16 referralCode;
//     mathint collateral_before = getAToken(t).balanceOf(b);

//     // Users IERC20(asset) balance decreases (transfers), while
//     // IAToken(reserveCache.aTokenAddress) balance increases

//     deposit(e, asset, amount, onBehalfOf, referralCode);
//     assert false;
// }

rule depositIncreasesUserBalance(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;
    mathint balance_before = aTokenBalanceOf(e, onBehalfOf);
    require balance_before == 6*RAY();
    mathint balance_before_sender = aTokenBalanceOf(e, e.msg.sender);
    require balance_before_sender + balance_before_sender > balance_before_sender;
    mathint underlying_balance_before = _underlyingAsset.balanceOf(e, onBehalfOf);
    mathint underlying_balance_before_sender = _underlyingAsset.balanceOf(e, e.msg.sender);
    // mathint incentivized_balance_before = 
    require to_mathint(amount) == 3*RAY();
    require asset != onBehalfOf;
    require onBehalfOf != _aToken;
    require e.msg.sender != _aToken;
    require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);
    mathint normalized_income_before = getReserveNormalizedIncome(e, asset);
    // require normalized_income_before == to_mathint(RAY()) || normalized_income_before == 2*RAY();
    require normalized_income_before == to_mathint(RAY());
    // mathint nextLiquidityIndex = getReserveCacheNextLiquidityIndex(asset);


    // e.msg.sender pays amount of asset and aToken balance of 'onBehalfOf' increases by amount
    deposit(e, asset, amount, onBehalfOf, referralCode);

    mathint balance_after = aTokenBalanceOf(e, onBehalfOf);
    mathint balance_after_sender = aTokenBalanceOf(e, e.msg.sender);
    mathint underlying_balance_after = _underlyingAsset.balanceOf(e, onBehalfOf);
    mathint underlying_balance_after_sender = _underlyingAsset.balanceOf(e, e.msg.sender);
    mathint normalized_income_after = getReserveNormalizedIncome(e, asset);
    //mathint amountScaled = amount.rayDiv(nextLiquidityIndex);
    mathint amountScaled;

    assert normalized_income_before == normalized_income_after => balance_after > balance_before;
    // assert normalized_income_before == normalized_income_after => balance_after - balance_before == amountScaled;
}

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

rule withdrawMoreThanBalanceImpossible(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;
    mathint balance_before = aTokenBalanceOf(e, e.msg.sender);
    mathint underlying_balance_before = _underlyingAsset.balanceOf(e, to);
    mathint underlying_total_before = _underlyingAsset.balanceOf(e, _aToken); //PoolHarness

    require balance_before == 6;
    require amount == 8;
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

rule withdrawUpdatesBalances(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;
    mathint balance_before = aTokenBalanceOf(e, e.msg.sender);
    mathint underlying_balance_before = _underlyingAsset.balanceOf(e, to);
    mathint underlying_total_before = _underlyingAsset.balanceOf(e, _aToken); //PoolHarness

    require balance_before == 6;
    require amount == 8;
    require asset != to;
    require to != _aToken;

    withdraw(e, asset, amount, to);

    mathint balance_after = aTokenBalanceOf(e, e.msg.sender);
    mathint underlying_balance_after = _underlyingAsset.balanceOf(e, to);
    mathint underlying_total_after = _underlyingAsset.balanceOf(e, _aToken);

    assert underlying_balance_after - underlying_balance_before == to_mathint(amount);
    assert underlying_total_before - underlying_total_after == to_mathint(amount);
    assert balance_before - balance_after == to_mathint(amount);
}


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

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
    // TODO: remove this summary: function _.calculateCompoundedInterest(uint256 x, uint40 t0, uint256 t1) internal => calculateCompoundedInterestSummary(x, t0, t1) expect uint256 ALL;

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
// ghost mapping(uint256 => mapping(uint256 => uint256)) calculateCompoundedInterestSummaryValues;
// function calculateCompoundedInterestSummary(uint256 rate, uint40 t0, uint256 t1) returns uint256
// {
//     //uint256 deltaT = require_uint256(t1 - t0);
//     uint256 deltaT = assert_uint256( (t1-t0) % 2^256 );
//     if (deltaT == 0)
// 	{
//             return RAY();
// 	}
//     if (rate == RAY())
// 	{
//             return RAY();
// 	}
//     if (rate >= RAY())
// 	{
//             require calculateCompoundedInterestSummaryValues[rate][deltaT] >= rate;
// 	}
//     else{
//         require calculateCompoundedInterestSummaryValues[rate][deltaT] < rate;
//     }
//     return calculateCompoundedInterestSummaryValues[rate][deltaT];
// }

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



// // @title P19: It's not possible to borrow with an interest rate mode that is different than 1 (stable) or 2 (variable)
// // Passing: https://prover.certora.com/output/31688/5cb1398883fb4162854b74af0bae79e9/?anonymousKey=0d7f3c6dc8249ba58a6af0d749ac7c9782611817
// rule borrowOnlyVariableOrStableRate(env e) {
//     address asset;
//     uint256 amount;
//     uint256 interestRateMode;
//     uint16 referralCode;
//     address onBehalfOf;

//     borrow@withrevert(e, asset, amount, interestRateMode, referralCode, onBehalfOf);

//     assert (interestRateMode != 1 && interestRateMode != 2) => lastReverted;
// }

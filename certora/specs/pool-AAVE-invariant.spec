import "pool-base.spec";

// using ReserveLogic as RL;
// using PoolHarness as PH;

methods {
    // math
    // function _.rayMul(uint256 a, uint256 b) internal => NONDET;
    // function _.rayDiv(uint256 a, uint256 b) internal => NONDET;
    // function _.percentMul(uint256 value, uint256 percentage) internal => NONDET;
    function _._getUserDebtInBaseCurrency(address user, DataTypes.ReserveData storage reserve, uint256 assetPrice, uint256 assetUnit) internal => NONDET;
    function _.rayMul(uint256 a, uint256 b) internal => mulDivDownAbstractPlus(a, b, 10^27) expect uint256 ALL;
    function _.rayDiv(uint256 a, uint256 b) internal => mulDivDownAbstractPlus(a, 10^27, b) expect uint256 ALL;
    // function _.rayDiv(uint256 a, uint256 b) internal => NONDET; //JB UC
	// function ReserveLogic._updateIndexes(PoolHarness.ReserveData storage reserve, PoolHarness.ReserveCache memory reserveCache) internal => _updateIndexesWrapper(reserve, reserveCache);
    function _.incrementCounter() external => ghostUpdate() expect bool ALL;
	function _.calculateInterestRates(DataTypes.CalculateInterestRatesParams params) external => NONDET;
}

ghost mapping(uint256 => mapping(uint256 => uint256)) rayMulSummariztionValues;
ghost mapping(uint256 => mapping(uint256 => uint256)) rayDivSummariztionValues;
ghost mathint counterUpdateIndexes;

function ghostUpdate() returns bool
{
    counterUpdateIndexes = counterUpdateIndexes + 1;
	return true;
}

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

// Customer's invariant that they wanted to be verified:
// The aToken total supply is never less than the total depth. 
invariant supply_gte_debt(env e, address a) 
    getTotalATokenSupply(e, a) >= getTotalDebt(e, a);

// @title updateReserveIndexesWithCache does not increase liquidity nor variable index
// TODO: fix for variable index. Proved here (currently failing):
// https://prover.certora.com/output/6893/be1581a978124ff4907a73774b878b8a/?anonymousKey=d557886cfefc63a31e0d73e846529ecd1268c429
// rule indexesNonDecresingFor_updateIndexes()
// {
//     address asset;
//     env e;

//     uint256 reserveLiquidityIndexBefore = getReserveLiquidityIndex(e, asset);
//     uint256 variableBorrowIndexBefore = getReserveVariableBorrowIndex(e, asset);
//     require reserveLiquidityIndexBefore >= RAY();
//     DataTypes.ReserveCache cache;
//     require cache.currLiquidityIndex == reserveLiquidityIndexBefore;
//     require cache.currVariableBorrowIndex == variableBorrowIndexBefore;

//     updateReserveIndexesWithCache(e, asset, cache);

//     uint256 variableBorrowIndexAfter = getReserveVariableBorrowIndex(e, asset);
//     uint256 reserveLiquidityIndexAfter = getReserveLiquidityIndex(e, asset);
//     assert variableBorrowIndexAfter >= variableBorrowIndexBefore;
//     assert reserveLiquidityIndexAfter >= reserveLiquidityIndexBefore;
// }

// @title updateReserveIndexesWithCache does not increase liquidity index
// proved here: https://prover.certora.com/output/40577/a133882942494ff1a3e79539a7c71496/?anonymousKey=aee5cf4c4d8f3b015f2ee934aa5967537fc74871
rule indexIncreasesMonotonically(env e) {
    address asset;

    mathint liquidityIndexBefore = getLiquidityIndex(e, asset);
    require liquidityIndexBefore < max_uint256;
    mathint variableBorrowIndexBefore = getReserveVariableBorrowIndex(e, asset);
    require liquidityIndexBefore >= to_mathint(RAY());

    DataTypes.ReserveCache cache;
    require to_mathint(cache.currLiquidityIndex) == liquidityIndexBefore;
    require to_mathint(cache.currVariableBorrowIndex) == variableBorrowIndexBefore;

    updateReserveIndexesWithCache(e, asset, cache);

    mathint liquidityIndexAfter = getLiquidityIndex(e, asset);

    assert liquidityIndexAfter >= liquidityIndexBefore, "liquidity index cannot decrease";
}

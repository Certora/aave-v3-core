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
	if (x == 0 || y == 0)
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

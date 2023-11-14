import "pool-base.spec";

methods {
    // math
    // function _.rayMul(uint256 a, uint256 b) internal => NONDET;
    // function _.rayDiv(uint256 a, uint256 b) internal => NONDET;
    // function _.percentMul(uint256 value, uint256 percentage) internal => NONDET;
    function _._getUserDebtInBaseCurrency(address user, DataTypes.ReserveData storage reserve, uint256 assetPrice, uint256 assetUnit) internal => NONDET;
    function _.rayMul(uint256 a, uint256 b) internal => rayMulSummarization(a, b) expect uint256 ALL;
    function _.rayDiv(uint256 a, uint256 b) internal => rayDivSummarization(a, b) expect uint256 ALL;
    // function _.rayDiv(uint256 a, uint256 b) internal => NONDET; //JB UC
}

ghost mapping(uint256 => mapping(uint256 => uint256)) rayMulSummarizationValues;
ghost mapping(uint256 => mapping(uint256 => uint256)) rayDivSummarizationValues;

function rayMulSummarization(uint256 x, uint256 y) returns uint256
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
			require rayMulSummarizationValues[y][x] >= x;
		}
		if (x > RAY())
		{
			require CrayMulSummarizationValues[y][x] >= y;
		}
		return CrayMulSummarizationValues[y][x];
	}
	else{
		if (x > RAY())
		{
			require CrayMulSummarizationValues[x][y] >= y;
		}
		if (y > RAY())
		{
			require CrayMulSummarizationValues[x][y] >= x;
		}
		return CrayMulSummarizationValues[x][y];
	}
}

function rayDivSummarization(uint256 x, uint256 y) returns uint256
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
	require y > RAY() => rayDivSummarizationValues[x][y] <= x;
	require y < RAY() => x <= rayDivSummarizationValues[x][y];
	return rayDivSummarizationValues[x][y];
}

invariant supply_gte_debt(env e, address a) 
    getTotalATokenSupply(e, a) >= getTotalDebt(e, a);

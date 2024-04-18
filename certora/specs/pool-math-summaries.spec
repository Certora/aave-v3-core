/*
    This is a Base Specification File for Smart Contract Verification with the Certora Prover.
    This file is meant to be included
*/
import "CVLMath.spec";

methods {
    function _.wadDiv(uint256 a, uint256 b) internal => wadDivPreciseSummarization(a, b) expect uint256 ALL;
    function _.wadMul(uint256 a, uint256 b) internal => wadMulPreciseSummarization(a, b) expect uint256 ALL;
    function _.wadToRay(uint256 a) internal => wadToRayPreciseSummarization(a) expect uint256 ALL;
    function _.rayToWad(uint256 a) internal => rayToWadPreciseSummarization(a) expect uint256 ALL;
    
	// use methods from CVLMath for non-precise summarizations, e.g. mulDivDownAbstractPlus(a, b, 10^27)
	function _.rayMul(uint256 a, uint256 b) internal => rayMulPreciseSummarization(a, b) expect uint256 ALL;
    function _.rayDiv(uint256 a, uint256 b) internal => rayDivPreciseSummarization(a, b) expect uint256 ALL;
    }

/* definitions and functions to be used within the spec file */

definition WAD() returns uint256 = 10^18;
definition WadRay_ratio() returns uint256 = 10^9;
definition IS_UINT256(uint256 x) returns bool = ((x >= 0) && (x <= max_uint256));

function rayMulPreciseSummarization(uint256 x, uint256 y) returns uint256
{
    if ((x == 0) || (y == 0))
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

    mathint c = x * y;
	return require_uint256(c / RAY());
}

function rayDivPreciseSummarization(uint256 x, uint256 y) returns uint256
{
    require y != 0;
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
    mathint c = x * RAY();
	return require_uint256(c / y);
}

function wadMulPreciseSummarization(uint256 x, uint256 y) returns uint256
{
    if ((x == 0) || (y == 0))
	{
		return 0;
	}
	if (x == WAD())
	{
		return y;
	}
	if (y == WAD())
	{
		return x;
	}

    mathint c = x * y;
	return require_uint256(c / WAD());
}

function wadDivPreciseSummarization(uint256 x, uint256 y) returns uint256
{
    require y != 0;
    if (x == 0)
	{
		return 0;
	}
	if (y == WAD())
	{
		return x;
	}
    if (y == x)
	{
		return WAD();
	}
    mathint c = x * WAD();
	return require_uint256(c / y);
}

function wadToRayPreciseSummarization(uint256 x) returns uint256
{
    if (x == 0)
	{
		return 0;
	}
    mathint c = x * WadRay_ratio();
    require c <= max_uint256;
	return require_uint256(c);
}

function rayToWadPreciseSummarization(uint256 x) returns uint256
{
    if (x == 0)
	{
		return 0;
	}
    mathint c = x / WadRay_ratio();
	return require_uint256(c);
}

/*
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
			require rayMulSummarizationValues[y][x] >= y;
		}
		return rayMulSummarizationValues[y][x];
	}
	else{
		if (x > RAY())
		{
			require rayMulSummarizationValues[x][y] >= y;
		}
		if (y > RAY())
		{
			require rayMulSummarizationValues[x][y] >= x;
		}
		return rayMulSummarizationValues[x][y];
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
*/
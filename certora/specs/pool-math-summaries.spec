/*
    This is a Base Specification File for Smart Contract Verification with the Certora Prover.
    This file is meant to be included
*/

methods {
    function _.wadDiv(uint256 a, uint256 b) internal => wadDivPreciseSummarization(a, b) expect uint256 ALL;
    function _.wadMul(uint256 a, uint256 b) internal => wadMulPreciseSummarization(a, b) expect uint256 ALL;
    function _.wadToRay(uint256 a) internal => wadToRayPreciseSummarization(a) expect uint256 ALL;
    function _.rayToWad(uint256 a) internal => rayToWadPreciseSummarization(a) expect uint256 ALL;
    function _.rayMul(uint256 a, uint256 b) internal => rayMulPreciseSummarization(a, b) expect uint256 ALL;
    function _.rayDiv(uint256 a, uint256 b) internal => rayDivPreciseSummarization(a, b) expect uint256 ALL;
    }

/* definitions and functions to be used within the spec file */

definition RAY() returns uint256 = 10^27;
definition WAD() returns uint256 = 10^18;
definition WadRay_ratio() returns uint256 = 10^9;
definition IS_UINT256(uint256 x) returns bool = ((x >= 0) && (x <= max_uint256));

function rayMulPreciseSummarization(uint256 x, uint256 y) returns uint256
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
    if (x == 0) || (y == 0)
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
    assert c <= max_uint256;
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

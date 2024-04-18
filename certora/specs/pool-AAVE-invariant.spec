import "pool-base.spec";

// using ReserveLogic as RL;
// using PoolHarness as PH;

methods {
    // math
    // function _.percentMul(uint256 value, uint256 percentage) internal => NONDET;
    function _._getUserDebtInBaseCurrency(address user, DataTypes.ReserveData storage reserve, uint256 assetPrice, uint256 assetUnit) internal => NONDET;
    // function ReserveLogic._updateIndexes(PoolHarness.ReserveData storage reserve, PoolHarness.ReserveCache memory reserveCache) internal => _updateIndexesWrapper(reserve, reserveCache);
    function _.incrementCounter() external => ghostUpdate() expect bool ALL;
	function _.calculateInterestRates(DataTypes.CalculateInterestRatesParams params) external => NONDET;
}

ghost mathint counterUpdateIndexes;

function ghostUpdate() returns bool
{
    counterUpdateIndexes = counterUpdateIndexes + 1;
	return true;
}


// Customer's invariant that they wanted to be verified:
// The aToken total supply is never less than the total depth. 
invariant supply_gte_debt(env e, address a) 
    getTotalATokenSupply(e, a) >= getTotalDebt(e, a);

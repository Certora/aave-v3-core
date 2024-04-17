import "pool-base.spec";

invariant supply_gte_debt(env e, address a) 
    getTotalATokenSupply(e, a) >= getTotalDebt(e, a);

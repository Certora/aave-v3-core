import "pool-simple-properties.spec";

methods {
    // //Unsat Core Based
    function _.getFlags(DataTypes.ReserveConfigurationMap memory self) internal => NONDET;
    function _.setUsingAsCollateral(DataTypes.UserConfigurationMap storage self,uint256 reserveIndex,bool usingAsCollateral) internal => NONDET;
    function _.setBorrowing(DataTypes.UserConfigurationMap storage self,uint256 reserveIndex,bool borrowing) internal => NONDET;
    // function _.getTotalATokenSupply(address asset) external envfree => DISPATCHER(true);
    // function _.getTotalDebt(address asset) external envfree => DISPATCHER(true);
}

invariant supply_gte_debt(env e, address user)
    getTotalATokenSupply(e, user) >= getTotalDebt(e, user);

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
    // f.selector != sig:repayWithPermit(address,uint256,uint256,address,uint256,uint8,bytes32,bytes32).selector &&
    // f.selector != sig:swapBorrowRateMode(address,uint256).selector &&
    // f.selector != sig:flashLoan(address,address[],uint256[],uint256[],address,bytes,uint16).selector &&
    // f.selector != sig:repay(address,uint256,uint256,address).selector &&
    // f.selector != sig:deposit(address,uint256,address,uint16).selector &&
    // f.selector != sig:flashLoanSimple(address,address,uint256,bytes,uint16).selector &&
    // f.selector != sig:borrow(address,uint256,uint256,uint16,address).selector &&
    // f.selector != sig:mintUnbacked(address,uint256,address,uint16).selector
} {
    address user;
    calldataarg args;
    // mathint balance_before = _aToken.ATokenBalanceOf(e, user);
    // mathint superBalanceBefore = _aToken.superBalance(e, user);
    mathint totalSupplyBefore = getTotalATokenSupply(e, user);

    f(e, args);

    // mathint superBalanceAfter = _aToken.superBalance(e, user);
    mathint totalSupplyAfter = getTotalATokenSupply(e, user);

    assert totalSupplyBefore == totalSupplyAfter; 
}

rule totalDeptCanChangeInFunctions(env e, method f) filtered{
    f -> !f.isView //&&
    //f.selector != sig:initReserve(address,address, address, address, address).selector &&
    //f.selector != sig:dropReserve(address).selector &&
    //f.selector != sig:mintToTreasury(address[]).selector &&
    //f.selector != sig:supplyWithPermit(address,uint256,address,uint16,uint256,uint8,bytes32,bytes32).selector &&
    //f.selector != sig:supply(address,uint256,address,uint16).selector
    // f.selector != sig:repayWithPermit(address,uint256,uint256,address,uint256,uint8,bytes32,bytes32).selector &&
    // f.selector != sig:swapBorrowRateMode(address,uint256).selector &&
    // f.selector != sig:flashLoan(address,address[],uint256[],uint256[],address,bytes,uint16).selector &&
    // f.selector != sig:repay(address,uint256,uint256,address).selector &&
    // f.selector != sig:deposit(address,uint256,address,uint16).selector &&
    // f.selector != sig:flashLoanSimple(address,address,uint256,bytes,uint16).selector &&
    // f.selector != sig:borrow(address,uint256,uint256,uint16,address).selector &&
    // f.selector != sig:mintUnbacked(address,uint256,address,uint16).selector
} {
    address user;
    calldataarg args;
    // mathint balance_before = _aToken.ATokenBalanceOf(e, user);
    // mathint superBalanceBefore = _aToken.superBalance(e, user);
    mathint totalDebtBefore = getTotalDebt(e, user);

    f(e, args);

    // mathint superBalanceAfter = _aToken.superBalance(e, user);
    mathint totalDebtAfter = getTotalDebt(e, user);

    satisfy totalDebtAfter != totalDebtBefore;
}

// Run: https://prover.certora.com/output/40577/9b8ea632aa4147288a6a8b5309e78021/?anonymousKey=8c1dd7499eb3c52ed76045917b1b2dccb1031162
rule transferATokenDoesntChangeTotal(env e, method f) filtered{
    f -> !f.isView &&
    f.selector != sig:initReserve(address,address, address, address, address).selector &&
    f.selector != sig:dropReserve(address).selector
} {
    address user;
    calldataarg args;
    mathint superBalanceBefore = _aToken.superBalance(e, user);
    // mathint balance_before = aTokenBalanceOf(e, user);
    mathint superTotalSupplyBefore = _aToken.totalSupply(e);

    f(e, args);

    mathint superBalanceAfter = _aToken.superBalance(e, user);
    // mathint balance_after = aTokenBalanceOf(e, user);
    mathint superTotalSupplyAfter = _aToken.superTotalSupply(e);

    assert superBalanceBefore != superBalanceAfter => superTotalSupplyBefore == superTotalSupplyAfter; 
}

// Fail: https://prover.certora.com/output/40577/25353c2624c547f6a572638a9e02ddf1/?anonymousKey=8410b75b3c1acaa83426c83f6a874a5f5e0ac094
rule depositIncreasesCollateral(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;
    // mathint underlying_balance_before = _underlyingAsset.balanceOf(e, onBehalfOf);
    mathint underlying_balance_before_sender = _underlyingAsset.balanceOf(e, e.msg.sender);
    // mathint normalized_income_before = getReserveNormalizedIncome(e, asset);
    
    // mathint currentLiquidityRateBefore = getCurrentLiquidityRate(e, asset);
    mathint liquidityIndexBefore = getLiquidityIndex(e, asset);

    require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);

    // Users IERC20(asset) balance decreases (transfers), while
    // IAToken(reserveCache.aTokenAddress) balance increases

    deposit(e, asset, amount, onBehalfOf, referralCode);

    // mathint underlying_balance_after = _underlyingAsset.balanceOf(e, onBehalfOf);
    mathint underlying_balance_after_sender = _underlyingAsset.balanceOf(e, e.msg.sender);
    // mathint normalized_income_after = getReserveNormalizedIncome(e, asset);

    // mathint currentLiquidityRateAfter = getCurrentLiquidityRate(e, asset);
    mathint liquidityIndexAfter = getLiquidityIndex(e, asset);
    
    // assert normalized_income_before == normalized_income_after => underlying_balance_before_sender > underlying_balance_after_sender;
    assert liquidityIndexBefore == liquidityIndexAfter => underlying_balance_before_sender > underlying_balance_after_sender;
}

// Proved
// https://prover.certora.com/output/40577/fad5aaf8dcd749448281077a94787820/?anonymousKey=0038e1e03f375e0e1a5b77a77f703ed059a86afd
rule depositIncreasesUserATokenSuperBalance(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;

    require to_mathint(amount) == 3*RAY(); //under approx
    require asset != onBehalfOf;
    require onBehalfOf != _aToken;
    require e.msg.sender != _aToken;
    require e.msg.sender != asset;
    require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);

    mathint superBalanceBefore = _aToken.superBalance(e, onBehalfOf);
    // mathint currentLiquidityRateBefore = getCurrentLiquidityRate(e, asset);
    // mathint liquidityIndexBefore = getLiquidityIndex(e, asset);

    // e.msg.sender pays amount of asset and aToken balance of 'onBehalfOf' increases by amount
    deposit(e, asset, amount, onBehalfOf, referralCode);

    mathint superBalanceAfter = _aToken.superBalance(e, onBehalfOf);
    // mathint currentLiquidityRateAfter = getCurrentLiquidityRate(e, asset);
    // mathint liquidityIndexAfter = getLiquidityIndex(e, asset);

    // assert currentLiquidityRateBefore == currentLiquidityRateAfter;
    // assert liquidityIndexBefore == liquidityIndexAfter;

    assert superBalanceAfter > superBalanceBefore;
}

// Fail: https://prover.certora.com/output/40577/288f87a364d54f05830b8a81d84bd77a/?anonymousKey=b149f5f79632a64822c0f1910cc81fa7250ea36b
rule depositIncreasesProtocolBalance(env e) {
    address asset;
    uint256 amount;
    address onBehalfOf;
    uint16 referralCode;

    mathint protocol_balance_before = _underlyingAsset.balanceOf(e, PH);

    require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);

    deposit(e, asset, amount, onBehalfOf, referralCode);

    mathint protocol_balance_after = _underlyingAsset.balanceOf(e, PH);
    assert protocol_balance_after > protocol_balance_before;
}

// Withdraws an `amount` of underlying asset from the reserve, burning the equivalent aTokens owned
// Proved:
// https://prover.certora.com/output/40577/0a227dfaafe049878749cbb457dc1ce6/?anonymousKey=cec9f01cf719afaf9da325844327adcdfd326bab
// https://prover.certora.com/jobStatus/40577/2876335c933045198787c064989bfb12?anonymousKey=24e7e680172e162529800f2f55f4d3cd822ee886
rule withdrawDecreasesATokenSuperBalance(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;
    mathint superBalanceBefore = _aToken.superBalance(e, e.msg.sender);

    require asset != to;
    require to != _aToken;
    require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);

    withdraw(e, asset, amount, to);

    mathint superBalanceAfter = _aToken.superBalance(e, e.msg.sender);

    assert superBalanceAfter < superBalanceBefore;
}

// Timeout: https://prover.certora.com/output/40577/d55923cefc064fdd85629c0cfea39f23/?anonymousKey=956ec5e9fabc7e9d1cd33a3b04c9ecdcd1c4c756
rule withdrawDecreasesLiquidityIndex(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;
    mathint liquidityIndexBefore = getLiquidityIndex(e, asset);

    require asset != to;
    require to != _aToken;
    require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);

    withdraw(e, asset, amount, to);

    mathint liquidityIndexAfter = getLiquidityIndex(e, asset);

    assert liquidityIndexAfter <= liquidityIndexBefore;
}

// Fail: https://prover.certora.com/output/40577/df497927ef314cc0b113ece511b707b2/?anonymousKey=48c714e420cf80eafaaed0c8da8fcc4726e950cc
rule withdrawDecreasesCurrentLiquidityRate(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;
    mathint currentLiquidityRateBefore = getCurrentLiquidityRate(e, asset);
    mathint liquidityIndexBefore = getLiquidityIndex(e, asset);

    require asset != to;
    require to != _aToken;
    require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);

    withdraw(e, asset, amount, to);

    mathint currentLiquidityRateAfter = getCurrentLiquidityRate(e, asset);
    mathint liquidityIndexAfter = getLiquidityIndex(e, asset);

    require liquidityIndexAfter <= liquidityIndexBefore;
    assert currentLiquidityRateAfter <= currentLiquidityRateBefore;
}

// Proved:
// https://prover.certora.com/output/40577/5102cf7a05444c85a097d26bbe171fc7/?anonymousKey=e81634ce1bc99cbb3064230f94ad90f3b79f621e
rule withdrawIncreasesUnderlyingBalance(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;
    mathint underlying_balance_before = _underlyingAsset.balanceOf(e, to); // asset is given to 'to'

    require asset != to;
    require to != _aToken;
    require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);

    withdraw(e, asset, amount, to);

    mathint underlying_balance_after = _underlyingAsset.balanceOf(e, to);

    assert underlying_balance_after > underlying_balance_before;
}

// Fail: https://prover.certora.com/output/40577/8faf3ebc2bec45d6a6c54f72c0403348/?anonymousKey=1759c21cba7b118a5de4ca1d99634e67966726e6
rule withdrawDecreasesProtocolUnderlyingBalance(env e) {
    address asset;
    uint256 amount;
    address to;
    uint16 referralCode;
    mathint underlying_protocol_before = _underlyingAsset.balanceOf(e, PH); // PoolHarness loses this asset

    require asset != to;
    require to != _aToken;
    require asset == _aToken.UNDERLYING_ASSET_ADDRESS(e);

    withdraw(e, asset, amount, to);

    mathint underlying_protocol_after = _underlyingAsset.balanceOf(e, PH);

    assert underlying_protocol_after < underlying_protocol_before;
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

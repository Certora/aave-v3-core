
# POOL properties

## Unit-test 

### Supply
 `supply(address asset, uint256 amount, address onBehalfOf, uint16 referralCode) ` 

 1. Increases atoken balance of onBehalfOf
 1. atoken balance of msg.sender does not change
 1. Decreases asset balance of msg.sender
 1. asset balance of onBehalfOf stays the same
 1. asset balance of atoken increases 

### FlashLoan
1. System balance can only increase
1. no reentrancy call 

## State Transition
1. every operation by msg.sender leaves his account in a solvent position

 ## Valid State
### flags vs actual balance

1. aToken.balance(user) > 0 <=> getUserConfig(user).userConfig.isUsingAsCollateral(reserve.id);
    
    
1. debtToken.balance(user) > 0 <=> getUserConfig(user).getBorrowing(debtToken)
    


 ## High Level

 1. Monotonicity of asset.balance(atoken) vs atoken.totalSupply()
 asset.balance(atoken) @ before < asset.balance(atoken) @ after <=>
atoken.totalSupply() @ before < atoken.totalSupply() @ after
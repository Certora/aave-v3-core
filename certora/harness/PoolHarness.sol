// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.10;

import {Pool} from '../munged/protocol/pool/Pool.sol';
import {DataTypes} from '../../contracts/protocol/libraries/types/DataTypes.sol';
import {ReserveLogic} from '../../contracts//protocol/libraries/logic/ReserveLogic.sol';
import {IPoolAddressesProvider} from '../../contracts//interfaces/IPoolAddressesProvider.sol';

import {IERC20} from '../../contracts/dependencies/openzeppelin/contracts/IERC20.sol';



contract PoolHarness is Pool {
    
    using ReserveLogic for DataTypes.ReserveData;
    using ReserveLogic for DataTypes.ReserveCache;

    constructor(IPoolAddressesProvider provider) public Pool(provider){}

    function getCurrScaledVariableDebt(address asset) public view returns (uint256){
        DataTypes.ReserveData storage reserve = _reserves[asset];
        DataTypes.ReserveCache memory reserveCache = reserve.cache();
        return reserveCache.currScaledVariableDebt;
    }

    function getTotalDebt(address asset) public view returns (uint256) {
        uint256 totalVariable = IERC20(_reserves[asset].variableDebtTokenAddress).totalSupply();
        uint256 totalStable = IERC20(_reserves[asset].stableDebtTokenAddress).totalSupply();
        return totalVariable + totalStable;
    }

    function getTotalATokenSupply(address asset) public view returns (uint256) {
        return IERC20(_reserves[asset].aTokenAddress).totalSupply();
    }
}

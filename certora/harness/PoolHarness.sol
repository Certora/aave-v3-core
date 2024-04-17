// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.10;

import {Pool} from '../munged/protocol/pool/Pool.sol';
import {DataTypes} from '../munged/protocol/libraries/types/DataTypes.sol';
import {ReserveLogic} from '../munged/protocol/libraries/logic/ReserveLogic.sol';
import {IPoolAddressesProvider} from '../munged/interfaces/IPoolAddressesProvider.sol';
import {ReserveConfiguration} from '../munged/protocol/libraries/configuration/ReserveConfiguration.sol';
import {IERC20} from '../munged/dependencies/openzeppelin/contracts/IERC20.sol';

contract PoolHarness is Pool {
    
    using ReserveLogic for DataTypes.ReserveData;
    using ReserveLogic for DataTypes.ReserveCache;
    using ReserveConfiguration for DataTypes.ReserveConfigurationMap;

    constructor(IPoolAddressesProvider provider) public Pool(provider){}

    function getCurrScaledVariableDebt(address asset) public view returns (uint256){
        DataTypes.ReserveData storage reserve = _reserves[asset];
        DataTypes.ReserveCache memory reserveCache = reserve.cache();
        return reserveCache.currScaledVariableDebt;
    }

    function isStableRateEnabled(address asset) public view returns (bool) {
        DataTypes.ReserveData storage reserve = _reserves[asset];
        DataTypes.ReserveCache memory reserveCache = reserve.cache();

        return reserveCache.reserveConfiguration.getStableRateBorrowingEnabled();
    }

    function getStableRateConstant() public view returns (uint256) {
        return uint256(DataTypes.InterestRateMode.STABLE);
    }

    function getVariableRateConstant() public view returns (uint256) {
        return uint256(DataTypes.InterestRateMode.VARIABLE);
    }

    function getTotalDebt(address asset) public view returns (uint256) {
        uint256 totalVariable = IERC20(_reserves[asset].variableDebtTokenAddress).totalSupply();
        uint256 totalStable = IERC20(_reserves[asset].stableDebtTokenAddress).totalSupply();
        return totalVariable + totalStable;
    }

    function getTotalATokenSupply(address asset) public view returns (uint256) {
        return IERC20(_reserves[asset].aTokenAddress).totalSupply();
    }

    function getAvailableLiquidity(address asset) public view returns (uint256) {
        return IERC20(asset).balanceOf(_reserves[asset].aTokenAddress);
    }

    function getStableRate(address asset) public view returns (uint256) {
        return _reserves[asset].currentStableBorrowRate;
    }

    function getReserveStableBorrowRate(address asset) public view returns (uint256) {
        return _reserves[asset].currentStableBorrowRate;
    } 

    function ballanceOfInAsset(address asset, address user) public view returns (uint256) {
        return IERC20(_reserves[asset].aTokenAddress).balanceOf(user);
    }

    function getReserveLiquidityIndex(address asset) public view returns (uint256) {
        return _reserves[asset].liquidityIndex;
    } 

    function getReserveVariableBorrowIndex(address asset) public view returns (uint256) {
        return _reserves[asset].variableBorrowIndex;
    } 

    function getReserveVariableBorrowRate(address asset) public view returns (uint256) {
        return _reserves[asset].currentVariableBorrowRate;
    } 




    function updateReserveIndexes(address asset) public returns (bool) {
        ReserveLogic._updateIndexes(_reserves[asset], _reserves[asset].cache());
        return true;
    } 

    function updateReserveIndexesWithCache(address asset, DataTypes.ReserveCache memory cache) public returns (bool) {
        ReserveLogic._updateIndexes(_reserves[asset], cache);
        return true;
    } 

    function isActiveReserve(address asset) public returns (bool)
    {
        DataTypes.ReserveData storage reserve = _reserves[asset];
        return ReserveConfiguration.getActive(reserve.configuration);
    }

    function isFrozenReserve(address asset) public returns (bool)
    {
        DataTypes.ReserveData storage reserve = _reserves[asset];
        return reserve.configuration.getFrozen();
    }

    function isEnabledForBorrow(address asset) public returns (bool)
    {
        DataTypes.ReserveData storage reserve = _reserves[asset];
        return reserve.configuration.getBorrowingEnabled();
    }

}

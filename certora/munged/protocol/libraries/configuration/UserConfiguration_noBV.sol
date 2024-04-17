// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.0;

import {Errors} from '../helpers/Errors.sol';
import {DataTypes} from '../types/DataTypes.sol';
import {ReserveConfiguration} from './ReserveConfiguration.sol';

library UserConfiguration {
  using ReserveConfiguration for DataTypes.ReserveConfigurationMap;

  function setBorrowing(
    DataTypes.UserConfigurationMap storage self,
    uint256 reserveIndex,
    bool borrowing) internal {
      require(reserveIndex < ReserveConfiguration.MAX_RESERVES_COUNT, Errors.INVALID_RESERVE_INDEX);
      bool borrowingBefore = self.isBorrowing[reserveIndex];
      if (borrowingBefore != borrowing) {
        if (borrowing) self.borrowingCount++;  
        else self.borrowingCount--;
        self.isBorrowing[reserveIndex] = borrowing;
      }
  }

  function setUsingAsCollateral(
    DataTypes.UserConfigurationMap storage self,
    uint256 reserveIndex,
    bool usingAsCollateral
  ) internal {
      require(reserveIndex < ReserveConfiguration.MAX_RESERVES_COUNT, Errors.INVALID_RESERVE_INDEX);
      bool usingAsCollateralBefore = self.isUsingAsCollateral[reserveIndex];
      if (usingAsCollateral != usingAsCollateralBefore) {
        if (usingAsCollateral) self.usingAsCollateralCount++;  
        else self.usingAsCollateralCount--;
        self.isUsingAsCollateral[reserveIndex] = usingAsCollateral;
      }
  }

  function isUsingAsCollateralOrBorrowing(
    DataTypes.UserConfigurationMap memory self,
    uint256 reserveIndex
  ) internal pure returns (bool) {
    require(reserveIndex < ReserveConfiguration.MAX_RESERVES_COUNT, Errors.INVALID_RESERVE_INDEX);
    return self.isBorrowing[reserveIndex] || self.isUsingAsCollateral[reserveIndex];
  }

  function isBorrowing(
    DataTypes.UserConfigurationMap memory self,
    uint256 reserveIndex
  ) internal pure returns (bool) {
      require(reserveIndex < ReserveConfiguration.MAX_RESERVES_COUNT, Errors.INVALID_RESERVE_INDEX);
      return self.isBorrowing[reserveIndex];
  }
  
  function isUsingAsCollateral(
    DataTypes.UserConfigurationMap memory self,
    uint256 reserveIndex
  ) internal pure returns (bool) {
    require(reserveIndex < ReserveConfiguration.MAX_RESERVES_COUNT, Errors.INVALID_RESERVE_INDEX);
    return self.isUsingAsCollateral[reserveIndex];
  }

  function isUsingAsCollateralOne(
    DataTypes.UserConfigurationMap memory self
  ) internal pure returns (bool) {
    return self.usingAsCollateralCount == 1;
  }

  function isUsingAsCollateralAny(
    DataTypes.UserConfigurationMap memory self
  ) internal pure returns (bool) {
    return self.usingAsCollateralCount > 0;
  }

  function isBorrowingOne(DataTypes.UserConfigurationMap memory self) internal pure returns (bool) {
    return self.borrowingCount == 1;
  }

  function isBorrowingAny(DataTypes.UserConfigurationMap memory self) internal pure returns (bool) {
    return self.borrowingCount > 0;
  }

  function isEmpty(DataTypes.UserConfigurationMap memory self) internal pure returns (bool) {
    return self.borrowingCount == 0 && self.usingAsCollateralCount == 0;
  }

  function getIsolationModeState(
    DataTypes.UserConfigurationMap memory self,
    mapping(address => DataTypes.ReserveData) storage reservesData,
    mapping(uint256 => address) storage reservesList
  ) internal view returns (bool, address, uint256) {
    if (isUsingAsCollateralOne(self)) {
      uint256 assetId = _getFirstUsingAsCollateralAssetID(self);
      address assetAddress = reservesList[assetId];
      uint256 ceiling = reservesData[assetAddress].configuration.getDebtCeiling();
      if (ceiling != 0) {
        return (true, assetAddress, ceiling);
      }
    }
    return (false, address(0), 0);
  }

  function getSiloedBorrowingState(
    DataTypes.UserConfigurationMap memory self,
    mapping(address => DataTypes.ReserveData) storage reservesData,
    mapping(uint256 => address) storage reservesList
  ) internal view returns (bool, address) {
    if (isBorrowingOne(self)) {
      uint256 assetId = _getFirstBorrowingAssetID(self);
      address assetAddress = reservesList[assetId];
      if (reservesData[assetAddress].configuration.getSiloedBorrowing()) {
        return (true, assetAddress);
      }
    }
    return (false, address(0));
  }

  function _getFirstBorrowingAssetID(
    DataTypes.UserConfigurationMap memory self
  ) internal pure returns (uint256) {
    for (uint i = 0; i < ReserveConfiguration.MAX_RESERVES_COUNT; i++) {
        if (self.isBorrowing[i]) { return i; }
    }
    return ReserveConfiguration.MAX_RESERVES_COUNT; //error fallback
}

function _getFirstUsingAsCollateralAssetID(
    DataTypes.UserConfigurationMap memory self
  ) internal pure returns (uint256) {
    for (uint i = 0; i < ReserveConfiguration.MAX_RESERVES_COUNT; i++) {
        if (self.isUsingAsCollateral[i]) { return i; }
    }
    return ReserveConfiguration.MAX_RESERVES_COUNT; //error fallback
}

function _isValidState(
    DataTypes.UserConfigurationMap memory self
  ) internal pure returns (bool) {
    bool correctSize = 
        self.isBorrowing.length == ReserveConfiguration.MAX_RESERVES_COUNT &&
        self.isUsingAsCollateral.length == ReserveConfiguration.MAX_RESERVES_COUNT;
    if (!correctSize) { return false; } 
    //we require equality to be able to scale the complexity by modifying MAX_RESERVES_COUNT

    uint borrowingAssetsCount = 0;
    uint usingAsCollateralAssetsCount = 0;
    for (uint i = 0; i < ReserveConfiguration.MAX_RESERVES_COUNT; i++) {
        if (self.isUsingAsCollateral[i]) { usingAsCollateralAssetsCount++; }
        if (self.isBorrowing[i]) { borrowingAssetsCount++; }
    }
    return self.borrowingCount == borrowingAssetsCount && 
        self.usingAsCollateralCount == usingAsCollateralAssetsCount;
}
}

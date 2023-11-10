// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.0;

import {Errors} from '../munged/protocol/libraries/helpers/Errors.sol';
import {DataTypes} from '../munged/protocol/libraries/types/DataTypes.sol';
import {ReserveConfiguration} from '../munged/protocol/libraries/configuration/ReserveConfiguration.sol';

library UserConfiguration {
  using ReserveConfiguration for DataTypes.ReserveConfigurationMap;
  uint16 public constant MAX_RESERVES_SUMMARY = 3;

  function setBorrowing(
    DataTypes.UserConfigurationMap storage self,
    uint256 reserveIndex,
    bool borrowing) internal {
      require(reserveIndex < ReserveConfiguration.MAX_RESERVES_COUNT, Errors.INVALID_RESERVE_INDEX);
      require(reserveIndex < MAX_RESERVES_SUMMARY, "Too mamy reserves for this summary");
      if (reserveIndex == 0) { self.isBorrowing0 = borrowing; }
      if (reserveIndex == 1) { self.isBorrowing1 = borrowing; }
      if (reserveIndex == 2) { self.isBorrowing2 = borrowing; }
  }

  function setUsingAsCollateral(
    DataTypes.UserConfigurationMap storage self,
    uint256 reserveIndex,
    bool usingAsCollateral
  ) internal {
      require(reserveIndex < ReserveConfiguration.MAX_RESERVES_COUNT, Errors.INVALID_RESERVE_INDEX);
      require(reserveIndex < MAX_RESERVES_SUMMARY, "Too mamy reserves for this summary");
      if (reserveIndex == 0) { self.isUsingAsCollateral0 = usingAsCollateral; }
      if (reserveIndex == 1) { self.isUsingAsCollateral1 = usingAsCollateral; }
      if (reserveIndex == 2) { self.isUsingAsCollateral2 = usingAsCollateral; }
  }

  function isUsingAsCollateralOrBorrowing(
    DataTypes.UserConfigurationMap memory self,
    uint256 reserveIndex
  ) internal pure returns (bool) {
    require(reserveIndex < ReserveConfiguration.MAX_RESERVES_COUNT, Errors.INVALID_RESERVE_INDEX);
      require(reserveIndex < MAX_RESERVES_SUMMARY, "Too mamy reserves for this summary");
      if (reserveIndex == 0) { return self.isBorrowing0 || self.isUsingAsCollateral0; }
      if (reserveIndex == 1) { return self.isBorrowing1 || self.isUsingAsCollateral1; }
      if (reserveIndex == 2) { return self.isBorrowing2 || self.isUsingAsCollateral2; }

      require(false, "error fallback");
      return false;
  }

  function isBorrowing(
    DataTypes.UserConfigurationMap memory self,
    uint256 reserveIndex
  ) internal pure returns (bool) {
      require(reserveIndex < ReserveConfiguration.MAX_RESERVES_COUNT, Errors.INVALID_RESERVE_INDEX);
      require(reserveIndex < MAX_RESERVES_SUMMARY, "Too mamy reserves for this summary");
      if (reserveIndex == 0) { return self.isBorrowing0; }
      if (reserveIndex == 1) { return self.isBorrowing1; }
      if (reserveIndex == 2) { return self.isBorrowing2; }
      
      require(false, "error fallback");
      return false;
  }
  
  function isUsingAsCollateral(
    DataTypes.UserConfigurationMap memory self,
    uint256 reserveIndex
  ) internal pure returns (bool) {
    require(reserveIndex < ReserveConfiguration.MAX_RESERVES_COUNT, Errors.INVALID_RESERVE_INDEX);
      require(reserveIndex < MAX_RESERVES_SUMMARY, "Too mamy reserves for this summary");
      if (reserveIndex == 0) { return self.isUsingAsCollateral0; }
      if (reserveIndex == 1) { return self.isUsingAsCollateral1; }
      if (reserveIndex == 2) { return self.isUsingAsCollateral2; }

      require(false, "error fallback");
      return false;
  }

  function isUsingAsCollateralOne(
    DataTypes.UserConfigurationMap memory self
  ) internal pure returns (bool) {
    return 
      (self.isUsingAsCollateral0 && 
        !self.isUsingAsCollateral1 && 
        !self.isUsingAsCollateral2) ||
      (!self.isUsingAsCollateral0 && 
        self.isUsingAsCollateral1 && 
        !self.isUsingAsCollateral2) ||
      (!self.isUsingAsCollateral0 && 
        !self.isUsingAsCollateral1 && 
        self.isUsingAsCollateral2);
  }

  function isUsingAsCollateralAny(
    DataTypes.UserConfigurationMap memory self
  ) internal pure returns (bool) {
    return self.isUsingAsCollateral0 || 
      self.isUsingAsCollateral1 || self.isUsingAsCollateral2;
  }

  function isBorrowingOne(DataTypes.UserConfigurationMap memory self) internal pure returns (bool) {
    return 
      (self.isBorrowing0 && !self.isBorrowing1 && !self.isBorrowing2) ||
      (!self.isBorrowing0 && self.isBorrowing1 && !self.isBorrowing2) ||
      (!self.isBorrowing0 && !self.isBorrowing1 && self.isBorrowing2);
  }

  function isBorrowingAny(DataTypes.UserConfigurationMap memory self) internal pure returns (bool) {
    return self.isBorrowing0 || self.isBorrowing1 || self.isBorrowing2;
  }

  function isEmpty(DataTypes.UserConfigurationMap memory self) internal pure returns (bool) {
    return !self.isBorrowing0 && !self.isBorrowing1 && !self.isBorrowing2 &&
      !self.isUsingAsCollateral0 && !self.isUsingAsCollateral1 && !self.isUsingAsCollateral2;
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
    if (self.isBorrowing0) { return 0; }
    if (self.isBorrowing1) { return 1; }
    if (self.isBorrowing2) { return 2; }
    
    require(false, "error fallback");
    return MAX_RESERVES_SUMMARY;
  }

function _getFirstUsingAsCollateralAssetID(
    DataTypes.UserConfigurationMap memory self
  ) internal pure returns (uint256) {
    if (self.isUsingAsCollateral0) { return 0; }
    if (self.isUsingAsCollateral1) { return 1; }
    if (self.isUsingAsCollateral2) { return 2; }

    require(false, "error fallback");
    return MAX_RESERVES_SUMMARY;
}

}

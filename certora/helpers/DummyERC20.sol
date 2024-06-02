// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.0;
import {IERC20} from '../munged/dependencies/openzeppelin/contracts/IERC20.sol';

contract DummyERC20 is IERC20 {
    constructor(string memory name_, string memory symbol_) 
        IERC20(name_,symbol_){}
}

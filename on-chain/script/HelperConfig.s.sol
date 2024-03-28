// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {Script} from "forge-std/Script.sol";

contract HelperConfig is Script {
    uint256 public deployerKey;

    constructor() {
        if (block.chainid == 80001) {
            deployerKey = vm.envUint("MUMBAI_PRIVATE_KEY");
        } else {
            deployerKey = vm.envUint("DEFAULT_ANVIL_KEY");
        }
    }
}

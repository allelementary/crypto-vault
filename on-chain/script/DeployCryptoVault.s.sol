// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import {Script} from "forge-std/Script.sol";
import {CryptoVault} from "../src/CryptoVault.sol";
import {HelperConfig} from "./HelperConfig.s.sol";

contract DeployCryptoVault is Script {
    address[] public tokenAddresses;
    address[] public priceFeedAddresses;

    function run() external returns (CryptoVault) {
        HelperConfig helperConfig = new HelperConfig();
        uint256 deployerKey = helperConfig.deployerKey();

        vm.startBroadcast(deployerKey);
        CryptoVault cryptoVault = new CryptoVault();
        vm.stopBroadcast();
        return cryptoVault;
    }
}

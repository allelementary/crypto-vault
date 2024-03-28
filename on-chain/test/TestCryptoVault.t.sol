// SPDX-License-Identifier: MIT

pragma solidity ^0.8.22;

import {Test, console} from "forge-std/Test.sol";
import {CryptoVault} from "../src/CryptoVault.sol";

contract TestCryptoVault is Test {
    CryptoVault cryptoVault;
    address UserOne = address(1);

    bytes public app = "MyApp";
    bytes public env = "MyEnv";
    bytes public data = "MySecretData";

    function setUp() public {
        cryptoVault = new CryptoVault();
    }

    function testStore() public {
        cryptoVault.store(app, env, data);
        bytes memory storedData = cryptoVault.retrieve(app, env);
        assertEq(storedData, data, "Stored data does not match the input data");
    }

    function testRetrieveData() public {
        vm.startPrank(UserOne);
        cryptoVault.store(app, env, data);
        bytes memory retrievedData = cryptoVault.retrieve(app, env);
        assertEq(retrievedData, data, "Retrieved data does not match stored data");

        vm.stopPrank();
    }
}
